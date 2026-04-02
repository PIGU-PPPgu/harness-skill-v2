# Harness Engineering

> 把你的仓库改造成 AI agent 可以持续、高效工作的环境

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 这是什么

你有没有遇到这种情况：把任务丢给 Claude Code 或 Codex，它写了一堆代码，但因为不了解你的仓库结构、不知道你的架构约束、不清楚当前在做什么，写出来的东西偏了方向，或者需要大量反复纠正？

**Harness Engineering** 解决的就是这个问题。

它不是一个 AI agent——Claude Code 和 Codex 本身就是 agent，而且比任何自制方案都强。它做的是**把你的仓库改造成 agent 友好的环境**：

- 生成结构化的 `CLAUDE.md` / `AGENTS.md` 入口文件，让 agent 一进来就理解仓库
- 建立标准化的文档骨架（架构、产品需求、质量标准、安全规范）
- 提供执行计划管理，让 agent 知道当前在做什么、做到哪了
- 提供真实的质量检查命令（不是打印假输出），在 PR 前机械化验收

基于 [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/)（2026-02-11）方法论。

---

## 核心理念

**"Humans steer. Agents execute."**

| 人类负责 | Agent 负责 |
|---------|-----------|
| 目标和验收标准 | 读文档理解仓库 |
| 架构决策 | 写代码、跑测试 |
| 安全审查 | 开 PR、响应 review |
| 最终合并 | 根据反馈修改 |

---

## 快速开始

```bash
# 安装
curl -fsSL https://raw.githubusercontent.com/PIGU-PPPgu/harness-skill-v2/main/install.sh | bash

# 在你的项目里初始化
cd your-project
harness init
```

`harness init` 会生成：

```
your-project/
├── CLAUDE.md                    ← Claude Code 自动读取的入口文件
├── AGENTS.md                    ← Codex / 其他 agent 的入口文件
└── .harness/
    ├── config.json              ← 项目配置（自动检测 Node/Python/Go/Rust）
    └── docs/
        ├── architecture/        ← 系统架构文档
        ├── product/             ← 产品需求
        ├── quality/             ← 质量标准（已预填测试和 lint 命令）
        ├── security/            ← 安全规范
        └── plans/active/        ← 执行计划（JSON + 任务状态机）
```

然后填写关键文档，让 agent 真正理解你的仓库，直接用 Claude Code 或 Codex 开始工作。

---

## 工作流

```
1. harness init              生成文档骨架
        ↓
2. 填写文档                  描述架构、需求、约束
        ↓
3. harness plan create       创建执行计划
   harness plan task add     拆分任务，设置依赖关系
        ↓
4. claude / codex            Agent 读文档、认领任务、写代码、开 PR
        ↓
5. harness check             验收（lint + test + 文档完整性）
   harness audit             检查 agent readability 评分
        ↓
6. 人类 review 并合并
```

---

## 命令参考

### 初始化

```bash
harness init
```

自动检测项目类型（Next.js / Node / Python / Go / Rust），生成对应的文档骨架和质量标准。

### 执行计划

```bash
# 创建计划
harness plan create "实现用户认证" "添加 JWT 认证，保护 API 接口"
# → Created execution plan: EP-20260401-120000

# 添加任务（可选：指定依赖）
harness plan task add EP-20260401-120000 "设计数据库 schema" "users 表，tokens 表"
# → Task ID: EP-20260401-120000-T001

harness plan task add EP-20260401-120000 "实现 JWT 签发" "登录接口" EP-20260401-120000-T001
# → Task ID: EP-20260401-120000-T002（依赖 T001 完成后才可认领）

# 查看计划
harness plan list
# → Active plans:
#   EP-20260401-120000  [0/2]  实现用户认证
```

### 质量检查

```bash
harness check                    # lint + typecheck + test + 文档完整性
harness check --only test        # 只跑测试
harness check --only lint        # 只跑 lint
harness check --json             # JSON 输出（适合 CI）
```

示例输出：
```
Project type: nextjs
──────────────────────────────────────────────────

✓ [PASS] harness-docs  (2ms)
✓ [PASS] lint  (1843ms)
✗ [FAIL] test  (4201ms)
  $ npx vitest run
  FAIL src/auth.test.ts
    ✗ should return 401 for invalid token

Results: 2/3 checks passed
```

### Agent Readability 审计

```bash
harness audit
```

```
  ✓ Architecture documentation          +20
  ✓ Principles / quality standards      +15
  ✓ AGENTS.md                           +10
  ✓ CLAUDE.md                           +5
  ✗ Active execution plans                0/15
  ✓ Test directory                       +20
  ✓ Linter configuration                 +10
  ✗ CI/CD workflows                       0/5

  Agent Readability Score: [███████████████░░░░░] 80/100

  ✓ Excellent — highly readable for agents
```

### 代码卫生

```bash
harness garden               # 文档过期检查 + 代码重复检测
harness garden --docs-only   # 只检查文档
harness golden-rules         # 代码模式检查（重复工具函数、未验证 API、魔法数字）
```

---

## 多 Agent 并行

`harness init` 生成的 `CLAUDE.md` 和 `AGENTS.md` 内置了多 agent 协调协议。多个 Claude Code 或 Codex 实例可以同时在同一个仓库工作，通过 plan JSON 文件协调，不需要中央调度器。

**协议（每个 agent 严格遵守）：**

1. 读 `.harness/docs/plans/active/` 找到当前计划
2. 找一个 `status == "pending"` 且所有依赖都是 `"done"` 的任务
3. **立即认领**：把 `status` 改为 `"in_progress"`，再开始写代码
4. 在分支 `harness/<plan-id>-<task-id>` 上工作
5. 完成后：`status = "done"`，记录 `pr_url`
6. 回到第 2 步

**实际操作：**

```bash
# 终端 1 — Agent A
cd your-project && claude
# Claude Code 自动读 CLAUDE.md，认领第一个可用任务

# 终端 2 — Agent B（同时开）
cd your-project && claude
# 认领另一个没有未完成依赖的任务
```

关键：步骤 3 的"先认领再动手"防止两个 agent 抢同一个任务。

---

## 支持的项目类型

| 类型 | 检测方式 | Lint | 测试 |
|------|---------|------|------|
| Next.js | `package.json` + `next` | `npm run lint` | `npx vitest run` |
| Node.js | `package.json` | `npm run lint` | `npm test` |
| Python | `pyproject.toml` | `ruff check .` | `pytest` |
| Go | `go.mod` | `go vet ./...` | `go test ./...` |
| Rust | `Cargo.toml` | `cargo clippy` | `cargo test` |

---

## CI 集成

`.github/workflows/harness-check.yml` 已包含在本仓库，可以直接复制到你的项目：

```yaml
name: Harness Check
on:
  push:
    branches: [main]
  pull_request:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install harness
        run: |
          chmod +x harness
          echo "$PWD" >> $GITHUB_PATH
      - name: harness check
        run: harness check --json
```

`harness check` 失败时 exit 1，直接卡住 PR 合并。

---

## 设计原则

### 不是"零人工干预"

OpenAI 原文明确写了 "Humans always remain in the loop"。这个工具不承诺零人工干预——它承诺的是让 agent 在你的仓库里工作得更好、更少走弯路。

### 不是 Agent Runtime

Claude Code 和 Codex 本身就是 agent runtime。我们做的是环境改造，不是重新发明轮子。

### 机械化约束优于口头规范

`harness check` 失败就是失败，exit 1 阻断 CI。不是"建议你测试一下"。

### 文档是一等公民

`harness audit` 把文档完整性纳入评分。文档不更新，分数下降，agent 工作质量下降。

---

## 项目结构

```
harness              ← 主 CLI（Bash）
bin/
  harness-daemon     ← 后台 daemon（PID 锁、JSON 日志、重试、escalation）
src/
  harness_runtime.py ← 执行计划管理、任务状态机、Git 集成
  harness_check.py   ← lint/typecheck/test 检查
  agent_loop.py      ← Agent 主循环框架
  checks/
    audit.py         ← Agent readability 评分
    garden.py        ← 文档卫生 + 代码重复检测
    golden_rules.py  ← 代码模式检查
templates/
  AGENTS.md          ← Agent 入口文件模板
  execution-plan.md  ← 执行计划模板（含 progress log + decision log）
  adr.md             ← Architecture Decision Record 模板
```

---

## 参考

- [OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/)（2026-02-11）
- [CHANGELOG.md](CHANGELOG.md)

## 许可证

MIT License
