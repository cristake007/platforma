# Source snapshot

## `watch_tailwind.ps1`

Size: 156 B

```powershell
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
& (Join-Path $root 'install.ps1') tailwind @args
exit $LASTEXITCODE
```
