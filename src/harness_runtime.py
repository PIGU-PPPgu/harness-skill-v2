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

        # 创建配置文件
        config_file = self.harness_dir / "config.json"
        if not config_file.exists():
            config = {
                "version": "2.1.0",
                "model": {
                    "provider": "anthropic",
                    "model": "claude-3-5-sonnet-20241022",
                    "api_key_env": "ANTHROPIC_API_KEY"
                },
                "git": {
                    "main_branch": "main",
                    "pr_template": ".harness/templates/pr_template.md"
                },
                "quality": {
                    "min_coverage": 80,
                    "lint_on_commit": True,
                    "type_check": True
                }
            }
            config_file.write_text(json.dumps(config, indent=2))

        # 创建入口文档
        readme = self.docs_dir / "README.md"
        if not readme.exists():
            readme.write_text("""# Repository Documentation

## Quick Links
- [Architecture](architecture/) - System design and technical decisions
- [Product](product/) - Product requirements and specifications
- [Quality](quality/) - Quality standards and testing strategy
- [Security](security/) - Security requirements and guidelines
- [Plans](plans/) - Execution plans (active and completed)

## How to Use
This documentation is structured for AI agents to quickly understand the codebase.
Keep it concise, up-to-date, and focused on what agents need to know.
""")

        print("✓ Harness structure initialized")
        print(f"  - Documentation: {self.docs_dir}")
        print(f"  - Plans: {self.plans_dir}")
        print(f"  - Config: {config_file}")

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
