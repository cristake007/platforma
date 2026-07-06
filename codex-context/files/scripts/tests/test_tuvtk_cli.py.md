# Source snapshot

## `scripts/tests/test_tuvtk_cli.py`

Size: 8.8 KB

```python
from __future__ import annotations

import hashlib
import io
import os
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

from scripts import tuvtk_cli


class EnvironmentFileTests(unittest.TestCase):
    def test_write_env_preserves_comments_and_updates_keys(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / ".env"
            path.write_text("# retained\nOLD=value\nKEEP=yes\n", encoding="utf-8")

            tuvtk_cli.write_env(path, {"OLD": "new", "ADDED": "value"})

            self.assertEqual(
                path.read_text(encoding="utf-8"),
                "# retained\nOLD=new\nKEEP=yes\n\nADDED=value\n",
            )

    def test_windows_environment_replaces_example_secrets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".env.example").write_text(
                "POSTGRES_DB=platforma_tuvtk\n"
                "POSTGRES_USER=postgres\n"
                "POSTGRES_PASSWORD=postgres\n"
                "POSTGRES_PORT=5432\n"
                "DJANGO_SECRET_KEY=\n",
                encoding="utf-8",
            )
            env_file = root / ".env"
            with mock.patch.object(tuvtk_cli, "ROOT", root), mock.patch.object(tuvtk_cli, "ENV_FILE", env_file):
                values = tuvtk_cli.WindowsNativeBackend({}).prepare_environment()

            self.assertNotEqual(values["POSTGRES_PASSWORD"], "postgres")
            self.assertTrue(values["DJANGO_SECRET_KEY"])
            self.assertEqual(tuvtk_cli.read_env(env_file)["POSTGRES_PASSWORD"], values["POSTGRES_PASSWORD"])


class ArchiveSafetyTests(unittest.TestCase):
    def test_zip_traversal_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            archive = root / "unsafe.zip"
            with zipfile.ZipFile(archive, "w") as bundle:
                bundle.writestr("../outside.txt", "unsafe")

            with self.assertRaises(tuvtk_cli.CliError):
                tuvtk_cli.safe_extract_zip(archive, root / "output")


class DownloadTests(unittest.TestCase):
    def test_download_verifies_sha256(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source.bin"
            source.write_bytes(b"verified")
            expected = hashlib.sha256(b"verified").hexdigest()

            destination = tuvtk_cli.download(source.as_uri(), root / "destination.bin", expected)

            self.assertEqual(destination.read_bytes(), b"verified")


class ArgumentTests(unittest.TestCase):
    def test_help_names_primary_windows_and_linux_launchers(self) -> None:
        self.assertIn("Windows: install.cmd COMMAND", tuvtk_cli.HELP)
        self.assertIn("Linux:   ./install.sh COMMAND", tuvtk_cli.HELP)
        self.assertIn("fresh-db [--yes] [--start]", tuvtk_cli.HELP)

    def test_option_value_supports_both_forms(self) -> None:
        self.assertEqual(tuvtk_cli.option_value(["--port=9000"], "--port"), "9000")
        self.assertEqual(tuvtk_cli.option_value(["--port", "9001"], "--port"), "9001")

    def test_invalid_port_is_rejected(self) -> None:
        with self.assertRaises(tuvtk_cli.CliError):
            tuvtk_cli.validate_port(0)

    def test_setup_port_supports_public_and_legacy_names(self) -> None:
        self.assertEqual(tuvtk_cli.selected_setup_port(["--port=9000"], {}), 9000)
        self.assertEqual(tuvtk_cli.selected_setup_port(["--dev-port", "9001"], {}), 9001)

    def test_setup_domain_supports_public_host_alias(self) -> None:
        self.assertEqual(tuvtk_cli.selected_setup_domain(["--public-host=example.com"]), "example.com")

    def test_linux_setup_passthrough_keeps_installer_options(self) -> None:
        self.assertEqual(
            tuvtk_cli.linux_setup_passthrough(
                [
                    "production",
                    "--port=9000",
                    "--domain=example.com",
                    "--http-port",
                    "8080",
                    "--data-dir=/srv/tuvtk",
                    "--force",
                ]
            ),
            ["--domain=example.com", "--http-port", "8080", "--data-dir=/srv/tuvtk"],
        )


class LinuxBackendTests(unittest.TestCase):
    def test_fresh_db_targets_linux_development(self) -> None:
        backend = mock.Mock()
        with mock.patch.object(tuvtk_cli, "IS_WINDOWS", False), mock.patch.object(
            tuvtk_cli, "load_config", return_value={"default_mode": "prod"}
        ), mock.patch.object(tuvtk_cli, "LinuxDockerBackend", return_value=backend):
            tuvtk_cli.main(["fresh-db", "--yes"])

        backend.invoke.assert_called_once_with("fresh-db", ["--yes"], "dev")

    def test_setup_passes_linux_installer_options(self) -> None:
        backend = tuvtk_cli.LinuxDockerBackend({})

        with mock.patch.object(backend, "_sudo", side_effect=lambda command: command), mock.patch.object(
            tuvtk_cli, "run"
        ) as runner, mock.patch.object(tuvtk_cli, "save_config"):
            backend.setup("prod", domain="example.com", passthrough=["--http-port=8080"])

        command = runner.call_args.args[0]
        self.assertIn("--domain=example.com", command)
        self.assertIn("--http-port=8080", command)

    def test_sudo_preserves_internal_installer_flags(self) -> None:
        backend = tuvtk_cli.LinuxDockerBackend({})
        with mock.patch.object(tuvtk_cli.os, "geteuid", return_value=1000, create=True), mock.patch.object(
            tuvtk_cli.shutil, "which", return_value="/usr/bin/sudo"
        ):
            command = backend._sudo(["bash", "install.sh", "--dev"])

        self.assertEqual(command[:2], ["sudo", "env"])
        self.assertIn("TUVTK_SKIP_COMMAND=true", command)

    def test_doctor_reports_missing_commands(self) -> None:
        backend = tuvtk_cli.LinuxDockerBackend({})
        output = io.StringIO()
        with mock.patch.object(tuvtk_cli.shutil, "which", return_value=None), mock.patch("sys.stdout", output):
            backend.doctor()

        self.assertIn("docker: missing/unavailable", output.getvalue())


@unittest.skipUnless(os.name == "nt", "Windows process flags")
class WindowsProcessTests(unittest.TestCase):
    def test_fresh_db_resets_windows_development_database(self) -> None:
        backend = mock.Mock()
        with mock.patch.object(tuvtk_cli, "IS_WINDOWS", True), mock.patch.object(
            tuvtk_cli, "load_config", return_value={}
        ), mock.patch.object(tuvtk_cli, "WindowsNativeBackend", return_value=backend):
            tuvtk_cli.main(["fresh-db", "--yes", "--start"])

        backend.reset_database.assert_called_once_with(True, True)

    def test_background_process_uses_no_window_flag(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            process = mock.Mock(pid=1234)
            process.poll.return_value = None
            backend = tuvtk_cli.WindowsNativeBackend({})
            with mock.patch.object(tuvtk_cli, "ROOT", root), mock.patch.object(
                tuvtk_cli, "PID_DIR", root / "pids"
            ), mock.patch.object(tuvtk_cli, "LOG_DIR", root / "logs"), mock.patch.object(
                backend, "process_running", return_value=False
            ), mock.patch.object(backend, "process_environment", return_value={}), mock.patch.object(
                tuvtk_cli.time, "sleep"
            ), mock.patch.object(tuvtk_cli.subprocess, "Popen", return_value=process) as popen:
                backend.spawn("web", ["fake.exe"])

            self.assertEqual(popen.call_args.kwargs["creationflags"], tuvtk_cli.WINDOWS_BACKGROUND_FLAGS)

    def test_foreground_processes_inherit_current_terminal(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            tailwind = mock.Mock(pid=1234)
            tailwind.poll.side_effect = [0, 0]
            web = mock.Mock(pid=1235)
            web.poll.return_value = None
            backend = tuvtk_cli.WindowsNativeBackend({})
            with mock.patch.object(tuvtk_cli, "ROOT", root), mock.patch.object(
                tuvtk_cli, "PID_DIR", root / "pids"
            ), mock.patch.object(backend, "stop_process"), mock.patch.object(
                backend, "prepare_development", return_value=Path("npm.cmd")
            ), mock.patch.object(backend, "process_environment", return_value={}), mock.patch.object(
                tuvtk_cli.subprocess, "Popen", side_effect=[tailwind, web]
            ) as popen, mock.patch.object(tuvtk_cli, "run"):
                backend.dev_foreground(prepared=True)

            self.assertEqual(popen.call_count, 2)
            for call in popen.call_args_list:
                self.assertNotIn("creationflags", call.kwargs)
                self.assertNotIn("stdout", call.kwargs)


if __name__ == "__main__":
    unittest.main()
```
