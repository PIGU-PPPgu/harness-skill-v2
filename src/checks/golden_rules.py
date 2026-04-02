#!/usr/bin/env python3
"""
harness golden-rules — 代码模式检查
移植自 agent-swarm-dev-v2/bin/harness:cmd_golden_rules
"""

import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class Violation:
    rule: str
    message: str
    fix: str
    file: str = ""
    line: str = ""


@dataclass
class GoldenRulesReport:
    violations: List[Violation] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return len(self.violations) == 0


def _grep(pattern: str, path: Path, include: List[str] = None) -> List[str]:
    cmd = ["grep", "-r", pattern, str(path)]
    if include:
        for ext in include:
            cmd += ["--include", ext]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        return [l for l in result.stdout.splitlines() if l.strip()]
    except Exception:
        return []


def run_golden_rules(cwd: Path) -> GoldenRulesReport:
    report = GoldenRulesReport()
    src = cwd / "src"

    if not src.exists():
        print("  ⚠ No src/ directory — skipping code checks")
        return report

    # Rule 1: 重复工具函数
    dup_fns = ["debounce", "throttle", "formatDate", "parseJSON", "sleep", "clamp"]
    for fn in dup_fns:
        matches = _grep(f"^function {fn}", src)
        if len(matches) > 1:
            report.violations.append(Violation(
                "shared-utilities",
                f"'{fn}' defined in {len(matches)} places",
                "Extract to src/utils/ shared package",
                matches[0].split(":")[0]
            ))

    if not any(v.rule == "shared-utilities" for v in report.violations):
        print("  ✓ No duplicate utility functions")

    # Rule 2: 未验证的 API 边界
    unvalidated = _grep(r"\.json()", src, ["*.ts", "*.js"])
    unvalidated = [l for l in unvalidated
                   if "parse" not in l and "validate" not in l and "schema" not in l]
    if unvalidated:
        report.violations.append(Violation(
            "boundary-validation",
            f"{len(unvalidated)} unvalidated .json() call(s)",
            "Use Zod / io-ts / pydantic schemas at API boundaries",
            unvalidated[0].split(":")[0]
        ))
    else:
        print("  ✓ API boundaries appear validated")

    # Rule 3: 手写 API 请求（应该用生成的 SDK）
    manual = _grep(r"axios\.post\|fetch(", src, ["*.ts", "*.js"])
    if len(manual) > 5:
        report.violations.append(Violation(
            "typed-sdks",
            f"{len(manual)} manual API calls — consider generated client",
            "Generate API client from OpenAPI spec",
        ))
    else:
        print("  ✓ API call count looks reasonable")

    # Rule 4: 魔法数字（timeout/interval 里的硬编码数字）
    magic = _grep(r"setTimeout\|setInterval", src, ["*.ts", "*.js", "*.py"])
    magic = [l for l in magic if any(c.isdigit() for c in l.split("(")[-1][:10])]
    if magic:
        report.violations.append(Violation(
            "no-magic-numbers",
            f"{len(magic)} hardcoded timeout/interval value(s)",
            "Extract to named constants (e.g. RETRY_DELAY_MS = 1000)",
            magic[0].split(":")[0]
        ))
    else:
        print("  ✓ No obvious magic numbers in timers")

    return report


def print_golden_rules(report: GoldenRulesReport) -> None:
    if report.violations:
        print()
        for v in report.violations:
            loc = f"  ({v.file})" if v.file else ""
            print(f"  ✗ [{v.rule}] {v.message}{loc}")
            print(f"      → {v.fix}")
        print(f"\n  {len(report.violations)} golden rule violation(s)")
    else:
        print("\n  ✓ All golden rules pass")
    print()


if __name__ == "__main__":
    import sys
    report = run_golden_rules(Path("."))
    print_golden_rules(report)
    sys.exit(0 if report.passed else 1)
