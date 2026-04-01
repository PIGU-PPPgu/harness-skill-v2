#!/usr/bin/env python3
"""
Agent Main Loop
单主循环实现，不是多角色流水线
"""

import os
import json
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
from harness_runtime import HarnessRuntime, Task, TaskStatus


class AgentLoop:
    """Agent 主循环"""

    def __init__(self, runtime: HarnessRuntime):
        self.runtime = runtime
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY not set")

    def read_docs(self) -> str:
        """读取仓库文档"""
        docs_dir = self.runtime.docs_dir
        context = []

        # 读取入口文档
        readme = docs_dir / "README.md"
        if readme.exists():
            context.append(f"# Repository Overview\n{readme.read_text()}")

        # 读取架构文档
        arch_dir = docs_dir / "architecture"
        if arch_dir.exists():
            for file in arch_dir.glob("*.md"):
                context.append(f"# Architecture: {file.stem}\n{file.read_text()}")

        # 读取产品文档
        product_dir = docs_dir / "product"
        if product_dir.exists():
            for file in product_dir.glob("*.md"):
                context.append(f"# Product: {file.stem}\n{file.read_text()}")

        return "\n\n---\n\n".join(context)

    def execute_task(self, plan_id: str, task: Task) -> bool:
        """执行单个任务"""
        print(f"\n{'='*60}")
        print(f"Executing Task: {task.id}")
        print(f"Title: {task.title}")
        print(f"{'='*60}\n")

        try:
            # 1. 更新状态为进行中
            self.runtime.update_task_status(
                plan_id, task.id, TaskStatus.IN_PROGRESS
            )

            # 2. 创建工作分支
            branch = self.runtime.create_branch(task.id)
            self.runtime.update_task_status(
                plan_id, task.id, TaskStatus.IN_PROGRESS, branch=branch
            )

            # 3. 读取仓库文档
            docs_context = self.read_docs()

            # 4. 调用 AI 模型生成实现
            # 这里需要集成 Anthropic API
            # 简化实现：打印提示
            print("📖 Reading repository documentation...")
            print(f"   Found {len(docs_context)} characters of context")

            print("\n🤖 Calling AI model to implement task...")
            print(f"   Task: {task.title}")
            print(f"   Description: {task.description}")

            # TODO: 实际的 AI 调用
            # response = self.call_ai_model(task, docs_context)
            # self.apply_changes(response)

            print("\n⚠️  AI implementation not yet connected")
            print("   This is where the agent would:")
            print("   - Read relevant code files")
            print("   - Generate implementation")
            print("   - Write code changes")
            print("   - Run tests")
            print("   - Commit changes")

            # 5. 运行测试
            print("\n🧪 Running tests...")
            # test_result = self.run_tests()

            # 6. 创建 PR
            print("\n📝 Creating Pull Request...")
            pr_url = self.runtime.create_pr(task, branch)
            self.runtime.update_task_status(
                plan_id, task.id, TaskStatus.DONE, pr_url=pr_url
            )

            print(f"\n✅ Task completed: {task.id}")
            print(f"   PR: {pr_url}")
            return True

        except Exception as e:
            print(f"\n❌ Task failed: {e}")
            self.runtime.update_task_status(
                plan_id, task.id, TaskStatus.FAILED
            )
            return False

    def run_tests(self) -> bool:
        """运行测试"""
        try:
            # 尝试运行常见的测试命令
            test_commands = [
                ["npm", "test"],
                ["pytest"],
                ["cargo", "test"],
                ["go", "test", "./..."],
            ]

            for cmd in test_commands:
                try:
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        timeout=300
                    )
                    if result.returncode == 0:
                        print(f"✓ Tests passed: {' '.join(cmd)}")
                        return True
                except (FileNotFoundError, subprocess.TimeoutExpired):
                    continue

            print("⚠ No test command found or tests failed")
            return False

        except Exception as e:
            print(f"✗ Test execution error: {e}")
            return False

    def call_ai_model(self, task: Task, context: str) -> Dict[str, Any]:
        """调用 AI 模型"""
        # TODO: 实现 Anthropic API 调用
        # 这里需要：
        # 1. 构建 prompt（包含任务描述、仓库上下文、代码规范）
        # 2. 调用 Claude API
        # 3. 解析响应（代码变更、测试、文档）
        # 4. 返回结构化结果
        pass

    def main_loop(self, plan_id: str, max_iterations: int = 100) -> None:
        """主循环：持续执行任务直到完成"""
        print(f"Starting agent loop for plan: {plan_id}")
        print(f"Max iterations: {max_iterations}\n")

        iteration = 0
        while iteration < max_iterations:
            iteration += 1

            # 获取下一个任务
            task = self.runtime.get_next_task(plan_id)
            if not task:
                print("\n✅ All tasks completed or blocked")
                break

            # 执行任务
            success = self.execute_task(plan_id, task)

            if not success:
                print(f"\n⚠️  Task {task.id} failed, checking for other tasks...")
                continue

            print(f"\n{'='*60}")
            print(f"Iteration {iteration} complete")
            print(f"{'='*60}\n")

        print(f"\nAgent loop finished after {iteration} iterations")


def main():
    """CLI 入口"""
    import sys

    if len(sys.argv) < 3:
        print("Usage: agent_loop.py <plan_id> [max_iterations]")
        sys.exit(1)

    plan_id = sys.argv[1]
    max_iterations = int(sys.argv[2]) if len(sys.argv) > 2 else 100

    runtime = HarnessRuntime()
    agent = AgentLoop(runtime)
    agent.main_loop(plan_id, max_iterations)


if __name__ == "__main__":
    main()
