$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $root '.venv\Scripts\python.exe'
$sourceRoots = @(
    (Join-Path $root 'theme\static_src\src'),
    (Join-Path $root 'theme\static\js'),
    (Join-Path $root 'core\templates'),
    (Join-Path $root 'apps\dashboard\templates'),
    (Join-Path $root 'apps\planificator\templates'),
    (Join-Path $root 'apps\planificator\static')
)

function Get-SourceFingerprint {
    $files = foreach ($sourceRoot in $sourceRoots) {
        if (Test-Path $sourceRoot) {
            Get-ChildItem -Path $sourceRoot -Recurse -File |
                Where-Object { $_.Extension -in '.css', '.html', '.js' }
        }
    }

    return ($files |
        Sort-Object FullName |
        ForEach-Object { '{0}|{1}|{2}' -f $_.FullName, $_.Length, $_.LastWriteTimeUtc.Ticks }) -join "`n"
}

Write-Host 'Building Tailwind CSS...'
& $python manage.py tailwind build
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

$fingerprint = Get-SourceFingerprint
Write-Host 'Watching Tailwind CSS and templates for saved changes...'

while ($true) {
    Start-Sleep -Milliseconds 750
    $nextFingerprint = Get-SourceFingerprint

    if ($nextFingerprint -ne $fingerprint) {
        $fingerprint = $nextFingerprint
        Write-Host 'Change detected. Rebuilding Tailwind CSS...'
        & $python manage.py tailwind build
    }
}
