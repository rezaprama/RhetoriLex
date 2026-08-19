from __future__ import annotations

from pathlib import Path
import sys
import tempfile
import unittest
import zipfile


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from package_plugin import build_archive, verify_archive  # noqa: E402


class PluginPackagingTests(unittest.TestCase):
    def test_archive_is_verified_and_carries_mixed_license_notices(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            archive = Path(raw) / "rhetorilex-plugin.zip"
            built, sidecar, digest = build_archive(ROOT, output=archive, expected_version="0.1.0")

            self.assertEqual(built, archive.resolve())
            self.assertTrue(sidecar.is_file())
            self.assertEqual(verify_archive(built, expected_version="0.1.0"), digest)

            with zipfile.ZipFile(built) as package:
                names = set(package.namelist())

            required = {
                "NOTICE",
                "PROVENANCE.md",
                "REUSE.toml",
                "THIRD_PARTY_NOTICES.md",
                "LICENSES/Apache-2.0.txt",
                "LICENSES/CC-BY-4.0.txt",
                "skills/rhetorilex/assets/patterns.json",
            }
            self.assertEqual(required - names, set())


if __name__ == "__main__":
    unittest.main()
