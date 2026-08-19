"""Rebuild data and plugin archives twice, then compare exact bytes."""

from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]


def digest_tree(path: Path) -> dict[str, str]:
    return {
        item.relative_to(path).as_posix(): hashlib.sha256(item.read_bytes()).hexdigest()
        for item in sorted(path.rglob("*"))
        if item.is_file()
    }


def run(*arguments: str) -> None:
    subprocess.run([sys.executable, *arguments], cwd=ROOT, check=True)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="rhetorilex-determinism-") as raw:
        temporary = Path(raw)
        builds = []
        archives = []
        for label in ("first", "second"):
            target = temporary / label
            run(
                "scripts/build_data.py",
                "--dist",
                str(target / "dist"),
                "--resources",
                str(target / "resources"),
            )
            archive = target / "plugin.zip"
            run("scripts/package_plugin.py", "--output", str(archive))
            run("scripts/package_plugin.py", "--verify", str(archive))
            builds.append(digest_tree(target / "dist") | {
                f"resources/{key}": value
                for key, value in digest_tree(target / "resources").items()
            })
            archives.append(hashlib.sha256(archive.read_bytes()).hexdigest())
        if builds[0] != builds[1]:
            print("data rebuild is not deterministic", file=sys.stderr)
            return 1
        if archives[0] != archives[1]:
            print("plugin package is not deterministic", file=sys.stderr)
            return 1
    print(f"deterministic data and plugin package: {archives[0]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
