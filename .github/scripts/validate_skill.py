"""Perform dependency-free quick checks for a bundled Codex skill."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
from urllib.parse import unquote


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
ICON_RE = re.compile(r"^\s*icon_(?:small|large):\s*[\"']?([^\"'\s]+)", re.MULTILINE)
WORKBOOK_SUFFIXES = {".xls", ".xlsx", ".xlsb", ".xlsm", ".ods", ".numbers"}


class SkillError(ValueError):
    pass


def _frontmatter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise SkillError("SKILL.md must begin with YAML frontmatter")
    try:
        closing = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration as exc:
        raise SkillError("SKILL.md frontmatter has no closing delimiter") from exc
    values: dict[str, str] = {}
    for line in lines[1:closing]:
        match = re.match(r"^([a-zA-Z_][a-zA-Z0-9_-]*):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip("\"'")
    return values, "\n".join(lines[closing + 1 :]).strip()


def validate(path: Path) -> list[str]:
    errors: list[str] = []
    skill_file = path / "SKILL.md"
    if not skill_file.is_file():
        return ["SKILL.md is missing"]
    try:
        text = skill_file.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return [f"SKILL.md is not readable UTF-8: {exc}"]
    try:
        metadata, body = _frontmatter(text)
    except SkillError as exc:
        return [str(exc)]
    name = metadata.get("name", "")
    if not NAME_RE.fullmatch(name) or len(name) > 64:
        errors.append("frontmatter name must be lower-case hyphen-case and at most 64 characters")
    if name != path.name:
        errors.append(f"frontmatter name {name!r} must match directory {path.name!r}")
    if not metadata.get("description"):
        errors.append("frontmatter description is required")
    if len(body) < 200:
        errors.append("SKILL.md body is too short to provide usable instructions")
    if "[TODO" in text or "TODO:" in text:
        errors.append("SKILL.md contains TODO placeholders")

    for raw_target in LINK_RE.findall(text):
        target = raw_target.strip().split(maxsplit=1)[0].strip("<>\"'")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        local = path / unquote(target.split("#", 1)[0])
        if not local.is_file():
            errors.append(f"broken local reference: {target}")

    agent_file = path / "agents" / "openai.yaml"
    if agent_file.is_file():
        try:
            agent_text = agent_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            errors.append(f"agents/openai.yaml is not readable UTF-8: {exc}")
        else:
            if "interface:" not in agent_text or "default_prompt:" not in agent_text:
                errors.append("agents/openai.yaml needs interface and default_prompt")
            for target in ICON_RE.findall(agent_text):
                while target.startswith("./"):
                    target = target[2:]
                if not (path / target).is_file():
                    errors.append(f"agents/openai.yaml icon is missing: {target}")

    for item in path.rglob("*"):
        if item.is_symlink():
            errors.append(f"symbolic link is not allowed: {item.relative_to(path)}")
        if item.is_file() and item.suffix.casefold() in WORKBOOK_SUFFIXES:
            errors.append(f"workbook is not allowed in skill: {item.relative_to(path)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", type=Path)
    args = parser.parse_args()
    errors = validate(args.skill.resolve())
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1
    print(f"valid skill: {args.skill}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
