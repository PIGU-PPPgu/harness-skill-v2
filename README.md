# Harness Engineering

> **Agent-first repository harness** - 基于 OpenAI Harness Engineering 方法论的仓库改造工具

## 核心理念

**"Humans steer. Agents execute."**（人类掌舵，智能体执行）

这不是一个"零人工干预的自动化框架"，而是一套**改造仓库和环境**的方法论，让 AI agent 能够在你的特定仓库中持续、高效地工作。

### 什么是 Harness Engineering？

Harness Engineering 是 OpenAI 提出的一种工程实践，核心思想是：

- **人类始终在环**（Humans always remain in the loop）
- 人类负责：目标设定、优先级、验收标准、架构决策、风险判断
- Agent 负责：编写代码、运行测试、创建 PR、响应 review、修复问题
- **不是通用框架**：每个仓库需要根据自身特点进行定制化改造

### 与传统开发的区别

**传统开发**：
```
人类 → 写代码 → 测试 → PR → Review → 合并
```

**Harness Engineering**：
```
人类 → 定义目标 → Agent 写代码 → Agent 测试 → Agent 开 PR
→ Agent 响应 review → 人类验收 → 合并
```

人类从"写代码"提升到"定义目标和验收标准"的抽象层。

## 快速开始

### 1. 初始化仓库 Harness

```bash
# 安装
curl -fsSL https://raw.githubusercontent.com/PIGU-PPPgu/harness-skill-v2/main/install.sh | bash

# 在你的项目中初始化
cd your-project
harness init
```

这会创建：
```
.harness/
├── docs/
│   ├── architecture/      # 架构文档
│   ├── product/          # 产品需求
│   ├── quality/          # 质量标准
│   └── plans/            # 执行计划
├── config.json           # Harness 配置
└── constraints/          # 约束规则
```

### 2. 编写结构化文档

Agent 需要清晰的仓库文档才能有效工作。

### 3. 定义执行计划

创建清晰的执行计划，包含目标、验收标准和技术约束。

### 4. 启动 Agent 工作循环

```bash
harness run
```

## 核心功能

### 1. 结构化知识系统

将仓库知识结构化，让 agent 能快速理解。

### 2. 可执行环境

Agent 需要能够启动和验证应用。

### 3. 机械化约束

将质量标准转化为可执行的检查。

### 4. 执行计划管理

管理和跟踪执行计划的生命周期。

### 5. PR 工作流

Agent 创建 PR、响应 review、修复问题。

### 6. 持续清理

Agent 会复制坏模式，需要持续清理。

## 配置

详见 `.harness/config.json`

## 工作流示例

### 场景 1: 新功能开发

1. 人类：创建执行计划
2. Agent：执行开发
3. 人类：Review PR
4. 人类：提供反馈
5. Agent：响应反馈
6. 人类：验收并合并

### 场景 2: Bug 修复

1. 人类：创建 bug 报告
2. Agent：调查和修复
3. 人类：验证修复
4. 人类：合并

### 场景 3: 代码重构

1. 人类：定义重构目标
2. Agent：执行重构
3. 人类：验证性能
4. 人类：合并

## 最佳实践

### 1. 文档驱动

编写清晰、结构化的文档。

### 2. 渐进式改造

不要一次性改造整个仓库，从一个模块开始。

### 3. 持续验证

每次 PR 前运行完整检查。

### 4. 人类监督

**何时需要人类介入**：
- 架构决策
- 安全审查
- 性能优化
- 用户体验
- 风险评估

**Agent 可以自主处理**：
- 编写代码
- 运行测试
- 修复 lint 错误
- 响应 review 评论
- 更新文档
- 重构重复代码

### 5. 反馈循环

持续提供反馈，帮助 agent 改进。

## 限制和注意事项

### 这不是银弹

Harness Engineering **不能**：
- 替代人类的判断和决策
- 自动理解模糊的需求
- 处理所有边界情况
- 保证零 bug
- 替代代码 review

### 适用场景

**适合**：
- 结构清晰的仓库
- 有完善测试的项目
- 需求明确的功能
- 重复性的重构工作

**不适合**：
- 全新项目（缺少结构）
- 需求不明确
- 复杂的架构决策
- 需要大量用户反馈的功能

### 成本考虑

- Agent 调用 API 有成本
- 需要维护文档和约束
- 初期改造需要投入时间
- 需要持续监督和反馈

## 参考资料

- [OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/)
- [OpenAI: Introducing Codex](https://openai.com/index/introducing-codex/)

## 许可证

MIT License

---

**记住**：Harness Engineering 的核心是"Humans steer. Agents execute."，不是"零人工干预"。
