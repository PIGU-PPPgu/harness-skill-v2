# Harness Engineering

> 把你的仓库改造成 AI agent 可以持续、高效工作的环境

## 核心理念

**"Humans steer. Agents execute."**（人类掌舵，Agent 执行）

基于 [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/) 方法论。核心不是"零人工干预"，而是：

- 人类负责：目标、验收标准、架构决策、最终合并
- Agent 负责：写代码、跑测试、开 PR、响应 review

这个工具帮你把仓库改造成"agent 友好"的状态，然后 Claude Code 或 Codex 进来就能直接高效工作。

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
├── CLAUDE.md                    ← Claude Code 入口文件
├── AGENTS.md                    ← Codex / OpenAI 入口文件
└── .harness/
    ├── config.json              ← 项目配置（自动检测项目类型）
    └── docs/
        ├── architecture/        ← 填写你的系统架构
        ├── product/             ← 填写你的产品需求
        ├── quality/             ← 已预填测试和 lint 命令
        ├── security/            ← 已预填安全规范
        └── plans/
            ├── active/          ← 当前执行计划（JSON）
            └── completed/       ← 已完成的计划
```

---

## 工作流

### 第一步：填写文档

初始化后，填写关键文档：

```bash
# 最重要的两个文件
vim CLAUDE.md                                    # 描述项目、运行方式、架构约束
vim .harness/docs/architecture/overview.md       # 系统设计
vim .harness/docs/product/requirements.md        # 当前要做什么
```

文档越清晰，agent 工作越准确。

### 第二步：创建执行计划

```bash
harness plan create "实现用户认证" "添加 JWT 认证，保护 API 接口"
# 输出: Created execution plan: EP-20260401-120000
```

### 第三步：让 Agent 工作

直接用 Claude Code 或 Codex，它们会自动读取 `CLAUDE.md` / `AGENTS.md`：

```bash
# Claude Code
claude

# Codex
codex
```

Agent 会：
1. 读取 `CLAUDE.md` 和 `.harness/docs/` 理解仓库
2. 读取 `plans/active/` 知道当前任务
3. 创建分支、写代码、跑测试
4. 开 PR，等待 review

### 第四步：质量验收

```bash
harness check              # 跑 lint + 类型检查 + 测试 + 文档完整性检查
harness check --only test  # 只跑测试
harness check --json       # JSON 输出（适合 CI）
```

通过后合并 PR。

---

## 命令参考

| 命令 | 说明 |
|------|------|
| `harness init` | 初始化项目，生成 CLAUDE.md、AGENTS.md 和文档骨架 |
| `harness plan create <title> <desc>` | 创建执行计划 |
| `harness check` | 运行所有质量检查 |
| `harness check --only lint` | 只跑 lint |
| `harness check --only test` | 只跑测试 |
| `harness check --json` | JSON 格式输出（CI 用） |
| `harness run [plan_id]` | 启动 agent 主循环（需要 ANTHROPIC_API_KEY） |

---

## 支持的项目类型

`harness init` 自动检测项目类型，`harness check` 自动选择对应命令：

| 类型 | 检测方式 | Lint | 测试 |
|------|---------|------|------|
| Next.js | `package.json` + `next` 依赖 | `npm run lint` | `npx vitest run` |
| Node.js | `package.json` | `npm run lint` | `npm test` |
| Python | `pyproject.toml` / `setup.py` | `ruff check .` | `pytest` |
| Go | `go.mod` | `go vet ./...` | `go test ./...` |
| Rust | `Cargo.toml` | `cargo clippy` | `cargo test` |

---

## 为什么这样设计

### 不是"零人工干预"

OpenAI 原文明确写了 "Humans always remain in the loop"。Agent 能做的是承担大部分编码工作，但人类仍然负责目标定义、架构决策和最终验收。

### 不是通用 Agent Runtime

Claude Code 和 Codex 本身就是 agent runtime，而且比任何自制方案都强。我们做的是把仓库改造成"agent 友好"的状态——结构化文档、清晰的执行计划、机械化的质量约束。

### 不是固定角色流水线

原文没有"七角色流水线"。是单主循环：读文档 → 理解任务 → 写代码 → 验证 → 开 PR。

---

## CI 集成

```yaml
# .github/workflows/harness-check.yml
name: Harness Check
on: [pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install harness
        run: curl -fsSL https://raw.githubusercontent.com/PIGU-PPPgu/harness-skill-v2/main/install.sh | bash
      - name: Run checks
        run: harness check --json
```

---

## 实现状态

- ✅ `harness init` — 生成 CLAUDE.md、AGENTS.md、文档骨架，自动检测项目类型
- ✅ `harness plan create` — 创建执行计划（JSON，带任务状态机）
- ✅ `harness check` — 真实运行 lint/typecheck/test，文档完整性检查
- ✅ `harness run` — agent 主循环框架（Git 集成就绪，AI 调用待接入）
- ⏳ AI 模型直接调用（当前需要用户自己用 Claude Code / Codex）

---

## 参考

- [OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/)（2026-02-11）
- [CHANGELOG.md](CHANGELOG.md) — 记录了误读和纠正过程
- [IMPLEMENTATION.md](IMPLEMENTATION.md) — 详细实现进度

## 许可证

MIT License
