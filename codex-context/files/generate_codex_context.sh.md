# Source snapshot

## `generate_codex_context.sh`

Size: 170 B

```bash
#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$SCRIPT_DIR/scripts/generate_codex_context.py" "$@"
```
