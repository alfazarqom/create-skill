#!/usr/bin/env python3
"""Dependency-free static Skill validator and permission-gate simulation runner.

This validates repository structure/documentation and executes a deterministic
policy model. It does not load a native Agent Skill runtime or invoke Supabase.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "SKILL.md", "README.md", "CHANGELOG.md",
    "references/official-duitku-pop.md", "references/supabase-audit-scope.md",
    "workflows/documentation-audit.md", "workflows/supabase-audit.md",
    "workflows/staged-workflow.md", "workflows/edge-function-testing.md",
    "workflows/implementation-testing.md",
    "templates/audit-report.md", "templates/requirements-report.md",
    "templates/verification-report.md", "tests/acceptance-checklist.md",
    "tests/permission-gate-scenarios.json",
]
ERRORS: list[str] = []
CHECKS = 0


def check(condition: bool, message: str) -> None:
    global CHECKS
    CHECKS += 1
    if not condition:
        ERRORS.append(message)


def permission_decision(case: dict) -> str:
    """Return ALLOW/DENY for the documented permission gate model."""
    level = case.get("level")
    action = case.get("action")
    if level not in (0, 1, 2, 3) or not case.get("approved_scope", False):
        return "DENY"
    if action == "inspect":
        return "ALLOW" if level >= 0 else "DENY"
    if action == "invoke":
        if level == 0:
            return "DENY"
        if case.get("production") and not case.get("production_test_approved", False):
            return "DENY"
        if case.get("external_effect") and not case.get("external_effect_approved", False):
            return "DENY"
        if case.get("mutates_data"):
            return "ALLOW" if level >= 2 and case.get("isolated_test_data", False) else "DENY"
        return "ALLOW" if level >= 1 else "DENY"
    if action == "modify_source":
        return "ALLOW" if level == 3 and case.get("source_change_approved", False) else "DENY"
    if action == "deploy":
        return "ALLOW" if level == 3 and case.get("deployment_approved", False) else "DENY"
    return "DENY"


def main() -> int:
    for rel in REQUIRED_FILES:
        check((ROOT / rel).is_file(), f"Missing required file: {rel}")

    skill_path = ROOT / "SKILL.md"
    skill = skill_path.read_text(encoding="utf-8") if skill_path.exists() else ""
    frontmatter = re.match(r"\A---\s*\n(.*?)\n---\s*\n", skill, re.S)
    check(frontmatter is not None, "SKILL.md: YAML frontmatter block missing")
    if frontmatter:
        fm = frontmatter.group(1)
        check(bool(re.search(r"(?m)^name:\s*\S+", fm)), "SKILL.md: name field missing")
        check(bool(re.search(r"(?m)^description:\s*\S", fm)), "SKILL.md: description field missing")

    # Check local Markdown links and inline links. Ignore web URLs and mailto links.
    markdown_files = [p for p in ROOT.rglob("*.md") if ".git" not in p.parts]
    link_pattern = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
    for source in markdown_files:
        body = source.read_text(encoding="utf-8")
        for raw in link_pattern.findall(body):
            target = raw.strip().split()[0].strip("<>")
            if not target or target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0].split("?", 1)[0]
            if target:
                check((source.parent / target).resolve().is_file(),
                      f"{source.relative_to(ROOT)}: broken local link: {target}")

    edge = ROOT / "workflows/edge-function-testing.md"
    edge_text = edge.read_text(encoding="utf-8") if edge.exists() else ""
    for phrase in (
        "Level 1 is strictly non-mutating",
        "Level 2",
        "complete request path",
        "external effects",
        "does not make a mutating request Level 1",
    ):
        check(phrase.lower() in edge_text.lower(),
              f"Permission policy missing/unclear required phrase: {phrase}")

    scenario_path = ROOT / "tests/permission-gate-scenarios.json"
    scenarios_doc = {}
    if scenario_path.exists():
        try:
            scenarios_doc = json.loads(scenario_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            ERRORS.append(f"Invalid scenario JSON: {exc}")
    cases = scenarios_doc.get("scenarios", [])
    check(isinstance(cases, list) and len(cases) >= 10,
          "Permission scenario file must contain at least 10 scenarios")
    seen = set()
    for case in cases:
        case_id = case.get("id", "<missing-id>")
        check(case_id not in seen, f"Duplicate scenario id: {case_id}")
        seen.add(case_id)
        check(case.get("expected") in ("ALLOW", "DENY"),
              f"{case_id}: expected must be ALLOW or DENY")
        actual = permission_decision(case)
        check(actual == case.get("expected"),
              f"{case_id}: expected {case.get('expected')}, got {actual}")

    if ERRORS:
        print(f"FAIL: {len(ERRORS)} issue(s), {CHECKS} checks executed")
        for error in ERRORS:
            print(f"- {error}")
        return 1
    print(f"PASS: {CHECKS} checks; {len(REQUIRED_FILES)} required files; "
          f"{len(cases)} permission scenarios.")
    print("Scope: static Skill validation + simulated permission policy only.")
    print("Not tested: native Skill runtime, Supabase Edge Function invocation, "
          "database effects, Duitku Sandbox/Production.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
