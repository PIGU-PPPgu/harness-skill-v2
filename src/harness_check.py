#!/usr/bin/env python3
"""
harness check — 真实的仓库约束检查
运行 lint、类型检查、测试，输出结构化结果
"""

import json
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple


@dataclass
class CheckResult:
    name: str
    passed: bool
    output: str
    duration_ms: int
    command: str


@dataclass
class CheckReport:
    results: List[CheckResult] = field(default_factory=list)
    project_type: str = "generic"

    @property
    def passed(self) -> bool:
        return all(r.passed for r in self.results)

    @property
    def failed(self) -> List[CheckResult]:
        return [r for r in self.results if not r.passed]


def detect_project(cwd: Path) -> Tuple[str, dict]:
    """检测项目类型，返回 (type, commands)"""
    if (cwd / "package.json").exists():
        try:
            pkg = json.loads((cwd / "package.json").read_text())
        except Exception:
            pkg = {}
        deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
        scripts = pkg.get("scripts", {})

        # 确定测试命令
        if "vitest" in deps:
            test_cmd = ["npx", "vitest", "run"]
        elif "jest" in deps or "test" in scripts:
            test_cmd = ["npm", "test", "--", "--watchAll=false"]
        else:
            test_cmd = None

        # 确定 lint 命令
        if "lint" in scripts:
            lint_cmd = ["npm", "run", "lint"]
        elif "eslint" in deps:
            lint_cmd = ["npx", "eslint", "."]
        else:
            lint_cmd = None

        # 确定类型检查命令
        if "typescript" in deps or (cwd / "tsconfig.json").exists():
            tsc_cmd = ["npx", "tsc", "--noEmit"]
        else:
            tsc_cmd = None

        project_type = "nextjs" if "next" in deps else "node"
        return project_type, {
            "lint": lint_cmd,
            "typecheck": tsc_cmd,
            "test": test_cmd,
        }

    if (cwd / "pyproject.toml").exists() or (cwd / "setup.py").exists():
        lint_cmd = ["ruff", "check", "."] if _cmd_exists("ruff") else (
            ["flake8"] if _cmd_exists("flake8") else None
        )
        type_cmd = ["mypy", "."] if _cmd_exists("mypy") else None
        test_cmd = ["pytest"] if _cmd_exists("pytest") else None
        return "python", {"lint": lint_cmd, "typecheck": type_cmd, "test": test_cmd}

    if (cwd / "go.mod").exists():
        return "go", {
            "lint": ["go", "vet", "./..."],
            "typecheck": None,  # go vet covers this
            "test": ["go", "test", "./..."],
        }

    if (cwd / "Cargo.toml").exists():
        return "rust", {
            "lint": ["cargo", "clippy", "--", "-D", "warnings"],
            "typecheck": None,
            "test": ["cargo", "test"],
        }

    return "generic", {"lint": None, "typecheck": None, "test": None}


def _cmd_exists(cmd: str) -> bool:
    try:
        subprocess.run(["which", cmd], capture_output=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def run_check(name: str, cmd: List[str], timeout: int = 120) -> CheckResult:
    """运行单个检查，返回结果"""
    start = time.time()
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        duration_ms = int((time.time() - start) * 1000)
        passed = result.returncode == 0
        output = (result.stdout + result.stderr).strip()
        return CheckResult(
            name=name,
            passed=passed,
            output=output,
            duration_ms=duration_ms,
            command=" ".join(cmd),
        )
    except subprocess.TimeoutExpired:
        duration_ms = int((time.time() - start) * 1000)
        return CheckResult(
            name=name,
            passed=False,
            output=f"Timed out after {timeout}s",
            duration_ms=duration_ms,
            command=" ".join(cmd),
        )
    except FileNotFoundError:
        duration_ms = int((time.time() - start) * 1000)
        return CheckResult(
            name=name,
            passed=False,
            output=f"Command not found: {cmd[0]}",
            duration_ms=duration_ms,
            command=" ".join(cmd),
        )


def check_harness_docs(cwd: Path) -> CheckResult:
    """检查 harness 文档完整性"""
    start = time.time()
    missing = []
    required = [
        ".harness/docs/architecture/overview.md",
        ".harness/docs/product/requirements.md",
        ".harness/docs/quality/standards.md",
    ]
    placeholder_markers = ["<!-- TODO", "TODO:"]

    warnings = []
    for rel_path in required:
        p = cwd / rel_path
        if not p.exists():
            missing.append(rel_path)
        else:
            content = p.read_text()
            if any(m in content for m in placeholder_markers):
                warnings.append(f"{rel_path} still has TODO placeholders")

    duration_ms = int((time.time() - start) * 1000)
    if missing:
        return CheckResult(
            name="harness-docs",
            passed=False,
            output="Missing required docs:\n" + "\n".join(f"  - {m}" for m in missing),
            duration_ms=duration_ms,
            command="harness check docs",
        )

    output = "All required docs present"
    if warnings:
        output += "\nWarnings:\n" + "\n".join(f"  ⚠ {w}" for w in warnings)

    return CheckResult(
        name="harness-docs",
        passed=True,
        output=output,
        duration_ms=duration_ms,
        command="harness check docs",
    )


def run_all_checks(cwd: Path, skip: List[str] = None) -> CheckReport:
    """运行所有检查"""
    skip = skip or []
    project_type, commands = detect_project(cwd)
    report = CheckReport(project_type=project_type)

    checks = [
        ("harness-docs", None),   # special case
        ("lint", commands.get("lint")),
        ("typecheck", commands.get("typecheck")),
        ("test", commands.get("test")),
    ]

    for name, cmd in checks:
        if name in skip:
            continue

        if name == "harness-docs":
            result = check_harness_docs(cwd)
        elif cmd is None:
            continue
        else:
            result = run_check(name, cmd)

        report.results.append(result)

    return report


def print_report(report: CheckReport) -> None:
    """打印检查报告"""
    print(f"\nProject type: {report.project_type}")
    print(f"{'─' * 50}")

    for r in report.results:
        icon = "✓" if r.passed else "✗"
        status = "PASS" if r.passed else "FAIL"
        print(f"\n{icon} [{status}] {r.name}  ({r.duration_ms}ms)")
        print(f"  $ {r.command}")
        if not r.passed or (r.passed and r.output and "Warning" in r.output):
            # 只打印失败输出或警告，成功时保持安静
            for line in r.output.splitlines()[:20]:
                print(f"  {line}")
            if len(r.output.splitlines()) > 20:
                print(f"  ... ({len(r.output.splitlines()) - 20} more lines)")

    print(f"\n{'─' * 50}")
    total = len(report.results)
    passed = sum(1 for r in report.results if r.passed)
    print(f"Results: {passed}/{total} checks passed")

    if report.failed:
        print("\nFailed checks:")
        for r in report.failed:
            print(f"  ✗ {r.name}")
        print()


def main():
    import argparse
    parser = argparse.ArgumentParser(description="harness check — run repo quality checks")
    parser.add_argument("--skip", nargs="*", default=[], help="checks to skip")
    parser.add_argument("--json", action="store_true", help="output JSON report")
    parser.add_argument("--only", choices=["lint", "typecheck", "test", "harness-docs"],
                        help="run only one check")
    args = parser.parse_args()

    cwd = Path(".")
    skip = args.skip or []
    if args.only:
        # run only the specified check
        project_type, commands = detect_project(cwd)
        report = CheckReport(project_type=project_type)
        if args.only == "harness-docs":
            report.results.append(check_harness_docs(cwd))
        else:
            cmd = commands.get(args.only)
            if cmd:
                report.results.append(run_check(args.only, cmd))
            else:
                print(f"No {args.only} command detected for this project type")
                sys.exit(1)
    else:
        report = run_all_checks(cwd, skip=skip)

    if args.json:
        output = {
            "passed": report.passed,
            "project_type": report.project_type,
            "results": [
                {
                    "name": r.name,
                    "passed": r.passed,
                    "command": r.command,
                    "duration_ms": r.duration_ms,
                    "output": r.output,
                }
                for r in report.results
            ],
        }
        print(json.dumps(output, indent=2))
    else:
        print_report(report)

    sys.exit(0 if report.passed else 1)


if __name__ == "__main__":
    main()
