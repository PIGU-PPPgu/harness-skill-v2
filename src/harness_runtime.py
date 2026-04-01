#!/usr/bin/env python3
"""
Harness Engineering Runtime
真正的 agent-first 仓库 harness 实现
"""

import json
import os
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Optional, List, Dict, Any


class TaskStatus(Enum):
    """任务状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    DONE = "done"
    FAILED = "failed"


@dataclass
class Task:
    """任务定义"""
    id: str
    title: str
    description: str
    status: TaskStatus
    created_at: str
    updated_at: str
    dependencies: List[str]
    assignee: Optional[str] = None
    branch: Optional[str] = None
    pr_url: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['status'] = self.status.value
        return data


@dataclass
class ExecutionPlan:
    """执行计划"""
    id: str
    title: str
    description: str
    tasks: List[Task]
    created_at: str
    updated_at: str
    status: str

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['tasks'] = [t.to_dict() for t in self.tasks]
        return data


class HarnessRuntime:
    """Harness 运行时核心"""

    def __init__(self, harness_dir: str = ".harness"):
        self.harness_dir = Path(harness_dir)
        self.docs_dir = self.harness_dir / "docs"
        self.plans_dir = self.docs_dir / "plans"
        self.state_file = self.harness_dir / "state.json"

    def initialize(self) -> None:
        """初始化项目结构"""
        # 创建目录结构
        dirs = [
            self.docs_dir / "architecture",
            self.docs_dir / "product",
            self.docs_dir / "quality",
            self.docs_dir / "security",
            self.plans_dir / "active",
            self.plans_dir / "completed",
            self.harness_dir / "constraints",
            self.harness_dir / "logs",
        ]
        for dir_path in dirs:
            dir_path.mkdir(parents=True, exist_ok=True)

        # 检测项目类型
        project_type = self._detect_project_type()

        # 创建配置文件
        config_file = self.harness_dir / "config.json"
        if not config_file.exists():
            config = {
                "version": "2.1.0",
                "project_type": project_type,
                "git": {"main_branch": "main"},
                "quality": {
                    "min_coverage": 80,
                    "lint_on_commit": True,
                    "type_check": True
                }
            }
            config_file.write_text(json.dumps(config, indent=2))

        # 生成所有模板文件
        self._write_if_missing(Path("CLAUDE.md"), self._tmpl_claude_md())
        self._write_if_missing(Path("AGENTS.md"), self._tmpl_agents_md())
        self._write_if_missing(self.docs_dir / "README.md", self._tmpl_docs_readme())
        self._write_if_missing(self.docs_dir / "architecture" / "overview.md", self._tmpl_architecture())
        self._write_if_missing(self.docs_dir / "product" / "requirements.md", self._tmpl_product())
        self._write_if_missing(self.docs_dir / "quality" / "standards.md", self._tmpl_quality(project_type))
        self._write_if_missing(self.docs_dir / "security" / "guidelines.md", self._tmpl_security())

        print("✓ Harness initialized")
        print()
        print("Generated files:")
        print("  CLAUDE.md          ← Claude Code entry point")
        print("  AGENTS.md          ← Codex / OpenAI entry point")
        print("  .harness/docs/     ← Structured knowledge system")
        print("    architecture/    ← Fill in your system design")
        print("    product/         ← Fill in your requirements")
        print("    quality/         ← Pre-filled with standards")
        print("    security/        ← Pre-filled with guidelines")
        print("    plans/active/    ← Execution plans go here")
        print()
        print("Next steps:")
        print("  1. Edit CLAUDE.md and AGENTS.md with your project specifics")
        print("  2. Fill in .harness/docs/architecture/overview.md")
        print("  3. Write your first requirement in .harness/docs/product/requirements.md")
        print("  4. Run: harness plan create '<title>' '<description>'")

    def _detect_project_type(self) -> str:
        """检测项目类型"""
        cwd = Path(".")
        if (cwd / "package.json").exists():
            pkg = json.loads((cwd / "package.json").read_text())
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if "next" in deps:
                return "nextjs"
            if "react" in deps:
                return "react"
            return "node"
        if (cwd / "pyproject.toml").exists() or (cwd / "setup.py").exists():
            return "python"
        if (cwd / "go.mod").exists():
            return "go"
        if (cwd / "Cargo.toml").exists():
            return "rust"
        return "generic"

    def _write_if_missing(self, path: Path, content: str) -> None:
        if not path.exists():
            path.write_text(content)

    def _tmpl_claude_md(self) -> str:
        return """# CLAUDE.md — Agent Entry Point

> This file is auto-loaded by Claude Code. Keep it concise and up-to-date.

## Repository Overview

<!-- TODO: 1-2 sentences describing what this repo does -->

## Tech Stack

<!-- TODO: List main technologies, e.g.:
- Runtime: Node.js 20 / Python 3.12 / Go 1.22
- Framework: Next.js 14 / FastAPI / Gin
- Database: PostgreSQL via Supabase
- Testing: Vitest / pytest / go test
-->

## How to Run

```bash
# Install dependencies
# TODO: e.g. npm install / pip install -e . / go mod download

# Start dev server
# TODO: e.g. npm run dev / uvicorn main:app --reload

# Run tests
# TODO: e.g. npm test / pytest / go test ./...

# Lint
# TODO: e.g. npm run lint / ruff check . / golangci-lint run
```

## Architecture

See `.harness/docs/architecture/overview.md` for full details.

Key constraint: <!-- TODO: e.g. "Never import from ui/ into service/" -->

## Active Work

See `.harness/docs/plans/active/` for current execution plans.

## Agent Guidelines

- Read `.harness/docs/` before starting any task
- Create a branch per task: `harness/<plan-id>-<task-id>`
- Run tests before creating a PR
- If blocked or uncertain about architecture decisions, stop and ask the human
- Update `.harness/docs/plans/active/<plan>.json` task status as you work
"""

    def _tmpl_agents_md(self) -> str:
        return """# AGENTS.md — Agent Entry Point (Codex / OpenAI)

> This file is the entry point for OpenAI Codex and other agents.

## What This Repo Does

<!-- TODO: 1-2 sentences -->

## Setup

```bash
# TODO: commands to install and run
```

## Testing

```bash
# TODO: command to run tests
# All tests must pass before submitting a PR
```

## Code Style

<!-- TODO: key conventions, e.g.:
- Use TypeScript strict mode
- No `any` types
- Functions under 50 lines
-->

## Repository Knowledge

Structured documentation lives in `.harness/docs/`:
- `architecture/overview.md` — system design
- `product/requirements.md` — what we're building
- `quality/standards.md` — quality bar
- `plans/active/` — current execution plans (JSON)

## Constraints

<!-- TODO: hard rules the agent must not violate, e.g.:
- Never commit secrets or API keys
- Never modify migration files directly
- Always add tests for new functionality
-->

## When to Stop and Ask

- Architecture decisions that affect multiple modules
- Security-sensitive changes
- Anything that requires production access
"""

    def _tmpl_docs_readme(self) -> str:
        return """# Repository Documentation

This directory is the structured knowledge system for AI agents.
Keep it concise, accurate, and up-to-date.

## Contents

| Directory | Purpose |
|-----------|---------|
| `architecture/` | System design, data models, dependency rules |
| `product/` | Requirements, acceptance criteria, user stories |
| `quality/` | Testing strategy, coverage requirements, lint rules |
| `security/` | Auth model, data handling, threat model |
| `plans/active/` | Current execution plans (JSON) |
| `plans/completed/` | Finished execution plans (for reference) |

## Maintenance

- Update `architecture/overview.md` after any structural change
- Move plans from `active/` to `completed/` when done
- Keep each file under 200 lines — link out rather than inline
"""

    def _tmpl_architecture(self) -> str:
        return """# Architecture Overview

<!-- TODO: Fill this in. This is the most important file for agents. -->

## System Diagram

```
<!-- ASCII diagram of your system -->
```

## Key Components

| Component | Responsibility | Location |
|-----------|---------------|----------|
| <!-- TODO --> | | |

## Data Model

<!-- TODO: Key entities and their relationships -->

## Dependency Rules

<!-- TODO: What can import what? e.g.:
- `ui/` can import from `services/` and `types/`
- `services/` cannot import from `ui/`
- No circular dependencies
-->

## Key Decisions

<!-- TODO: Important architectural decisions and why they were made -->
"""

    def _tmpl_product(self) -> str:
        return """# Product Requirements

<!-- TODO: Fill in your current requirements -->

## Current Goals

<!-- What are we building right now? -->

## Acceptance Criteria

<!-- What does "done" look like? Be specific and testable.
- [ ] Criterion 1
- [ ] Criterion 2
-->

## Out of Scope

<!-- What are we explicitly NOT doing? -->

## User Stories

<!-- Optional: who uses this and what do they need? -->
"""

    def _tmpl_quality(self, project_type: str) -> str:
        test_cmd = {
            "nextjs": "npm test -- --run",
            "react": "npm test -- --run",
            "node": "npm test",
            "python": "pytest",
            "go": "go test ./...",
            "rust": "cargo test",
        }.get(project_type, "# TODO: add test command")

        lint_cmd = {
            "nextjs": "npm run lint",
            "react": "npm run lint",
            "node": "npm run lint",
            "python": "ruff check .",
            "go": "golangci-lint run",
            "rust": "cargo clippy",
        }.get(project_type, "# TODO: add lint command")

        return f"""# Quality Standards

## Test Command

```bash
{test_cmd}
```

## Lint Command

```bash
{lint_cmd}
```

## Requirements

- Minimum test coverage: 80%
- All tests must pass before PR
- No lint errors
- No type errors (if applicable)

## Test Strategy

- Unit tests for pure functions and business logic
- Integration tests for API endpoints
- Do NOT mock the database in integration tests

## Definition of Done

A task is done when:
1. Feature works as described in acceptance criteria
2. Tests written and passing
3. No new lint errors
4. PR created with description of changes
"""

    def _tmpl_security(self) -> str:
        return """# Security Guidelines

## Authentication

<!-- TODO: How does auth work in this system? -->

## Data Handling

- Never log sensitive data (passwords, tokens, PII)
- Validate all user input at system boundaries
- Use parameterized queries (no string interpolation in SQL)

## Secrets

- Never commit secrets or API keys
- Use environment variables for all credentials
- See `.env.example` for required variables

## Agent Constraints

- Agents must not access production databases directly
- Agents must not modify auth/security code without human review
- Any change to permission models requires human approval
"""

    def create_plan(self, title: str, description: str) -> ExecutionPlan:
        """创建执行计划"""
        plan_id = f"EP-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        now = datetime.now().isoformat()

        plan = ExecutionPlan(
            id=plan_id,
            title=title,
            description=description,
            tasks=[],
            created_at=now,
            updated_at=now,
            status="active"
        )

        # 保存计划
        plan_file = self.plans_dir / "active" / f"{plan_id}.json"
        plan_file.write_text(json.dumps(plan.to_dict(), indent=2))

        print(f"✓ Created execution plan: {plan_id}")
        return plan

    def add_task(self, plan_id: str, title: str, description: str,
                 dependencies: List[str] = None) -> Task:
        """添加任务到执行计划"""
        plan_file = self.plans_dir / "active" / f"{plan_id}.json"
        if not plan_file.exists():
            raise ValueError(f"Plan {plan_id} not found")

        plan_data = json.loads(plan_file.read_text())

        # 生成任务 ID
        task_count = len(plan_data['tasks'])
        task_id = f"{plan_id}-T{task_count + 1:03d}"
        now = datetime.now().isoformat()

        task = Task(
            id=task_id,
            title=title,
            description=description,
            status=TaskStatus.PENDING,
            created_at=now,
            updated_at=now,
            dependencies=dependencies or []
        )

        plan_data['tasks'].append(task.to_dict())
        plan_data['updated_at'] = now
        plan_file.write_text(json.dumps(plan_data, indent=2))

        print(f"✓ Added task: {task_id}")
        return task

    def get_next_task(self, plan_id: str) -> Optional[Task]:
        """获取下一个可执行的任务"""
        plan_file = self.plans_dir / "active" / f"{plan_id}.json"
        if not plan_file.exists():
            return None

        plan_data = json.loads(plan_file.read_text())
        completed_tasks = {
            t['id'] for t in plan_data['tasks']
            if t['status'] == TaskStatus.DONE.value
        }

        for task_data in plan_data['tasks']:
            if task_data['status'] != TaskStatus.PENDING.value:
                continue

            # 检查依赖是否完成
            deps = set(task_data.get('dependencies', []))
            if deps.issubset(completed_tasks):
                return Task(
                    id=task_data['id'],
                    title=task_data['title'],
                    description=task_data['description'],
                    status=TaskStatus(task_data['status']),
                    created_at=task_data['created_at'],
                    updated_at=task_data['updated_at'],
                    dependencies=task_data['dependencies'],
                    assignee=task_data.get('assignee'),
                    branch=task_data.get('branch'),
                    pr_url=task_data.get('pr_url')
                )

        return None

    def update_task_status(self, plan_id: str, task_id: str,
                          status: TaskStatus, **kwargs) -> None:
        """更新任务状态"""
        plan_file = self.plans_dir / "active" / f"{plan_id}.json"
        if not plan_file.exists():
            raise ValueError(f"Plan {plan_id} not found")

        plan_data = json.loads(plan_file.read_text())

        for task in plan_data['tasks']:
            if task['id'] == task_id:
                task['status'] = status.value
                task['updated_at'] = datetime.now().isoformat()
                for key, value in kwargs.items():
                    task[key] = value
                break

        plan_file.write_text(json.dumps(plan_data, indent=2))
        print(f"✓ Updated task {task_id}: {status.value}")

    def create_branch(self, task_id: str) -> str:
        """为任务创建 Git 分支"""
        branch_name = f"harness/{task_id.lower()}"

        try:
            subprocess.run(
                ["git", "checkout", "-b", branch_name],
                check=True,
                capture_output=True
            )
            print(f"✓ Created branch: {branch_name}")
            return branch_name
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to create branch: {e.stderr.decode()}")
            raise

    def create_pr(self, task: Task, branch: str) -> str:
        """创建 Pull Request"""
        # 这里需要集成 gh CLI 或 GitHub API
        # 简化实现：返回模拟 URL
        pr_title = f"[{task.id}] {task.title}"
        pr_body = f"""## Task
{task.description}

## Changes
<!-- Describe what changed -->

## Testing
<!-- How was this tested? -->

---
*Generated by Harness Engineering*
"""

        try:
            # 使用 gh CLI 创建 PR
            result = subprocess.run(
                ["gh", "pr", "create", "--title", pr_title, "--body", pr_body],
                check=True,
                capture_output=True,
                text=True
            )
            pr_url = result.stdout.strip()
            print(f"✓ Created PR: {pr_url}")
            return pr_url
        except subprocess.CalledProcessError:
            # 如果 gh CLI 不可用，返回占位符
            pr_url = f"https://github.com/owner/repo/pull/placeholder"
            print(f"⚠ gh CLI not available, PR creation skipped")
            return pr_url


def main():
    """CLI 入口"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: harness_runtime.py <command>")
        sys.exit(1)

    runtime = HarnessRuntime()
    command = sys.argv[1]

    if command == "init":
        runtime.initialize()
    elif command == "create-plan":
        if len(sys.argv) < 4:
            print("Usage: harness_runtime.py create-plan <title> <description>")
            sys.exit(1)
        plan = runtime.create_plan(sys.argv[2], sys.argv[3])
        print(f"Plan ID: {plan.id}")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
