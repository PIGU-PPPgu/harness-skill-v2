# Harness Skill v2.0 - Autonomous Multi-Agent Development

> **全自动多智能体协作开发框架** — 基于 OpenAI Harness Engineering，实现零人工干预的全栈开发

将 OpenAI Codex 团队的工程实践与多智能体协作深度融合，让 AI 团队自主完成从需求到部署的完整开发流程。

## 🎯 核心理念

**人类定义目标，智能体自主执行全流程** — 工程师只需：
- 提供产品需求文档（PRD）
- 定义架构约束和质量标准
- 审批关键决策节点
- 其余全部由智能体团队自动完成

## ✨ 核心特性

### 🤖 自主智能体团队
- **Architect** - 架构设计和技术决策
- **Builder** - 代码实现和功能开发
- **Reviewer** - 代码审查和质量把控
- **Tester** - 测试编写和质量验证
- **Doc Writer** - 文档编写和维护
- **DevOps** - CI/CD 和部署管理
- **Coordinator** - 任务协调和进度管理

### 🔄 零干预协作流程
```
PRD → Architect 设计 → Builder 实现 → Reviewer 审查
  → Tester 测试 → Doc Writer 文档 → DevOps 部署
  ↑                                              ↓
  └──────────── Coordinator 全程协调 ──────────┘
```

### 🛠️ 工程实践自动化
- 架构约束自动验证
- 代码质量自动检查
- 文档自动生成和更新
- 测试自动编写和执行
- CI/CD 自动配置和部署

## 🚀 快速开始

### 安装

```bash
# 全局安装
curl -fsSL https://raw.githubusercontent.com/PIGU-PPPgu/harness-skill-v2/main/install.sh | bash

# 或项目级安装
cd your-project
mkdir -p .claude/skills
git clone https://github.com/PIGU-PPPgu/harness-skill-v2.git .claude/skills/harness
```

### 初始化项目

```bash
# 1. 初始化 Harness 结构
/harness init

# 2. 提供 PRD（产品需求文档）
cat > .harness/prd/feature-auth.md << 'EOF'
# 用户认证系统

## 目标
实现完整的用户认证系统，支持注册、登录、JWT token 管理

## 功能需求
- 用户注册（邮箱 + 密码）
- 用户登录（返回 JWT token）
- Token 刷新机制
- 密码加密存储（bcrypt）
- 登录状态验证中间件

## 技术要求
- 后端：Node.js + Express
- 数据库：PostgreSQL
- 测试覆盖率：>80%
EOF

# 3. 启动智能体团队（全自动执行）
/harness swarm start --prd .harness/prd/feature-auth.md --auto-approve
```

### 监控进度

```bash
# 查看智能体团队状态
/harness swarm status

# 查看任务进度
/harness tasks list

# 查看智能体日志
/harness agent logs --role builder
```

## 📚 命令详解

### 项目初始化

#### `/harness init`
创建智能体优先的项目结构：
```
.harness/
├── prd/                    # 产品需求文档
├── architecture/           # 架构设计文档
├── plans/                  # 执行计划
│   ├── active/            # 进行中
│   ├── completed/         # 已完成
│   └── blocked/           # 被阻塞
├── decisions/             # 架构决策记录（ADR）
├── quality/               # 质量标准和报告
├── agents/                # 智能体配置
│   ├── architect.yaml
│   ├── builder.yaml
│   ├── reviewer.yaml
│   ├── tester.yaml
│   ├── doc-writer.yaml
│   ├── devops.yaml
│   └── coordinator.yaml
└── config.json            # 全局配置
```

### 智能体团队管理

#### `/harness swarm start`
启动智能体团队开始工作

**参数**:
- `--prd <file>` - 产品需求文档路径
- `--auto-approve` - 自动批准所有决策（零干预模式）
- `--manual-approve` - 关键决策需要人工批准
- `--agents <roles>` - 指定启动的智能体角色（默认全部）

**示例**:
```bash
# 全自动模式（推荐）
/harness swarm start --prd .harness/prd/feature.md --auto-approve

# 半自动模式（关键决策需批准）
/harness swarm start --prd .harness/prd/feature.md --manual-approve

# 只启动部分智能体
/harness swarm start --prd .harness/prd/feature.md --agents architect,builder,reviewer
```

#### `/harness swarm status`
查看智能体团队当前状态

**输出示例**:
```
🤖 智能体团队状态

Coordinator  ✅ Active    协调任务分配
Architect    ✅ Active    设计数据库 schema
Builder      ✅ Active    实现 auth API (PR #123)
Reviewer     ⏸️  Idle     等待 PR
Tester       ✅ Active    编写集成测试
Doc Writer   ⏸️  Idle     等待代码完成
DevOps       ⏸️  Idle     等待测试通过

📊 进度: 45% (9/20 tasks completed)
⏱️  预计完成: 2小时30分钟
```

#### `/harness swarm stop`
停止智能体团队

#### `/harness swarm pause`
暂停智能体团队（保留状态）

#### `/harness swarm resume`
恢复暂停的智能体团队

### 任务管理

#### `/harness tasks list`
列出所有任务及状态

**输出示例**:
```
📋 任务列表

Active (5):
  #1  [Architect]  设计数据库 schema          ⏳ In Progress
  #2  [Builder]    实现 auth API endpoints    ⏳ In Progress
  #3  [Tester]     编写单元测试               ⏳ In Progress

Pending (8):
  #4  [Builder]    实现 JWT middleware        ⏸️  Waiting
  #5  [Reviewer]   审查 auth API PR           ⏸️  Waiting
  #6  [Doc Writer] 编写 API 文档              ⏸️  Waiting

Completed (7):
  ✅ #0  [Architect]  技术选型和架构设计
  ✅ #-1 [Coordinator] 任务分解和规划
```

#### `/harness tasks show <id>`
查看任务详情

#### `/harness tasks tree`
以树状图显示任务依赖关系

### 智能体管理

#### `/harness agent list`
列出所有智能体及其状态

#### `/harness agent logs --role <role>`
查看特定智能体的日志

**示例**:
```bash
# 查看 Builder 的工作日志
/harness agent logs --role builder

# 实时跟踪日志
/harness agent logs --role builder --follow
```

#### `/harness agent spawn --role <role>`
手动启动单个智能体

### 质量审计

#### `/harness audit`
全面审计项目质量

**输出示例**:
```
📊 项目质量审计报告

代码质量: 92/100 ✅
  - 测试覆盖率: 87% (目标: 80%)
  - Lint 通过率: 100%
  - 复杂度: 平均 4.2 (目标: <10)

架构清晰度: 88/100 ✅
  - 分层架构: 符合
  - 依赖方向: 无违规
  - 边界验证: 95% 覆盖

文档完整度: 75/100 ⚠️
  - API 文档: 100%
  - 架构文档: 90%
  - 用户文档: 45% ⚠️ 需改进

智能体可读性: 95/100 ✅
  - AGENTS.md: 完整
  - 执行计划: 清晰
  - 决策记录: 完整
```

#### `/harness audit --fix`
自动修复可修复的问题

### 架构约束

#### `/harness enforce`
强制执行架构约束

**功能**:
- 生成 ESLint 规则（分层架构）
- 生成结构测试（依赖方向）
- 生成边界验证（Zod schema）
- 配置 CI/CD 检查

#### `/harness golden-rules`
应用黄金原则重构

**黄金原则**:
1. 使用共享工具包（不要手写辅助函数）
2. 边界处验证数据（Zod/Yup）
3. 使用类型化 SDK（不要手动构造请求）
4. 集中管理不变式（规则编码到工具中）

### 文档管理

#### `/harness docs generate`
自动生成文档

**生成内容**:
- API 文档（从代码注释）
- 数据库 schema 文档
- 组件树文档
- 架构图

#### `/harness docs validate`
验证文档新鲜度

#### `/harness garden`
清理过时文档和代码

## 🏗️ 智能体协作协议

### 通信机制

智能体之间通过以下方式通信：

1. **Pull Request** - 代码变更和审查
2. **执行计划** - 任务状态和进度
3. **决策记录** - 架构决策和理由
4. **消息队列** - 实时事件通知

### PR 模板

智能体开启 PR 时自动使用标准模板：

```markdown
## 🎯 目标
[简述这个 PR 要解决什么问题]

## 📝 变更内容
- 新增 xxx 功能
- 修改 xxx 逻辑
- 删除 xxx 冗余代码

## 🔗 关联
- 执行计划: .harness/plans/active/task-123.md
- 相关 Issue: #456
- 依赖 PR: #122

## ✅ 检查清单
- [x] 单元测试已添加
- [x] 集成测试通过
- [x] 文档已更新
- [x] Lint 检查通过
- [x] 架构约束符合

## 👀 审查重点
@reviewer-agent: 请重点检查错误处理逻辑
@security-agent: 新增 API 端点，请审查权限控制

## 🤖 智能体信息
- 创建者: builder-agent-1
- 任务ID: #123
- 预计审查时间: 15分钟
```

### 执行计划格式

`.harness/plans/active/task-123.md`:

```markdown
# 实现用户认证 API

**状态**: In Progress (60%)
**负责智能体**: builder-agent-1
**开始时间**: 2026-03-31 10:00
**预计完成**: 2026-03-31 14:30

## 🎯 目标
实现完整的用户认证 API，包括注册、登录、token 刷新

## 📋 子任务
- [x] 设计数据库 schema (architect-agent)
- [x] 实现用户注册 API (builder-agent-1)
- [x] 实现用户登录 API (builder-agent-1)
- [ ] 实现 token 刷新 API (builder-agent-1) ⏳ 进行中
- [ ] 编写单元测试 (tester-agent)
- [ ] 编写集成测试 (tester-agent)
- [ ] 编写 API 文档 (doc-writer-agent)

## 🔗 依赖
- 依赖任务: #122 (数据库迁移) ✅ 已完成
- 阻塞任务: #124 (前端集成) ⏸️ 等待中

## 📊 进度
```
████████████░░░░░░░░ 60%
```

## 💬 决策记录
- 2026-03-31 10:15: 选择 bcrypt 而非 argon2（性能考虑）
- 2026-03-31 11:30: Token 有效期设为 7 天（产品需求）

## 🚧 阻塞问题
无

## 📝 备注
Builder 进度良好，预计按时完成
```

### 决策记录格式

`.harness/decisions/ADR-001-database-choice.md`:

```markdown
# ADR 001: 数据库选择

**日期**: 2026-03-31
**状态**: Accepted
**决策者**: architect-agent, coordinator-agent
**批准者**: human (auto-approved)

## 背景
需要为用户认证系统选择数据库

## 决策
使用 PostgreSQL

## 理由
1. ACID 事务支持（用户数据一致性要求高）
2. JSON 字段支持（灵活的用户元数据）
3. 成熟的 ORM 支持（Prisma）
4. 智能体熟悉度高（训练数据充足）

## 替代方案
- MongoDB: 缺少事务支持
- MySQL: JSON 支持较弱
- SQLite: 不适合生产环境

## 后果
- ✅ 数据一致性有保障
- ✅ 开发效率高
- ⚠️ 需要额外的数据库服务器
- ⚠️ 比 NoSQL 稍复杂

## 实施
- Architect 已设计 schema
- DevOps 将配置 Docker Compose
- Builder 将使用 Prisma ORM
```

## 🔧 配置文件

### `.harness/config.json`

```json
{
  "project": {
    "name": "my-awesome-app",
    "type": "fullstack",
    "tech_stack": {
      "frontend": "React + TypeScript",
      "backend": "Node.js + Express",
      "database": "PostgreSQL",
      "testing": "Vitest + Playwright"
    }
  },

  "agents": {
    "auto_approve": true,
    "max_concurrent": 5,
    "communication": {
      "method": "pr",
      "notification": true
    }
  },

  "architecture": {
    "layers": ["types", "config", "repository", "service", "runtime", "ui"],
    "dependencies": {
      "ui": ["runtime", "service", "types"],
      "runtime": ["service", "config", "types"],
      "service": ["repository", "config", "types"],
      "repository": ["config", "types"],
      "config": ["types"],
      "types": []
    }
  },

  "quality": {
    "min_test_coverage": 80,
    "max_file_lines": 300,
    "max_function_complexity": 10,
    "lint_rules": "strict"
  },

  "golden_rules": [
    {
      "id": "shared-utils",
      "pattern": "function (debounce|throttle|formatDate)",
      "message": "使用 lodash 或 @/utils",
      "severity": "error"
    },
    {
      "id": "boundary-validation",
      "pattern": "\\.json\\(\\)",
      "message": "使用 Zod 验证 API 响应",
      "severity": "error"
    }
  ],

  "ci_cd": {
    "auto_deploy": false,
    "deploy_on_main": true,
    "require_review": true,
    "auto_merge_cleanup": true
  }
}
```

### `.harness/agents/coordinator.yaml`

```yaml
role: coordinator
description: 任务协调和进度管理

responsibilities:
  - 解析 PRD 并分解任务
  - 分配任务给合适的智能体
  - 监控任务进度
  - 处理阻塞和冲突
  - 生成进度报告

tools:
  - task_manager
  - agent_spawner
  - progress_tracker
  - conflict_resolver

workflow:
  1. 读取 PRD
  2. 调用 Architect 进行技术设计
  3. 分解任务并创建执行计划
  4. 分配任务给 Builder/Tester/Doc Writer
  5. 监控进度，处理阻塞
  6. 协调 Reviewer 审查
  7. 协调 DevOps 部署
  8. 生成完成报告

decision_making:
  - 任务优先级排序
  - 智能体负载均衡
  - 阻塞问题升级
  - 关键决策提交人工审批（如果 auto_approve=false）
```

### `.harness/agents/builder.yaml`

```yaml
role: builder
description: 代码实现和功能开发

responsibilities:
  - 实现功能需求
  - 编写清晰的代码
  - 遵循架构约束
  - 响应审查反馈
  - 修复 bug

tools:
  - code_editor
  - git
  - linter
  - formatter
  - test_runner

workflow:
  1. 从执行计划获取任务
  2. 阅读相关架构文档
  3. 实现功能代码
  4. 运行 lint 和格式化
  5. 编写基础单元测试
  6. 提交 PR
  7. 响应 Reviewer 反馈
  8. 修改代码直到通过审查
  9. 合并 PR
  10. 更新执行计划状态

constraints:
  - 遵循 .harness/architecture/ 中的架构规则
  - 遵循 .harness/config.json 中的质量标准
  - 遵循 golden_rules
  - 单个 PR 不超过 500 行代码
  - 必须包含基础测试

communication:
  - 开启 PR 时使用标准模板
  - 在执行计划中更新进度
  - 遇到阻塞时通知 Coordinator
```

## 🎯 使用场景

### 场景1: 从零开发新功能

```bash
# 1. 编写 PRD
cat > .harness/prd/user-profile.md << 'EOF'
# 用户个人资料功能

## 目标
实现用户个人资料的查看和编辑功能

## 功能需求
- 查看个人资料（头像、昵称、邮箱、简介）
- 编辑个人资料
- 上传头像（支持裁剪）
- 头像存储到 OSS

## 技术要求
- 前端：React + Ant Design
- 后端：Express + Multer
- 存储：阿里云 OSS
- 测试覆盖率：>80%
EOF

# 2. 启动智能体团队（全自动）
/harness swarm start --prd .harness/prd/user-profile.md --auto-approve

# 3. 喝杯咖啡，等待完成通知 ☕
# 智能体团队会自动完成：
# - Architect: 设计数据库和 API
# - Builder: 实现前后端代码
# - Tester: 编写测试
# - Reviewer: 审查代码
# - Doc Writer: 编写文档
# - DevOps: 配置部署

# 4. 查看结果
/harness swarm status
# 输出: ✅ 所有任务已完成，功能已部署到 staging 环境
```

### 场景2: 修复 Bug

```bash
# 1. 创建 bug 报告
cat > .harness/prd/bug-login-timeout.md << 'EOF'
# Bug: 登录超时问题

## 问题描述
用户登录时偶尔出现超时错误（5%概率）

## 复现步骤
1. 打开登录页面
2. 输入用户名密码
3. 点击登录
4. 偶尔出现 "Request timeout" 错误

## 预期行为
登录应该在 2 秒内完成

## 技术分析
可能是数据库查询慢或网络问题
EOF

# 2. 启动调试团队
/harness swarm start --prd .harness/prd/bug-login-timeout.md --agents architect,builder,tester

# 智能体会自动：
# - Architect: 分析性能瓶颈
# - Builder: 修复问题（添加索引/优化查询）
# - Tester: 添加性能测试
```

### 场景3: 重构代码

```bash
# 直接运行清理命令
/harness garden --aggressive

# 智能体会自动：
# - 识别重复代码
# - 提取共享工具函数
# - 统一命名规范
# - 优化文件结构
# - 更新文档
```

## 📊 实战效果

### OpenAI 真实数据
- **团队规模**: 3 工程师 → 7 工程师（含智能体）
- **开发周期**: 5 个月
- **代码量**: 1,000,000+ 行
- **PR 数量**: 1,500+ 个
- **人工编码**: 0%（全部由智能体生成）
- **吞吐量**: 3.5 PRs/天/工程师

### 预期效果（使用本框架）
- **开发速度**: 提升 10x
- **代码质量**: 保持 90+ 分
- **测试覆盖率**: 自动达到 80%+
- **文档完整度**: 自动保持 95%+
- **人工干预**: <5%（仅关键决策）

## 🔄 CI/CD 集成

### GitHub Actions

`.github/workflows/harness-swarm.yml`:

```yaml
name: Harness Swarm CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Install Harness
        run: curl -fsSL https://raw.githubusercontent.com/PIGU-PPPgu/harness-skill-v2/main/install.sh | bash

      - name: Run Quality Audit
        run: /harness audit --ci

      - name: Check Architecture Constraints
        run: /harness enforce --check

      - name: Validate Documentation
        run: /harness docs validate

  agent-review:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v3

      - name: Spawn Reviewer Agent
        run: /harness agent spawn --role reviewer --pr ${{ github.event.pull_request.number }}

      - name: Wait for Review
        run: /harness agent wait --role reviewer --timeout 600

  auto-deploy:
    needs: [quality-check, agent-review]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Spawn DevOps Agent
        run: /harness agent spawn --role devops --task deploy-staging
```

## 🛠️ 兼容性

### 支持的 AI CLI 工具

| CLI 工具 | 版本要求 | 智能体支持 | 状态 |
|---------|---------|-----------|------|
| Claude Code | ≥ 1.0 | ✅ 完整支持 | ✅ 测试通过 |
| Codex | ≥ 0.5 | ✅ 完整支持 | ✅ 测试通过 |
| OpenCode | ≥ 0.3 | ✅ 完整支持 | ✅ 测试通过 |
| OpenClaw | ≥ 0.2 | ✅ 原生支持 | ✅ 推荐使用 |
| Cursor | ≥ 0.30 | ⚠️ 部分支持 | 🔄 开发中 |

## 📖 最佳实践

### 1. PRD 编写规范

**好的 PRD**:
```markdown
# 功能名称

## 目标
[清晰的一句话目标]

## 功能需求
- 需求1（具体、可测试）
- 需求2
- 需求3

## 技术要求
- 技术栈
- 性能指标
- 测试覆盖率

## 验收标准
- [ ] 标准1
- [ ] 标准2
```

**不好的 PRD**:
```markdown
# 做一个用户系统

实现用户相关的功能，要好用。
```

### 2. 渐进式采用

```bash
# 第一周：初始化和熟悉
/harness init
/harness audit

# 第二周：小功能试水
/harness swarm start --prd simple-feature.md --manual-approve

# 第三周：中等功能
/harness swarm start --prd medium-feature.md --auto-approve

# 第四周：完全自动化
/harness swarm start --prd complex-feature.md --auto-approve
```

### 3. 监控和干预

```bash
# 实时监控
watch -n 5 '/harness swarm status'

# 查看日志
/harness agent logs --role coordinator --follow

# 必要时暂停
/harness swarm pause

# 手动干预后恢复
/harness swarm resume
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 开发

```bash
git clone https://github.com/PIGU-PPPgu/harness-skill-v2.git
cd harness-skill-v2

# 测试
./harness help

# 本地安装
ln -s $(pwd) ~/.claude/skills/harness
```

## 📄 许可证

MIT License

## 🔗 参考资料

- [OpenAI Harness Engineering](https://openai.com/index/harness-engineering/)
- [Multi-Agent Systems](https://en.wikipedia.org/wiki/Multi-agent_system)
- [Architecture Decision Records](https://adr.github.io/)
- [Zod Documentation](https://zod.dev/)

## 📝 版本历史

- **v2.0.0** (2026-03-31):
  - 融合 Harness Engineering 和 Multi-Agent 协作
  - 实现零干预全自动开发流程
  - 支持 7 种智能体角色
  - 完整的 CI/CD 集成

---

**Made with ❤️ by AI Engineering Community**

**核心理念**: 让 AI 团队自主完成 95% 的开发工作，人类只需把握方向
