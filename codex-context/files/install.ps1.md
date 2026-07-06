# Source snapshot

## `install.ps1`

Size: 2.7 KB

```powershell
[CmdletBinding()]
param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$CommandArgs
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$router = Join-Path $root 'scripts\tuvtk_cli.py'
$runtimeRoot = Join-Path $root '.tuvtk\runtime\python'
$runtimePython = Join-Path $runtimeRoot 'python.exe'
$minimumVersion = [Version]'3.12'

function Test-TuvtkPython {
    param([string]$Executable)

    if (-not (Test-Path -LiteralPath $Executable -PathType Leaf)) {
        return $false
    }
    try {
        $versionText = & $Executable -c "import sys; print('.'.join(map(str, sys.version_info[:3])))" 2>$null
        return ([Version]$versionText -ge $minimumVersion)
    }
    catch {
        return $false
    }
}

$python = $null
$candidates = @(
    $runtimePython,
    (Join-Path $root '.venv\Scripts\python.exe')
)

$pathPython = Get-Command python.exe -ErrorAction SilentlyContinue
if ($pathPython) {
    $candidates += $pathPython.Source
}

foreach ($candidate in $candidates) {
    if (Test-TuvtkPython -Executable $candidate) {
        $python = $candidate
        break
    }
}

if (-not $python) {
    $version = '3.12.10'
    $installerName = "python-$version-amd64.exe"
    $downloadDir = Join-Path $root '.tuvtk\downloads'
    $installer = Join-Path $downloadDir $installerName
    $url = "https://www.python.org/ftp/python/$version/$installerName"

    New-Item -ItemType Directory -Force -Path $downloadDir | Out-Null
    New-Item -ItemType Directory -Force -Path $runtimeRoot | Out-Null
    if (-not (Test-Path -LiteralPath $installer)) {
        Write-Host "[tuvtk] Downloading $url"
        $partial = "$installer.part"
        Invoke-WebRequest -Uri $url -OutFile $partial -UseBasicParsing
        Move-Item -Force -LiteralPath $partial -Destination $installer
    }

    $signature = Get-AuthenticodeSignature -LiteralPath $installer
    if ($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Subject -notmatch 'Python Software Foundation') {
        throw "Python installer signature validation failed: $($signature.Status)"
    }

    Write-Host "[tuvtk] Installing a private Python runtime"
    $arguments = @(
        '/quiet',
        'InstallAllUsers=0',
        "TargetDir=`"$runtimeRoot`"",
        'Include_pip=1',
        'Include_launcher=0',
        'PrependPath=0',
        'Shortcuts=0'
    )
    $process = Start-Process -FilePath $installer -ArgumentList $arguments -Wait -PassThru -WindowStyle Hidden
    if ($process.ExitCode -ne 0 -or -not (Test-TuvtkPython -Executable $runtimePython)) {
        throw "Private Python installation failed with exit code $($process.ExitCode)."
    }
    $python = $runtimePython
}

& $python $router @CommandArgs
exit $LASTEXITCODE
```
