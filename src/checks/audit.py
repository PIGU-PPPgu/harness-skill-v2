#!/usr/bin/env python3
"""
harness audit — agent readability score (0-100)
移植自 agent-swarm-dev-v2/bin/harness:cmd_audit，改写为 Python
"""

import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Tuple


@dataclass
class AuditItem:
    label: str
    passed: bool
    points: int
    max_points: int
    detail: str = ""


@dataclass
class AuditReport:
    items: List[AuditItem] = field(default_factory=list)

    @property
    def score(self) -> int:
        return sum(i.points for i in self.items)

    @property
    def max_score(self) -> int:
        return sum(i.max_points for i in self.items)

    @property
    def passed(self) -> bool:
        return self.score >= 80


def run_audit(cwd: Path) -> AuditReport:
    report = AuditReport()

    # 1. Architecture docs (20pts)
    arch_dir = cwd / ".harness" / "docs" / "architecture"
    if not arch_dir.exists():
        arch_dir = cwd / "docs" / "architecture"
    has_arch = arch_dir.exists() and any(arch_dir.glob("*.md"))
    report.items.append(AuditItem(
        "Architecture documentation",
        has_arch, 20 if has_arch else 0, 20,
        str(arch_dir) if has_arch else f"Missing: {arch_dir}"
    ))

    # 2. Principles / golden rules (15pts)
    principles = (cwd / ".harness" / "docs" / "quality" / "standards.md").exists() or \
                 (cwd / "docs" / "principles.md").exists()
    report.items.append(AuditItem(
        "Principles / quality standards",
        principles, 15 if principles else 0, 15,
        "Found" if principles else "Missing docs/principles.md or .harness/docs/quality/standards.md"
    ))

    # 3. AGENTS.md (10pts)
    has_agents = (cwd / "AGENTS.md").exists()
    report.items.append(AuditItem(
        "AGENTS.md",
        has_agents, 10 if has_agents else 0, 10,
        "Found" if has_agents else "Missing AGENTS.md"
    ))

    # 4. CLAUDE.md (5pts — bonus for Claude Code users)
    has_claude = (cwd / "CLAUDE.md").exists()
    report.items.append(AuditItem(
        "CLAUDE.md",
        has_claude, 5 if has_claude else 0, 5,
        "Found" if has_claude else "Missing CLAUDE.md (optional, for Claude Code)"
    ))

    # 5. Active execution plans (15pts)
    plans_dir = cwd / ".harness" / "docs" / "plans" / "active"
    if not plans_dir.exists():
        plans_dir = cwd / "plans" / "active"
    plan_count = len(list(plans_dir.glob("*.json"))) + len(list(plans_dir.glob("*.md"))) \
        if plans_dir.exists() else 0
    has_plans = plan_count > 0
    report.items.append(AuditItem(
        "Active execution plans",
        has_plans, 15 if has_plans else 0, 15,
        f"{plan_count} plan(s) found" if has_plans else f"No plans in {plans_dir}"
    ))

    # 6. Test directory (20pts)
    test_dirs = ["tests", "test", "__tests__", "spec"]
    has_tests = any((cwd / d).exists() for d in test_dirs)
    report.items.append(AuditItem(
        "Test directory",
        has_tests, 20 if has_tests else 0, 20,
        "Found" if has_tests else f"No test directory ({', '.join(test_dirs)})"
    ))

    # 7. Linter config (10pts)
    lint_configs = [".eslintrc.js", ".eslintrc.json", "eslint.config.js",
                    ".ruff.toml", "pyproject.toml", ".golangci.yml"]
    has_lint = any((cwd / f).exists() for f in lint_configs)
    report.items.append(AuditItem(
        "Linter configuration",
        has_lint, 10 if has_lint else 0, 10,
        "Found" if has_lint else "No linter config found"
    ))

    # 8. CI/CD (5pts)
    has_ci = (cwd / ".github" / "workflows").exists()
    report.items.append(AuditItem(
        "CI/CD workflows",
        has_ci, 5 if has_ci else 0, 5,
        "Found .github/workflows/" if has_ci else "No .github/workflows/"
    ))

    return report


def print_audit(report: AuditReport, score_only: bool = False) -> None:
    if score_only:
        print(f"{report.score}/{report.max_score}")
        return

    print()
    for item in report.items:
        icon = "✓" if item.passed else "✗"
        pts = f"+{item.points}" if item.passed else f"  0/{item.max_points}"
        print(f"  {icon} {item.label:<35} {pts}")
        if not item.passed:
            print(f"      → {item.detail}")

    print()
    bar_filled = int(report.score / report.max_score * 20)
    bar = "█" * bar_filled + "░" * (20 - bar_filled)
    print(f"  Agent Readability Score: [{bar}] {report.score}/{report.max_score}")
    print()

    if report.score >= 80:
        print("  ✓ Excellent — highly readable for agents")
    elif report.score >= 60:
        print("  ⚠ Good — some improvements recommended")
    elif report.score >= 40:
        print("  ⚠ Fair — several improvements needed")
    else:
        print("  ✗ Poor — run 'harness init' to create missing structure")
    print()


if __name__ == "__main__":
    import sys
    score_only = "--score" in sys.argv
    report = run_audit(Path("."))
    print_audit(report, score_only)
    sys.exit(0 if report.passed else 1)
