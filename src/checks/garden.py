#!/usr/bin/env python3
"""
harness garden — 文档卫生 + 代码重复检查
移植自 agent-swarm-dev-v2/bin/harness:cmd_garden
"""

import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class GardenIssue:
    category: str
    severity: str  # "warn" | "error"
    message: str
    file: str = ""


@dataclass
class GardenReport:
    issues: List[GardenIssue] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        # warn issues still count as failures — garden is a blocking check
        return len(self.issues) == 0


def check_docs(cwd: Path, report: GardenReport) -> None:
    docs_dirs = [cwd / ".harness" / "docs", cwd / "docs"]
    md_files = []
    for d in docs_dirs:
        if d.exists():
            md_files.extend(d.rglob("*.md"))

    if not md_files:
        return

    # 过期文档（90天未更新）
    stale = []
    now = time.time()
    for f in md_files:
        age_days = (now - f.stat().st_mtime) / 86400
        if age_days > 90:
            stale.append((f, int(age_days)))

    if stale:
        for f, days in stale:
            report.issues.append(GardenIssue(
                "docs", "warn",
                f"Not updated in {days} days",
                str(f.relative_to(cwd))
            ))
    else:
        print("  ✓ All docs updated within 90 days")

    # TODO 占位符
    todo_files = []
    for f in md_files:
        try:
            content = f.read_text()
            if "<!-- TODO" in content or "\nTODO:" in content:
                todo_files.append(f)
        except Exception:
            pass

    if todo_files:
        for f in todo_files:
            report.issues.append(GardenIssue(
                "docs", "warn",
                "Contains TODO placeholders — fill in or remove",
                str(f.relative_to(cwd))
            ))
    else:
        print("  ✓ No TODO placeholders in docs")


def check_code(cwd: Path, report: GardenReport) -> None:
    src_dir = cwd / "src"
    if not src_dir.exists():
        return

    # 重复工具函数
    dup_patterns = ["debounce", "throttle", "formatDate", "parseJSON", "sleep"]
    for pattern in dup_patterns:
        try:
            result = subprocess.run(
                ["grep", "-r", f"^function {pattern}", str(src_dir)],
                capture_output=True, text=True
            )
            matches = [l for l in result.stdout.splitlines() if l.strip()]
            if len(matches) > 1:
                report.issues.append(GardenIssue(
                    "code", "warn",
                    f"Duplicate '{pattern}' function found in {len(matches)} files — extract to shared utils",
                    matches[0].split(":")[0]
                ))
        except Exception:
            pass

    # 未验证的 API 响应
    try:
        result = subprocess.run(
            ["grep", "-r", "--include=*.ts", "--include=*.js", r"\.json()", str(src_dir)],
            capture_output=True, text=True
        )
        unvalidated = [l for l in result.stdout.splitlines()
                       if "parse" not in l and "validate" not in l and "schema" not in l]
        if unvalidated:
            report.issues.append(GardenIssue(
                "code", "warn",
                f"{len(unvalidated)} unvalidated .json() calls — consider Zod schemas",
                ""
            ))
        else:
            print("  ✓ No obvious unvalidated API responses")
    except Exception:
        pass

    # 大文件
    large = []
    for ext in ["*.ts", "*.js", "*.py"]:
        for f in src_dir.rglob(ext):
            try:
                lines = len(f.read_text().splitlines())
                if lines > 500:
                    large.append((f, lines))
            except Exception:
                pass

    if large:
        for f, lines in large:
            report.issues.append(GardenIssue(
                "code", "warn",
                f"{lines} lines — consider splitting",
                str(f.relative_to(cwd))
            ))
    else:
        print("  ✓ No files over 500 lines")


def run_garden(cwd: Path, mode: str = "all") -> GardenReport:
    report = GardenReport()

    if mode in ("all", "docs"):
        print("\n  Scanning documentation...")
        check_docs(cwd, report)

    if mode in ("all", "code"):
        print("\n  Scanning code...")
        check_code(cwd, report)

    return report


def print_garden(report: GardenReport) -> None:
    if report.issues:
        print()
        for issue in report.issues:
            icon = "⚠" if issue.severity == "warn" else "✗"
            loc = f"  ({issue.file})" if issue.file else ""
            print(f"  {icon} [{issue.category}] {issue.message}{loc}")
        print(f"\n  {len(report.issues)} issue(s) found — consider opening PRs to fix")
    else:
        print("\n  ✓ Garden clean — no issues found")
    print()


if __name__ == "__main__":
    import sys
    mode = "all"
    if "--docs-only" in sys.argv:
        mode = "docs"
    elif "--code-only" in sys.argv:
        mode = "code"

    report = run_garden(Path("."), mode)
    print_garden(report)
    sys.exit(0 if report.passed else 1)
