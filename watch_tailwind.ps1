$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
& (Join-Path $root 'install.ps1') tailwind @args
exit $LASTEXITCODE
