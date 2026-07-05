param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$RunserverArgs
)

$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$python = Join-Path $root '.venv\Scripts\python.exe'
$watcherScript = Join-Path $root 'watch_tailwind.ps1'
$watcherArguments = "-NoProfile -ExecutionPolicy Bypass -File `"$watcherScript`""
$forwardedRunserverArgs = @()
$djangoDebug = $null

foreach ($arg in $RunserverArgs) {
    switch -Regex ($arg) {
        '^--debug=(true|1|yes|on)$' {
            $djangoDebug = 'true'
            continue
        }
        '^--debug=(false|0|no|off)$' {
            $djangoDebug = 'false'
            continue
        }
        '^--production-errors$' {
            $djangoDebug = 'false'
            continue
        }
        '^--dev-errors$' {
            $djangoDebug = 'true'
            continue
        }
        default {
            $forwardedRunserverArgs += $arg
        }
    }
}

if ($null -ne $djangoDebug) {
    $env:DJANGO_DEBUG = $djangoDebug
}

if ($env:DJANGO_DEBUG -eq 'false' -and [string]::IsNullOrWhiteSpace($env:DJANGO_ALLOWED_HOSTS)) {
    $env:DJANGO_ALLOWED_HOSTS = '127.0.0.1,localhost'
}

$debugDisplay = if ([string]::IsNullOrWhiteSpace($env:DJANGO_DEBUG)) { 'settings default' } else { $env:DJANGO_DEBUG }
Write-Host "Django DEBUG: $debugDisplay"
$tailwind = $null
$skipTailwindWatcher = $forwardedRunserverArgs -contains '--help' -or $forwardedRunserverArgs -contains '-h'

if (-not $skipTailwindWatcher) {
    $tailwind = Start-Process `
        -FilePath 'powershell.exe' `
        -ArgumentList $watcherArguments `
        -WorkingDirectory $root `
        -WindowStyle Hidden `
        -PassThru

    Start-Sleep -Milliseconds 750
    if ($tailwind.HasExited) {
        throw "Tailwind watcher failed to start (exit code $($tailwind.ExitCode))."
    }
}

try {
    & $python manage.py runserver @forwardedRunserverArgs
    exit $LASTEXITCODE
}
finally {
    if ($null -ne $tailwind) {
        $tailwind.Refresh()
        if (-not $tailwind.HasExited) {
            try {
                & taskkill.exe /PID $tailwind.Id /T /F *>$null
            }
            catch {
                $tailwind.Refresh()
                if (-not $tailwind.HasExited) {
                    Write-Warning "Tailwind watcher cleanup failed for PID $($tailwind.Id)."
                }
            }
        }
    }
}
