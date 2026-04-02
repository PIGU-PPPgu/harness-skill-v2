# 我把 Claude Code 调教成了一个不乱跑的好 Agent

## 你有没有遇到过这种情况

把任务丢给 Claude Code 或 Codex，它开始噼里啪啦写代码。

写完你一看——方向错了。它不知道你有个专门的 utils/ 目录，它不知道你这个模块不能直接访问数据库，它不知道你上周刚重构了那块逻辑。

于是你花了 20 分钟解释背景，它重写，还是偏，再解释……

**这不是 AI 不够聪明，是你的仓库对 AI 不友好。**

---

## 问题出在哪

OpenAI 在今年二月发了一篇文章，叫 [Harness Engineering](https://openai.com/index/harness-engineering/)。

核心观点是：AI agent 能不能好好工作，很大程度上取决于你的仓库有没有给它准备好"工作环境"。

他们内部用这套方法，让 agent 承担了相当一部分实际的开发工作。不是零人工干预——**人负责决策和审查，agent 负责执行**。

这个分工很清晰：

| 人类负责 | Agent 负责 |
|---------|-----------|
| 目标和验收标准 | 读文档理解仓库 |
| 架构决策 | 写代码、跑测试 |
| 安全审查 | 开 PR、响应 review |
| 最终合并 | 根据反馈修改 |

问题是，大多数仓库根本没有给 agent 准备这些东西。没有入口文件，没有架构约束，没有当前任务是什么——agent 进来两眼一抹黑。

---

## 我做了什么

我做了一个工具，叫 **Harness Engineering**，把上面的方法论落地成可以直接用的 CLI。

一条命令初始化：

```bash
harness init
```

它会在你的项目里生成：

```
your-project/
├── CLAUDE.md          ← Claude Code 自动读取的入口文件
├── AGENTS.md          ← Codex / 其他 agent 的入口文件
└── .harness/
    └── docs/
        ├── architecture/   ← 系统架构文档
        ├── product/        ← 产品需求
        ├── quality/        ← 质量标准（已预填命令）
        ├── security/       ← 安全规范
        └── plans/active/   ← 执行计划（JSON + 状态机）
```

你填好这些文档，agent 进来读一遍，就知道：
- 这个项目是干什么的
- 架构是怎么分层的，什么不能动
- 当前在做哪个任务，做到哪一步了

---

## 执行计划：让 agent 知道"现在在做什么"

这是最关键的一块。

```bash
harness plan create "实现用户认证" "添加 JWT 认证，保护 API 接口"
# → Created execution plan: EP-20260401-120000

harness plan list
# → Active plans:
#   EP-20260401-120000  [0/3]  实现用户认证
```

计划存成 JSON 文件，带任务状态机（pending → in_progress → done）。

Agent 每次开始工作，先读计划，知道做什么、依赖什么、当前卡在哪。做完一步，更新状态。下次继续的时候，不用从头解释。

---

## harness check：机械化验收

这里有个很常见的问题：很多"质量检查"工具其实只是打印一行"✓ passed"，但背后什么都没跑。

`harness check` 是真的跑：

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

自动检测项目类型（Next.js / Node / Python / Go / Rust），选对应的 lint 和 test 命令。失败就 exit 1，直接卡掉 CI。

不是"建议你测试一下"，是"没过就不让合并"。

---

## harness audit：量化 agent 可读性

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

把仓库对 agent 的友好程度量化成一个 0-100 的分数。

文档没更新、没有执行计划、没有 CI——分数会掉。分数掉了，agent 工作质量也会掉，这个因果链是真实的。

---

## harness garden：代码卫生

```bash
harness garden        # 文档过期检查 + 代码重复检测
harness golden-rules  # 代码模式检查（重复工具函数、未验证 API、魔法数字）
```

检查：
- 90 天未更新的文档（过期信息比没有信息更危险）
- 重复定义的工具函数（debounce / formatDate 写了三份）
- 未经 schema 验证的 API 响应
- setTimeout 里的硬编码数字

---

## 完整工作流

```
1. harness init          生成文档骨架
        ↓
2. 填写文档              描述架构、需求、约束
        ↓
3. harness plan create   创建执行计划
        ↓
4. claude / codex        Agent 读文档、写代码、开 PR
        ↓
5. harness check         验收（lint + test + 文档完整性）
6. harness audit         检查 agent readability 评分
        ↓
7. 人类 review 并合并
```

步骤 4 就是你正常用 Claude Code 或 Codex，不需要换工具。Harness 做的是让步骤 4 变得更顺。

---

## 安装

```bash
curl -fsSL https://raw.githubusercontent.com/PIGU-PPPgu/harness-skill-v2/main/install.sh | bash
```

支持 macOS / Linux。

GitHub：https://github.com/PIGU-PPPgu/harness-skill-v2

---

## 一句话总结

**Claude Code 和 Codex 已经足够强了，你需要做的是把仓库改造成它们能顺畅工作的环境。**

这个工具做的就是这件事。

---

*基于 OpenAI Harness Engineering（2026-02-11）方法论实现。MIT License。*
