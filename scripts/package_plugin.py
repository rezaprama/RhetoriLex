"""Build and verify a deterministic, self-checking RhetoriLex plugin archive."""

from __future__ import annotations

import argparse
from io import BytesIO
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
import tempfile
from typing import Any, Iterable
import zipfile


ROOT = Path(__file__).resolve().parents[1]
PACKAGE_DIRECTORIES = (".codex-plugin", "skills", "assets")
PACKAGE_FILES = (
    "NOTICE",
    "PROVENANCE.md",
    "REUSE.toml",
    "THIRD_PARTY_NOTICES.md",
    "LICENSES/Apache-2.0.txt",
    "LICENSES/CC-BY-4.0.txt",
)
MANIFEST_PATH = ".codex-plugin/plugin.json"
CHECKSUM_PATH = "SHA256SUMS"
FIXED_TIMESTAMP = (1980, 1, 1, 0, 0, 0)
FILE_MODE = 0o100644
PLUGIN_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
VERSION_RE = re.compile(
    r"^(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
RESTRICTED_NAMES = {"academic_phrasebank_sections.xlsx"}
WORKBOOK_SUFFIXES = {".xls", ".xlsx", ".xlsb", ".xlsm", ".ods", ".numbers"}
OLE_SIGNATURE = bytes.fromhex("D0CF11E0A1B11AE1")


class PackageError(ValueError):
    """Raised when plugin input or an archive violates the package contract."""


def _json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise PackageError(f"duplicate JSON key: {key}")
        value[key] = item
    return value


def _load_json(data: bytes, member: str) -> dict[str, Any]:
    try:
        value = json.loads(data.decode("utf-8"), object_pairs_hook=_json_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PackageError(f"{member}: invalid UTF-8 JSON: {exc}") from exc
    if not isinstance(value, dict):
        raise PackageError(f"{member}: expected a JSON object")
    return value


def _safe_member(name: str) -> str:
    if not name or "\\" in name or name.startswith("/"):
        raise PackageError(f"unsafe archive path: {name!r}")
    path = PurePosixPath(name)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise PackageError(f"unsafe archive path: {name!r}")
    return path.as_posix()


def _looks_like_workbook(data: bytes) -> bool:
    if data.startswith(OLE_SIGNATURE):
        return True
    if not data.startswith(b"PK"):
        return False
    try:
        with zipfile.ZipFile(BytesIO(data)) as archive:
            names = {name.casefold() for name in archive.namelist()}
    except (OSError, zipfile.BadZipFile):
        return False
    return any(name.startswith("xl/") for name in names) or (
        "mimetype" in names
        and b"application/vnd.oasis.opendocument.spreadsheet" in data[:4096]
    )


def _reject_restricted(name: str, data: bytes) -> None:
    path = PurePosixPath(name)
    if path.name.casefold() in RESTRICTED_NAMES:
        raise PackageError(f"restricted workbook cannot be packaged: {name}")
    if path.suffix.casefold() in WORKBOOK_SUFFIXES:
        raise PackageError(f"workbook files cannot be packaged: {name}")
    if any(part.casefold() == "private" for part in path.parts):
        raise PackageError(f"private source material cannot be packaged: {name}")
    if _looks_like_workbook(data):
        raise PackageError(f"embedded or renamed workbook cannot be packaged: {name}")


def collect_payload(root: Path) -> dict[str, bytes]:
    root = root.resolve()
    payload: dict[str, bytes] = {}
    for directory in PACKAGE_DIRECTORIES:
        source = root / directory
        if not source.is_dir():
            raise PackageError(f"required plugin directory missing: {directory}/")
        found_file = False
        for path in sorted(source.rglob("*"), key=lambda item: item.as_posix()):
            if path.is_symlink():
                raise PackageError(f"symbolic links are not allowed: {path.relative_to(root)}")
            if path.is_dir():
                continue
            if not path.is_file():
                raise PackageError(f"unsupported filesystem entry: {path.relative_to(root)}")
            found_file = True
            member = _safe_member(path.relative_to(root).as_posix())
            data = path.read_bytes()
            _reject_restricted(member, data)
            payload[member] = data
        if not found_file:
            raise PackageError(f"required plugin directory is empty: {directory}/")
    for filename in PACKAGE_FILES:
        path = root / filename
        if not path.is_file() or path.is_symlink():
            raise PackageError(f"required plugin notice missing or invalid: {filename}")
        member = _safe_member(filename)
        data = path.read_bytes()
        _reject_restricted(member, data)
        payload[member] = data
    return payload


def _local_reference(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PackageError(f"manifest {field} must be a non-empty local path")
    reference = value.strip()
    if "://" in reference or reference.startswith(("/", "\\")):
        raise PackageError(f"manifest {field} must be a relative local path")
    while reference.startswith("./"):
        reference = reference[2:]
    reference = reference.rstrip("/")
    return _safe_member(reference)


def validate_manifest(payload: dict[str, bytes]) -> dict[str, Any]:
    if MANIFEST_PATH not in payload:
        raise PackageError(f"required manifest missing: {MANIFEST_PATH}")
    manifest = _load_json(payload[MANIFEST_PATH], MANIFEST_PATH)
    name = manifest.get("name")
    if not isinstance(name, str) or len(name) > 64 or not PLUGIN_NAME_RE.fullmatch(name):
        raise PackageError("manifest name must be lower-case hyphen-case and at most 64 characters")
    version = manifest.get("version")
    if not isinstance(version, str) or not VERSION_RE.fullmatch(version):
        raise PackageError("manifest version must be a semantic version")
    description = manifest.get("description")
    if not isinstance(description, str) or len(description.strip()) < 12:
        raise PackageError("manifest description must be meaningful")

    skills_path = _local_reference(manifest.get("skills"), "skills")
    if skills_path != "skills":
        raise PackageError("manifest skills must point to ./skills/")
    expected_skill = f"skills/{name}/SKILL.md"
    if expected_skill not in payload:
        raise PackageError(f"primary skill missing: {expected_skill}")

    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        raise PackageError("manifest interface must be an object")
    asset_fields: list[tuple[str, Any]] = [
        ("interface.composerIcon", interface.get("composerIcon")),
        ("interface.logo", interface.get("logo")),
    ]
    screenshots = interface.get("screenshots", [])
    if not isinstance(screenshots, list):
        raise PackageError("manifest interface.screenshots must be an array")
    asset_fields.extend(
        (f"interface.screenshots[{index}]", value)
        for index, value in enumerate(screenshots)
    )
    for field, value in asset_fields:
        member = _local_reference(value, field)
        if not member.startswith("assets/"):
            raise PackageError(f"manifest {field} must point inside ./assets/")
        if member not in payload:
            raise PackageError(f"manifest {field} target missing: {member}")
    return manifest


def checksum_document(payload: dict[str, bytes]) -> bytes:
    lines = [
        f"{hashlib.sha256(payload[name]).hexdigest()}  {name}"
        for name in sorted(payload)
    ]
    return ("\n".join(lines) + "\n").encode("ascii")


def _write_archive(path: Path, payload: dict[str, bytes]) -> None:
    members = dict(payload)
    members[CHECKSUM_PATH] = checksum_document(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=path.parent, prefix=f".{path.name}.", suffix=".tmp", delete=False
        ) as handle:
            temporary = Path(handle.name)
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_STORED) as archive:
            for name in sorted(members):
                info = zipfile.ZipInfo(name, date_time=FIXED_TIMESTAMP)
                info.compress_type = zipfile.ZIP_STORED
                info.create_system = 3
                info.external_attr = FILE_MODE << 16
                archive.writestr(info, members[name])
        temporary.replace(path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def _write_sidecar(path: Path, archive: Path) -> str:
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    body = f"{digest}  {archive.name}\n"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="ascii", newline="\n")
    return digest


def build_archive(
    root: Path,
    output: Path | None = None,
    checksum_output: Path | None = None,
    expected_version: str | None = None,
) -> tuple[Path, Path, str]:
    payload = collect_payload(root)
    manifest = validate_manifest(payload)
    if expected_version is not None and manifest["version"] != expected_version:
        raise PackageError(
            f"manifest version {manifest['version']} does not match requested {expected_version}"
        )
    if output is None:
        output = root / "dist" / f"{manifest['name']}-plugin-{manifest['version']}.zip"
    output = output.resolve()
    if checksum_output is None:
        checksum_output = output.with_name(f"{output.name}.sha256")
    checksum_output = checksum_output.resolve()
    if output == checksum_output:
        raise PackageError("archive and checksum paths must differ")
    _write_archive(output, payload)
    digest = _write_sidecar(checksum_output, output)
    return output, checksum_output, digest


def _read_archive(path: Path) -> tuple[dict[str, bytes], list[zipfile.ZipInfo]]:
    try:
        with zipfile.ZipFile(path) as archive:
            if archive.comment:
                raise PackageError("archive comment is not allowed")
            infos = archive.infolist()
            names = [info.filename for info in infos]
            if len(names) != len(set(names)):
                raise PackageError("archive contains duplicate member names")
            if names != sorted(names):
                raise PackageError("archive members are not sorted")
            payload: dict[str, bytes] = {}
            for info in infos:
                name = _safe_member(info.filename)
                if info.is_dir():
                    raise PackageError(f"directory entries are not allowed: {name}")
                if info.date_time != FIXED_TIMESTAMP:
                    raise PackageError(f"non-deterministic timestamp on {name}")
                if info.compress_type != zipfile.ZIP_STORED:
                    raise PackageError(f"non-deterministic compression on {name}")
                if info.create_system != 3 or (info.external_attr >> 16) != FILE_MODE:
                    raise PackageError(f"non-canonical file mode on {name}")
                if info.extra or info.comment or info.flag_bits & 0x1:
                    raise PackageError(f"unsupported ZIP metadata on {name}")
                data = archive.read(info)
                _reject_restricted(name, data)
                payload[name] = data
    except (OSError, zipfile.BadZipFile) as exc:
        raise PackageError(f"cannot read plugin archive: {exc}") from exc
    return payload, infos


def verify_archive(path: Path, expected_version: str | None = None) -> str:
    members, _ = _read_archive(path)
    if CHECKSUM_PATH not in members:
        raise PackageError(f"archive missing {CHECKSUM_PATH}")
    payload = {name: data for name, data in members.items() if name != CHECKSUM_PATH}
    for directory in PACKAGE_DIRECTORIES:
        if not any(name.startswith(f"{directory}/") for name in payload):
            raise PackageError(f"archive missing {directory}/ content")
    for filename in PACKAGE_FILES:
        if filename not in payload:
            raise PackageError(f"archive missing required plugin notice: {filename}")
    manifest = validate_manifest(payload)
    if expected_version is not None and manifest["version"] != expected_version:
        raise PackageError(
            f"archive version {manifest['version']} does not match requested {expected_version}"
        )
    expected_checksums = checksum_document(payload)
    if members[CHECKSUM_PATH] != expected_checksums:
        raise PackageError(f"archive {CHECKSUM_PATH} is invalid or non-canonical")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="plugin repository root")
    parser.add_argument("--output", type=Path, help="destination ZIP path")
    parser.add_argument("--checksum-output", type=Path, help="destination SHA-256 sidecar")
    parser.add_argument("--expected-version", help="require this manifest semantic version")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check-only", action="store_true", help="validate source without writing")
    mode.add_argument("--verify", type=Path, metavar="ZIP", help="verify an existing archive")
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.verify is not None:
            digest = verify_archive(args.verify.resolve(), args.expected_version)
            print(f"valid plugin archive: {args.verify} ({digest})")
            return 0
        root = args.root.resolve()
        if args.check_only:
            payload = collect_payload(root)
            manifest = validate_manifest(payload)
            if args.expected_version is not None and manifest["version"] != args.expected_version:
                raise PackageError(
                    f"manifest version {manifest['version']} does not match requested "
                    f"{args.expected_version}"
                )
            print(f"valid plugin source: {manifest['name']} {manifest['version']} ({len(payload)} files)")
            return 0
        output, checksum, digest = build_archive(
            root=root,
            output=args.output,
            checksum_output=args.checksum_output,
            expected_version=args.expected_version,
        )
        verify_archive(output, args.expected_version)
        print(f"built {output}")
        print(f"built {checksum}")
        print(f"sha256 {digest}")
        return 0
    except (OSError, PackageError) as exc:
        print(f"package failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
