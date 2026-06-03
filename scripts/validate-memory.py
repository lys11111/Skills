#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validate shiki-wechat-summary-plus memory YAML files."""

import sys
from pathlib import Path

REQUIRED_TOP = {"wxid", "display_name", "relationship_to_self", "updated_at", "memory", "evidence"}
RELATIONSHIPS = {"friend", "crush", "partner", "colleague", "family", "unknown"}
CONFIDENCE = {"high", "low"}
MEMORY_KEYS = {
    "birthday",
    "likes",
    "dislikes",
    "gift_ideas",
    "taboos",
    "hobbies",
    "communication_style",
    "notes",
}


def load_yaml(path: Path):
    try:
        import yaml  # type: ignore
    except ImportError:
        # minimal parser for our flat schema
        return load_yaml_minimal(path.read_text(encoding="utf-8"))
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_yaml_minimal(text: str) -> dict:
    """Tiny subset parser when PyYAML is missing."""
    import re

    data = {"memory": {}, "evidence": []}
    section = None
    for line in text.splitlines():
        if line.strip() == "memory:":
            section = "memory"
            continue
        if line.strip() == "evidence:":
            section = "evidence"
            continue
        m = re.match(r"^(\w+):\s*(.*)$", line)
        if m and section is None:
            key, val = m.group(1), m.group(2).strip()
            if val.startswith("[") or val in ("null", "~", ""):
                data[key] = [] if val.startswith("[") else None
            else:
                data[key] = val.strip('"')
        if section == "memory" and line.startswith("  "):
            m2 = re.match(r"^\s+(\w+):\s*(.*)$", line)
            if m2:
                k, v = m2.group(1), m2.group(2).strip()
                if v.startswith("["):
                    data["memory"][k] = []
                elif v in ("null", "~"):
                    data["memory"][k] = None
                else:
                    data["memory"][k] = v.strip('"')
    if not data.get("wxid"):
        raise ValueError("minimal parse failed; install pyyaml: pip install pyyaml")
    return data


def validate(data: dict, path: Path) -> list:
    errors = []
    if not isinstance(data, dict):
        return [f"{path}: root must be a mapping"]

    missing = REQUIRED_TOP - set(data.keys())
    if missing:
        errors.append(f"{path}: missing keys: {sorted(missing)}")

    rel = data.get("relationship_to_self")
    if rel and rel not in RELATIONSHIPS:
        errors.append(f"{path}: invalid relationship_to_self: {rel}")

    memory = data.get("memory")
    if memory is not None:
        if not isinstance(memory, dict):
            errors.append(f"{path}: memory must be a mapping")
        else:
            unknown = set(memory.keys()) - MEMORY_KEYS
            if unknown:
                errors.append(f"{path}: unknown memory keys: {sorted(unknown)}")

    evidence = data.get("evidence")
    if evidence is not None:
        if not isinstance(evidence, list):
            errors.append(f"{path}: evidence must be a list")
        else:
            for i, item in enumerate(evidence):
                if not isinstance(item, dict):
                    errors.append(f"{path}: evidence[{i}] must be a mapping")
                    continue
                for req in ("date", "quote", "field"):
                    if req not in item:
                        errors.append(f"{path}: evidence[{i}] missing {req}")
                conf = item.get("confidence", "high")
                if conf not in CONFIDENCE:
                    errors.append(f"{path}: evidence[{i}] bad confidence: {conf}")

    bday = (memory or {}).get("birthday") if isinstance(memory, dict) else None
    if isinstance(bday, str) and len(bday) == 10 and bday[4] == "-":
        pass  # YYYY-MM-DD allowed
    elif isinstance(bday, str) and bday and len(bday) != 5:
        errors.append(f"{path}: birthday should be MM-DD or YYYY-MM-DD, got {bday!r}")

    return errors


def main(argv=None):
    argv = argv or sys.argv[1:]
    if not argv:
        print("Usage: validate-memory.py <file.yaml> [...]", file=sys.stderr)
        return 2

    script_dir = Path(__file__).resolve().parent
    default_fixture = script_dir / "fixtures" / "memory.sample.yaml"
    paths = [Path(p) for p in argv]
    if len(paths) == 1 and paths[0].name == "--fixture":
        paths = [default_fixture]

    exit_code = 0
    for path in paths:
        if not path.is_file():
            print(f"FAIL: not found: {path}")
            exit_code = 1
            continue
        try:
            data = load_yaml(path)
            errs = validate(data, path)
        except Exception as e:
            print(f"FAIL: {path}: {e}")
            exit_code = 1
            continue
        if errs:
            exit_code = 1
            for e in errs:
                print(f"FAIL: {e}")
        else:
            print(f"OK: {path}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
