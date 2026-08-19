from __future__ import annotations

from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]


class WorkflowTests(unittest.TestCase):
    def test_release_tag_regex_accepts_semver_prerelease_and_build(self) -> None:
        workflow = (ROOT / ".github" / "workflows" / "release.yml").read_text(encoding="utf-8")
        match = re.search(r'if \[\[ ! "\$version" =~ (\^.+\$) \]\]; then', workflow)
        self.assertIsNotNone(match)
        pattern = re.compile(match.group(1))

        for version in ("0.1.0", "1.2.3-rc.1", "1.2.3+build.5", "1.2.3-rc.1+build.5"):
            with self.subTest(version=version):
                self.assertIsNotNone(pattern.fullmatch(version))

        for version in ("v0.1.0", "1.2", "1.2.3-", "1.2.3+"):
            with self.subTest(version=version):
                self.assertIsNone(pattern.fullmatch(version))


if __name__ == "__main__":
    unittest.main()
