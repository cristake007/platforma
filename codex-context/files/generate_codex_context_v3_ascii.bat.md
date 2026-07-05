# generate_codex_context_v3_ascii.bat

Generated: `2026-07-05T22:50:42`

## Scope

- Real source file: `generate_codex_context_v3_ascii.bat`
- App: none
- Role: `tooling`
- Size: 22880 bytes
- Source SHA-256: `69048cbf87f50095a6fb4a7b1b31070fe8ca02f5ab690c235d236c17092b31d1`

## Codex usage

Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.

## Source

```bat
@echo off
setlocal EnableExtensions

set "REPO_ROOT=%~dp0"
set "CONTEXT_DIR=%REPO_ROOT%codex-context"
set "SCRIPT_PATH=%~f0"

cd /d "%REPO_ROOT%"

powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$p=$env:SCRIPT_PATH; $lines=Get-Content -LiteralPath $p -Encoding UTF8; $marker='# POWERSHELL_START'; $start=[Array]::IndexOf($lines,$marker); if ($start -lt 0) { throw 'PowerShell marker not found.' }; $script=($lines[($start+1)..($lines.Count-1)] -join [Environment]::NewLine); Invoke-Expression $script"
exit /b %ERRORLEVEL%

# POWERSHELL_START
$ErrorActionPreference = "Stop"

$root = (Resolve-Path $env:REPO_ROOT).Path.TrimEnd("\")
$out = $env:CONTEXT_DIR.TrimEnd("\")
$generatedAt = Get-Date -Format "yyyy-MM-ddTHH:mm:ss"
$maxTextFileBytes = 300KB

$expectedOut = Join-Path $root "codex-context"
if (-not [string]::Equals(
    [System.IO.Path]::GetFullPath($out),
    [System.IO.Path]::GetFullPath($expectedOut),
    [StringComparison]::OrdinalIgnoreCase
)) {
    throw "Refusing to clean unexpected context path: $out"
}

Write-Host ""
Write-Host "==============================================="
Write-Host " Generating granular Codex Markdown context"
Write-Host "==============================================="
Write-Host ""

Write-Host "Cleaning previous generated context folder..."
if (Test-Path -LiteralPath $out) {
    Remove-Item -LiteralPath $out -Recurse -Force
}
New-Item -ItemType Directory -Path $out | Out-Null
New-Item -ItemType Directory -Path (Join-Path $out "apps") | Out-Null
New-Item -ItemType Directory -Path (Join-Path $out "files") | Out-Null

Remove-Item -LiteralPath (Join-Path $root "repomix-codex.xml") -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath (Join-Path $root "repomix-output.xml") -Force -ErrorAction SilentlyContinue
Remove-Item -LiteralPath (Join-Path $root "codex-file-map.txt") -Force -ErrorAction SilentlyContinue

$excludedDirs = @(
    "node_modules",
    "__pycache__",
    ".venv",
    ".git",
    ".vscode",
    ".agents",
    ".bootstrap_icons_cache",
    ".postgresql",
    "staticfiles",
    ".playwright-mcp",
    "test-results",
    "playwright-report",
    ".codex-plugin",
    "media",
    "codex-context"
)

$excludedExtensions = @(
    ".pyc",
    ".pyo",
    ".woff",
    ".woff2",
    ".ttf",
    ".otf",
    ".eot",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".svg",
    ".pdf",
    ".zip",
    ".7z",
    ".rar",
    ".xlsx",
    ".xls",
    ".docx",
    ".doc",
    ".pptx",
    ".csv",
    ".sqlite3",
    ".db",
    ".log",
    ".map"
)

$excludedFileNames = @(
    ".env",
    "AGENTS.md",
    "codex-file-map.txt",
    "package-lock.json"
)

$excludedAppDirs = @(
    "planificator-main"
)

function Get-Relative {
    param([string]$Path)
    return $Path.Substring($root.Length).TrimStart("\")
}

function Get-SlashPath {
    param([string]$Path)
    return $Path.Replace("\", "/")
}

function Ensure-Directory {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Path $Path | Out-Null
    }
}

function Test-Included {
    param($File)

    $relative = Get-Relative $File.FullName
    $parts = $relative -split "\\"

    if ($excludedFileNames -contains $File.Name) { return $false }
    if ($File.Name -like "repomix-output.*") { return $false }
    if ($File.Name -like "repomix-codex.*") { return $false }
    if ($excludedExtensions -contains $File.Extension.ToLowerInvariant()) { return $false }

    foreach ($dir in $excludedDirs) {
        if ($parts -contains $dir) { return $false }
    }

    if ($relative.StartsWith("apps\planificator-main\", [StringComparison]::OrdinalIgnoreCase)) { return $false }
    if ($relative.StartsWith("plugins\playwright\", [StringComparison]::OrdinalIgnoreCase)) { return $false }
    if ($relative.StartsWith("theme\static\fonts\", [StringComparison]::OrdinalIgnoreCase)) { return $false }
    if ($relative.StartsWith("theme\static\images\", [StringComparison]::OrdinalIgnoreCase)) { return $false }
    if ($relative.StartsWith("theme\static\css\dist\", [StringComparison]::OrdinalIgnoreCase)) { return $false }

    if ($File.Length -gt $maxTextFileBytes) { return $false }

    return $true
}

function Test-SkippedBySize {
    param($File)
    if ($File.Length -le $maxTextFileBytes) { return $false }
    $relative = Get-Relative $File.FullName
    $parts = $relative -split "\\"
    foreach ($dir in $excludedDirs) {
        if ($parts -contains $dir) { return $false }
    }
    if ($excludedFileNames -contains $File.Name) { return $false }
    if ($excludedExtensions -contains $File.Extension.ToLowerInvariant()) { return $false }
    return $true
}

function Get-AppName {
    param([string]$Relative)
    $parts = $Relative -split "\\"
    if ($parts.Count -ge 2 -and $parts[0] -ieq "apps") {
        return $parts[1]
    }
    return ""
}

function Get-FileRole {
    param($File)

    $relative = Get-Relative $File.FullName
    $name = $File.Name

    if ($relative -match "\\migrations\\") { return "migration" }
    if ($relative -match "\\templates\\") { return "template" }
    if ($relative -match "\\static\\") { return "static" }
    if ($relative -match "\\tests(\\|$)") { return "test" }
    if ($name -match "^tests?.*\.py$") { return "test" }
    if ($relative.StartsWith("platforma_tuvtk\", [StringComparison]::OrdinalIgnoreCase)) { return "project-config" }
    if ($relative.StartsWith("core\", [StringComparison]::OrdinalIgnoreCase)) { return "core" }
    if ($relative.StartsWith("theme\", [StringComparison]::OrdinalIgnoreCase)) { return "theme" }
    if ($relative.StartsWith("apps\", [StringComparison]::OrdinalIgnoreCase)) { return "backend" }
    if ($File.Extension -ieq ".bat" -or $File.Extension -ieq ".ps1" -or $File.Extension -ieq ".json" -or $File.Extension -ieq ".toml" -or $File.Extension -ieq ".ini" -or $File.Extension -ieq ".cfg") { return "tooling" }
    if ($File.Extension -ieq ".md" -or $File.Extension -ieq ".txt") { return "docs" }

    return "source"
}

function Get-Language {
    param($File)

    switch ($File.Extension.ToLowerInvariant()) {
        ".py" { return "python" }
        ".html" { return "html" }
        ".htm" { return "html" }
        ".js" { return "javascript" }
        ".mjs" { return "javascript" }
        ".ts" { return "typescript" }
        ".tsx" { return "tsx" }
        ".css" { return "css" }
        ".scss" { return "scss" }
        ".json" { return "json" }
        ".md" { return "markdown" }
        ".txt" { return "text" }
        ".bat" { return "bat" }
        ".cmd" { return "bat" }
        ".ps1" { return "powershell" }
        ".toml" { return "toml" }
        ".yml" { return "yaml" }
        ".yaml" { return "yaml" }
        ".ini" { return "ini" }
        ".cfg" { return "ini" }
        ".sql" { return "sql" }
        ".sh" { return "bash" }
        default { return "text" }
    }
}

function Get-CodeFence {
    param([string]$Content)

    $max = 3
    $matches = [regex]::Matches($Content, '`+')
    foreach ($match in $matches) {
        if ($match.Value.Length -ge $max) {
            $max = $match.Value.Length + 1
        }
    }
    return ('`' * $max)
}

function Get-ContextPathForFile {
    param($File)
    $relative = Get-Relative $File.FullName
    return Join-Path (Join-Path $out "files") ($relative + ".md")
}

function Get-RelativeContextPathForFile {
    param($File)
    $relative = Get-Relative $File.FullName
    return Get-SlashPath ("codex-context\files\" + $relative + ".md")
}

function Write-Utf8NoBomLines {
    param(
        [string]$Path,
        [string[]]$Lines
    )
    $parent = Split-Path -Parent $Path
    Ensure-Directory $parent
    [System.IO.File]::WriteAllLines($Path, $Lines, [System.Text.UTF8Encoding]::new($false))
}

function Write-Utf8NoBomText {
    param(
        [string]$Path,
        [string]$Text
    )
    $parent = Split-Path -Parent $Path
    Ensure-Directory $parent
    [System.IO.File]::WriteAllText($Path, $Text, [System.Text.UTF8Encoding]::new($false))
}

function Write-FileContext {
    param($File)

    $relative = Get-Relative $File.FullName
    $relativeSlash = Get-SlashPath $relative
    $appName = Get-AppName $relative
    $role = Get-FileRole $File
    $lang = Get-Language $File
    $target = Get-ContextPathForFile $File

    try {
        $content = [System.IO.File]::ReadAllText($File.FullName)
    }
    catch {
        return [pscustomobject]@{
            Relative = $relative
            Context = ""
            App = $appName
            Role = $role
            Status = "read-error"
            Error = $_.Exception.Message
        }
    }

    $sha256 = [System.Security.Cryptography.SHA256]::Create()
    try {
        $sourceHash = [System.BitConverter]::ToString(
            $sha256.ComputeHash([System.IO.File]::ReadAllBytes($File.FullName))
        ).Replace("-", "").ToLowerInvariant()
    }
    finally {
        $sha256.Dispose()
    }

    $fence = Get-CodeFence $content
    $sb = New-Object System.Text.StringBuilder

    [void]$sb.AppendLine("# $relativeSlash")
    [void]$sb.AppendLine("")
    [void]$sb.AppendLine("Generated: ``$generatedAt``")
    [void]$sb.AppendLine("")
    [void]$sb.AppendLine("## Scope")
    [void]$sb.AppendLine("")
    [void]$sb.AppendLine("- Real source file: ``$relativeSlash``")
    if ($appName) {
        [void]$sb.AppendLine("- App: ``$appName``")
        [void]$sb.AppendLine("- App guide: ``codex-context/apps/$appName.md``")
    }
    else {
        [void]$sb.AppendLine("- App: none")
    }
    [void]$sb.AppendLine("- Role: ``$role``")
    [void]$sb.AppendLine("- Size: $($File.Length) bytes")
    [void]$sb.AppendLine("- Source SHA-256: ``$sourceHash``")
    [void]$sb.AppendLine("")
    [void]$sb.AppendLine("## Codex usage")
    [void]$sb.AppendLine("")
    [void]$sb.AppendLine("Use this context only when the task directly touches this file or requires this file for routing. The real source file remains the source of truth before editing.")
    [void]$sb.AppendLine("")
    [void]$sb.AppendLine("## Source")
    [void]$sb.AppendLine("")
    [void]$sb.AppendLine("$fence$lang")
    [void]$sb.AppendLine($content.TrimEnd())
    [void]$sb.AppendLine($fence)

    Write-Utf8NoBomText $target $sb.ToString()

    return [pscustomobject]@{
        Relative = $relative
        Context = Get-SlashPath ("codex-context\files\" + $relative + ".md")
        App = $appName
        Role = $role
        Status = "ok"
        Error = ""
    }
}

Write-Host "Scanning source files..."
$allRepoFiles = @(Get-ChildItem -LiteralPath $root -Recurse -File | Sort-Object FullName)
$allFiles = @($allRepoFiles | Where-Object { Test-Included $_ } | Sort-Object FullName)
$skippedLargeFiles = @($allRepoFiles | Where-Object { Test-SkippedBySize $_ } | Sort-Object FullName)

Write-Host "Generating file map..."
$mapPath = Join-Path $out "codex-file-map.txt"
Write-Utf8NoBomLines $mapPath @($allFiles | ForEach-Object { Get-SlashPath (Get-Relative $_.FullName) })

if ($skippedLargeFiles.Count -gt 0) {
    $skippedPath = Join-Path $out "codex-skipped-large-files.txt"
    Write-Utf8NoBomLines $skippedPath @($skippedLargeFiles | ForEach-Object { "$(Get-SlashPath (Get-Relative $_.FullName)) ($($_.Length) bytes)" })
}

Write-Host "Generating one Markdown context file per source file..."
$fileRows = New-Object System.Collections.Generic.List[object]
foreach ($file in $allFiles) {
    [void]$fileRows.Add((Write-FileContext $file))
}

$okFileRows = @($fileRows | Where-Object { $_.Status -eq "ok" })
$readErrorRows = @($fileRows | Where-Object { $_.Status -ne "ok" })

if ($readErrorRows.Count -gt 0) {
    $readErrorLines = @($readErrorRows | ForEach-Object { "$(Get-SlashPath $_.Relative) :: $($_.Error)" })
    Write-Utf8NoBomLines (Join-Path $out "codex-read-errors.txt") $readErrorLines
}

function Write-AppGuide {
    param(
        [string]$AppName,
        [object[]]$Rows
    )

    $target = Join-Path (Join-Path $out "apps") ($AppName + ".md")
    $lines = New-Object System.Collections.Generic.List[string]

    [void]$lines.Add("# App context: $AppName")
    [void]$lines.Add("")
    [void]$lines.Add("Generated: ``$generatedAt``")
    [void]$lines.Add("")
    [void]$lines.Add("Local instructions: ``apps/$AppName/AGENTS.md``. They define app contracts and the smallest workflow-specific file set.")
    [void]$lines.Add("")
    [void]$lines.Add("Use this app guide to select exact file-level context. Do not load all files listed here unless the task truly affects all of them.")
    [void]$lines.Add("")
    [void]$lines.Add("## Routing")
    [void]$lines.Add("")
    [void]$lines.Add("- Backend behavior: start with ``models.py``, ``urls.py``, ``views.py``, ``forms.py``, ``services.py``, ``selectors.py``, or ``validators.py`` only if present and relevant.")
    [void]$lines.Add("- UI behavior: start with the exact template/static context file.")
    [void]$lines.Add("- Tests: read only tests related to the changed behavior.")
    [void]$lines.Add("- Migrations: read only for model/schema changes or migration debugging.")
    [void]$lines.Add("")

    $roleOrder = @("backend", "template", "static", "test", "migration", "source", "docs", "tooling")
    foreach ($role in $roleOrder) {
        $roleRows = @($Rows | Where-Object { $_.Role -eq $role } | Sort-Object Relative)
        if ($roleRows.Count -eq 0) { continue }

        $title = $role.Substring(0,1).ToUpperInvariant() + $role.Substring(1)
        [void]$lines.Add("## $title files")
        [void]$lines.Add("")
        [void]$lines.Add("| Real file | Context file |")
        [void]$lines.Add("|---|---|")
        foreach ($row in $roleRows) {
            $real = Get-SlashPath $row.Relative
            $context = $row.Context.Substring("codex-context/".Length)
            [void]$lines.Add("| ``$real`` | [``$context``](../$context) |")
        }
        [void]$lines.Add("")
    }

    Write-Utf8NoBomLines $target $lines.ToArray()
}

Write-Host "Generating one Markdown guide per app..."
$appRows = New-Object System.Collections.Generic.List[object]
$appsRoot = Join-Path $root "apps"
if (Test-Path -LiteralPath $appsRoot) {
    $appDirs = @(
        Get-ChildItem -LiteralPath $appsRoot -Directory |
        Where-Object { $excludedAppDirs -notcontains $_.Name } |
        Sort-Object Name
    )

    foreach ($appDir in $appDirs) {
        $appName = $appDir.Name
        $rows = @($okFileRows | Where-Object { $_.App -eq $appName } | Sort-Object Relative)
        if ($rows.Count -eq 0) { continue }

        Write-AppGuide $appName $rows

        [void]$appRows.Add([pscustomobject]@{
            Name = $appName
            Guide = "codex-context/apps/$appName.md"
            FileCount = $rows.Count
            BackendCount = @($rows | Where-Object { $_.Role -eq "backend" }).Count
            FrontendCount = @($rows | Where-Object { $_.Role -eq "template" -or $_.Role -eq "static" }).Count
            TestCount = @($rows | Where-Object { $_.Role -eq "test" }).Count
            MigrationCount = @($rows | Where-Object { $_.Role -eq "migration" }).Count
        })
    }
}

Write-Host "Generating project-core guide..."
$corePrefixes = @(
    "platforma_tuvtk\",
    "core\",
    "theme\static_src\",
    "theme\static\js\"
)
$coreExact = @(
    "manage.py",
    ".env.example",
    "frontend.md",
    "requirements.txt",
    "requirements-dev.txt",
    "README.md",
    "repomix.config.json",
    "generate_codex_context.bat",
    "generate_codex_context_v3_ascii.bat"
)

$coreRows = @(
    $okFileRows | Where-Object {
        $rel = $_.Relative
        foreach ($exact in $coreExact) {
            if ($rel -ieq $exact) { return $true }
        }
        foreach ($prefix in $corePrefixes) {
            if ($rel.StartsWith($prefix, [StringComparison]::OrdinalIgnoreCase)) { return $true }
        }
        return $false
    } | Sort-Object Relative
)

$coreLines = New-Object System.Collections.Generic.List[string]
[void]$coreLines.Add("# Project core context")
[void]$coreLines.Add("")
[void]$coreLines.Add("Generated: ``$generatedAt``")
[void]$coreLines.Add("")
[void]$coreLines.Add("Use this guide for project settings, root URLs, global shell/navigation, Tailwind/daisyUI source, and tooling.")
[void]$coreLines.Add("")
[void]$coreLines.Add("## File contexts")
[void]$coreLines.Add("")
[void]$coreLines.Add("| Real file | Role | Context file |")
[void]$coreLines.Add("|---|---|---|")
foreach ($row in $coreRows) {
    $real = Get-SlashPath $row.Relative
    $context = $row.Context.Substring("codex-context/".Length)
    [void]$coreLines.Add("| ``$real`` | ``$($row.Role)`` | [``$context``]($context) |")
}
Write-Utf8NoBomLines (Join-Path $out "project-core.md") $coreLines.ToArray()

Write-Host "Generating main context index..."
$index = New-Object System.Collections.Generic.List[string]
[void]$index.Add("# Codex Context Index")
[void]$index.Add("")
[void]$index.Add("Generated: ``$generatedAt``")
[void]$index.Add("")
[void]$index.Add("Use the smallest possible context. This generator creates one Markdown context file per included source file. It intentionally does not create broad app XML packs or full-repository Repomix output.")
[void]$index.Add("")
[void]$index.Add("## Start here")
[void]$index.Add("")
[void]$index.Add("1. Read the applicable repository/app ``AGENTS.md`` instructions.")
[void]$index.Add("2. If exact paths are known, open the real source files directly and skip their generated copies.")
[void]$index.Add("3. If paths are unknown, use only the relevant ``apps/<app>.md`` guide or ``project-core.md``.")
[void]$index.Add("4. Use ``codex-file-map.txt`` only to locate an unknown file, then open the smallest matching set.")
[void]$index.Add("5. Treat file contexts as hashed snapshots; the real source remains authoritative before editing.")
[void]$index.Add("")
[void]$index.Add("## Global guides")
[void]$index.Add("")
[void]$index.Add("- [``project-core.md``](project-core.md) - settings, root URLs, core shell/navigation, theme source, and tooling.")
[void]$index.Add("- ``codex-file-map.txt`` - included real source file list.")
[void]$index.Add("- ``codex-context-audit.md`` - generated coverage and integrity summary.")
if ($skippedLargeFiles.Count -gt 0) {
    [void]$index.Add("- ``codex-skipped-large-files.txt`` - text files skipped because they exceed $maxTextFileBytes bytes.")
}
if ($readErrorRows.Count -gt 0) {
    [void]$index.Add("- ``codex-read-errors.txt`` - files that could not be copied into file-level context.")
}
[void]$index.Add("")
[void]$index.Add("## App guides")

foreach ($row in ($appRows | Sort-Object Name)) {
    [void]$index.Add("")
    [void]$index.Add("### ``$($row.Name)``")
    [void]$index.Add("")
    [void]$index.Add("- Guide: [``apps/$($row.Name).md``](apps/$($row.Name).md)")
    [void]$index.Add("- Files: $($row.FileCount)")
    [void]$index.Add("- Backend: $($row.BackendCount)")
    [void]$index.Add("- Frontend/template/static: $($row.FrontendCount)")
    [void]$index.Add("- Tests: $($row.TestCount)")
    [void]$index.Add("- Migrations: $($row.MigrationCount)")
}

[void]$index.Add("")
[void]$index.Add("## Routing examples")
[void]$index.Add("")
[void]$index.Add("- ``apps/foo/models.py`` -> ``apps/foo.md`` + ``files/apps/foo/models.py.md``")
[void]$index.Add("- ``apps/foo/templates/foo/list.html`` -> ``apps/foo.md`` + ``files/apps/foo/templates/foo/list.html.md``")
[void]$index.Add("- ``platforma_tuvtk/urls.py`` -> ``project-core.md`` + ``files/platforma_tuvtk/urls.py.md``")

Write-Utf8NoBomLines (Join-Path $out "codex-context-index.md") $index.ToArray()

Write-Host "Validating generated context coverage..."
$generatedContextFiles = @(
    Get-ChildItem -LiteralPath (Join-Path $out "files") -Recurse -File -Filter "*.md"
)
if ($generatedContextFiles.Count -ne $okFileRows.Count) {
    throw "Context coverage mismatch: expected $($okFileRows.Count), found $($generatedContextFiles.Count)."
}
if ($readErrorRows.Count -gt 0) {
    throw "Context generation had $($readErrorRows.Count) source read error(s)."
}

$missingAppGuides = @(
    $appRows | Where-Object {
        -not (Test-Path -LiteralPath (Join-Path $root $_.Guide.Replace("/", "\")))
    }
)
if ($missingAppGuides.Count -gt 0) {
    throw "Missing generated app guide(s): $($missingAppGuides.Name -join ', ')."
}

$audit = New-Object System.Collections.Generic.List[string]
[void]$audit.Add("# Codex Context Audit")
[void]$audit.Add("")
[void]$audit.Add("Generated: ``$generatedAt``")
[void]$audit.Add("")
[void]$audit.Add("- Included source files: $($allFiles.Count)")
[void]$audit.Add("- Generated file contexts: $($generatedContextFiles.Count)")
[void]$audit.Add("- Generated app guides: $($appRows.Count)")
[void]$audit.Add("- Source read errors: $($readErrorRows.Count)")
[void]$audit.Add("- Files skipped by size: $($skippedLargeFiles.Count)")
[void]$audit.Add("- Coverage result: PASS")
[void]$audit.Add("")
[void]$audit.Add("Every generated file context contains a SHA-256 hash of its source snapshot. Real source files remain authoritative.")
Write-Utf8NoBomLines (Join-Path $out "codex-context-audit.md") $audit.ToArray()

$generatedList = @(
    Get-ChildItem -LiteralPath $out -Recurse -File |
    Sort-Object FullName |
    ForEach-Object { Get-SlashPath ($_.FullName.Substring($out.Length).TrimStart("\")) }
)
Write-Utf8NoBomLines (Join-Path $out "codex-generated-files.txt") $generatedList

Write-Host ""
Write-Host "Done."
Write-Host "Generated granular context folder:"
Write-Host "  codex-context\"
Write-Host ""
Write-Host "Main files:"
Write-Host "  codex-context\codex-file-map.txt"
Write-Host "  codex-context\codex-context-index.md"
Write-Host "  codex-context\codex-context-audit.md"
Write-Host "  codex-context\project-core.md"
Write-Host "  codex-context\apps\<app>.md"
Write-Host "  codex-context\files\<real-path>.md"
Write-Host ""
Write-Host "Included source files: $($allFiles.Count)"
Write-Host "Generated file contexts: $($okFileRows.Count)"
Write-Host "Generated app guides: $($appRows.Count)"
if ($skippedLargeFiles.Count -gt 0) {
    Write-Host "Skipped large files: $($skippedLargeFiles.Count)"
}
if ($readErrorRows.Count -gt 0) {
    Write-Host "Read errors: $($readErrorRows.Count)"
}
Write-Host ""
Write-Host "No full repomix-codex.xml or broad app XML packs were generated."
Write-Host ""
```
