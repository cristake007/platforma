# Source snapshot

## `runserver.ps1`

Size: 151 B

```powershell
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
& (Join-Path $root 'install.ps1') dev @args
exit $LASTEXITCODE
```
