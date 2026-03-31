# Harness Engineering Skill v2

## 概述

这是一个零干预的自主智能体团队系统，基于 OpenAI Harness Engineering 方法论，实现全栈开发的完全自动化。

## 智能体角色

### 1. Coordinator (协调者)
**职责**: 任务分解、进度跟踪、团队协调

**工作流程**:
1. 读取 PRD 文档
2. 分解为可执行任务
3. 创建执行计划
4. 分配任务给其他智能体
5. 监控进度并调整计划

**输出**:
- `.harness/plans/execution-plan-{id}.md`
- 任务分配消息

**通信协议**:
```markdown
## 任务分配
- **接收者**: @architect
- **任务**: 设计用户认证系统架构
- **优先级**: P0
- **依赖**: 无
- **截止时间**: 2小时
```

### 2. Architect (架构师)
**职责**: 架构设计、技术决策、ADR 编写

**工作流程**:
1. 接收架构设计任务
2. 分析需求和约束
3. 设计系统架构
4. 编写 ADR 文档
5. 通知 Builder 开始实现

**输出**:
- `.harness/architecture/*.md`
- `.harness/decisions/ADR-{number}.md`

**ADR 模板**:
```markdown
# ADR-001: 选择 JWT 作为认证方案

## 状态
已接受

## 上下文
需要实现用户认证系统，考虑了 Session 和 JWT 两种方案。

## 决策
选择 JWT，因为：
1. 无状态，易于扩展
2. 支持跨域
3. 移动端友好

## 后果
- 需要实现 token 刷新机制
- 需要处理 token 失效问题
```

### 3. Builder (构建者)
**职责**: 代码实现、单元测试

**工作流程**:
1. 接收实现任务
2. 创建功能分支
3. 实现代码
4. 编写单元测试
5. 创建 PR
6. 通知 Reviewer

**PR 模板**:
```markdown
## 变更说明
实现用户认证 API

## 实现细节
- 添加 JWT 生成和验证
- 实现登录/注册接口
- 添加密码加密

## 测试
- ✅ 单元测试覆盖率 85%
- ✅ 所有测试通过

## 检查清单
- [x] 代码符合架构约束
- [x] 添加了单元测试
- [x] 更新了类型定义
- [x] 无 lint 错误

## 关联
- 执行计划: #EP-001
- ADR: ADR-001
```

### 4. Reviewer (审查者)
**职责**: 代码审查、质量把关

**工作流程**:
1. 接收 PR 通知
2. 审查代码质量
3. 检查架构约束
4. 验证测试覆盖率
5. 提供反馈或批准
6. 通知 Tester

**审查清单**:
```markdown
## 代码质量
- [ ] 代码可读性
- [ ] 命名规范
- [ ] 注释充分
- [ ] 无重复代码

## 架构约束
- [ ] 层级依赖正确
- [ ] 无循环依赖
- [ ] 符合设计模式

## 测试
- [ ] 覆盖率 ≥ 80%
- [ ] 测试用例完整
- [ ] 边界条件测试

## 安全
- [ ] 无 SQL 注入风险
- [ ] 无 XSS 风险
- [ ] 敏感数据加密
```

### 5. Tester (测试者)
**职责**: 集成测试、E2E 测试

**工作流程**:
1. 接收测试任务
2. 编写集成测试
3. 编写 E2E 测试
4. 执行测试套件
5. 报告测试结果
6. 通知 Doc Writer

**测试报告**:
```markdown
## 测试结果
- 单元测试: 125/125 通过
- 集成测试: 45/45 通过
- E2E 测试: 12/12 通过
- 覆盖率: 87%

## 性能指标
- API 响应时间: 平均 45ms
- 数据库查询: 平均 12ms
- 内存使用: 峰值 256MB

## 问题
无
```

### 6. Doc Writer (文档编写者)
**职责**: 文档维护、API 文档生成

**工作流程**:
1. 接收文档任务
2. 更新 README
3. 生成 API 文档
4. 更新变更日志
5. 通知 DevOps

**文档结构**:
```markdown
## API 文档

### POST /api/auth/login
登录接口

**请求**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**响应**:
```json
{
  "token": "eyJhbGc...",
  "user": {
    "id": "123",
    "email": "user@example.com"
  }
}
```

**错误码**:
- 401: 认证失败
- 400: 参数错误
```

### 7. DevOps (运维者)
**职责**: CI/CD、部署、监控

**工作流程**:
1. 接收部署任务
2. 配置 CI/CD 流水线
3. 执行部署
4. 配置监控
5. 报告部署状态
6. 通知 Coordinator

**部署报告**:
```markdown
## 部署信息
- 环境: production
- 版本: v1.2.0
- 时间: 2024-01-15 14:30:00
- 状态: ✅ 成功

## 健康检查
- API 健康: ✅
- 数据库连接: ✅
- 缓存服务: ✅

## 监控配置
- 错误率告警: < 1%
- 响应时间告警: > 500ms
- CPU 使用率告警: > 80%
```

## 通信协议

### 消息格式
```json
{
  "from": "coordinator",
  "to": "architect",
  "type": "task_assignment",
  "priority": "P0",
  "task": {
    "id": "TASK-001",
    "title": "设计认证系统架构",
    "description": "...",
    "dependencies": [],
    "deadline": "2024-01-15T16:00:00Z"
  }
}
```

### 消息类型
- `task_assignment`: 任务分配
- `task_completed`: 任务完成
- `review_request`: 审查请求
- `review_feedback`: 审查反馈
- `deployment_request`: 部署请求
- `status_update`: 状态更新

## 执行计划格式

```markdown
# 执行计划 EP-001: 用户认证系统

## 目标
实现完整的用户认证系统

## 任务分解
1. [ARCH-001] 架构设计 (@architect) - 2h
2. [BUILD-001] 实现后端 API (@builder) - 4h
3. [BUILD-002] 实现前端组件 (@builder) - 3h
4. [TEST-001] 编写测试 (@tester) - 2h
5. [DOC-001] 编写文档 (@doc-writer) - 1h
6. [DEPLOY-001] 部署上线 (@devops) - 1h

## 依赖关系
- BUILD-001 依赖 ARCH-001
- BUILD-002 依赖 BUILD-001
- TEST-001 依赖 BUILD-002
- DOC-001 依赖 TEST-001
- DEPLOY-001 依赖 DOC-001

## 时间线
- 开始: 2024-01-15 10:00
- 预计完成: 2024-01-15 23:00
- 总工时: 13h

## 状态
- [x] ARCH-001 已完成
- [ ] BUILD-001 进行中
- [ ] BUILD-002 待开始
- [ ] TEST-001 待开始
- [ ] DOC-001 待开始
- [ ] DEPLOY-001 待开始
```

## 质量标准

### 代码质量
- 测试覆盖率 ≥ 80%
- 单文件行数 ≤ 500
- 函数长度 ≤ 50 行
- 圈复杂度 ≤ 10

### 架构约束
- 严格遵守分层架构
- 禁止跨层依赖
- 禁止循环依赖

### 性能标准
- API 响应时间 < 100ms (P95)
- 数据库查询 < 50ms (P95)
- 前端首屏加载 < 2s

## 自动化流程

### 1. PRD 驱动开发
```bash
# 用户提供 PRD
echo "需求文档" > .harness/prd/feature-auth.md

# Coordinator 自动启动
/harness swarm start

# 自动执行完整流程
# 1. Coordinator 分解任务
# 2. Architect 设计架构
# 3. Builder 实现代码
# 4. Reviewer 审查代码
# 5. Tester 执行测试
# 6. Doc Writer 更新文档
# 7. DevOps 部署上线
```

### 2. 自动审批模式
```json
{
  "auto_approve": {
    "enabled": true,
    "conditions": {
      "test_coverage": ">= 80",
      "lint_errors": "== 0",
      "architecture_violations": "== 0"
    }
  }
}
```

### 3. 持续监控
```bash
# 自动监控部署状态
/harness agent logs --role devops --follow

# 自动监控任务进度
/harness swarm status --watch
```

## 配置文件

### .harness/config.json
```json
{
  "version": "2.0",
  "agents": {
    "coordinator": {
      "enabled": true,
      "auto_start": true
    },
    "architect": {
      "enabled": true,
      "model": "claude-3-5-sonnet"
    },
    "builder": {
      "enabled": true,
      "model": "claude-3-5-sonnet",
      "parallel_tasks": 2
    },
    "reviewer": {
      "enabled": true,
      "model": "claude-3-5-sonnet",
      "auto_approve": true
    },
    "tester": {
      "enabled": true,
      "model": "claude-3-5-sonnet"
    },
    "doc_writer": {
      "enabled": true,
      "model": "claude-3-5-sonnet"
    },
    "devops": {
      "enabled": true,
      "model": "claude-3-5-sonnet",
      "auto_deploy": false
    }
  },
  "architecture": {
    "layers": ["types", "config", "repository", "service", "runtime", "ui"],
    "allowedDependencies": {
      "ui": ["runtime", "service", "types"],
      "runtime": ["service", "config", "types"],
      "service": ["repository", "config", "types"],
      "repository": ["config", "types"],
      "config": ["types"],
      "types": []
    }
  },
  "quality": {
    "minCoverage": 80,
    "maxFileSize": 500,
    "maxFunctionLength": 50,
    "maxComplexity": 10
  },
  "communication": {
    "protocol": "pull_request",
    "message_queue": "redis",
    "notification": "slack"
  }
}
```

## 使用示例

### 场景 1: 新功能开发
```bash
# 1. 创建 PRD
cat > .harness/prd/user-profile.md << EOF
# 用户资料功能

## 需求
用户可以查看和编辑个人资料

## 功能点
- 查看资料
- 编辑资料
- 上传头像
EOF

# 2. 启动智能体团队
/harness swarm start

# 3. 监控进度（可选）
/harness swarm status

# 4. 等待完成
# 智能体团队会自动完成所有工作
```

### 场景 2: Bug 修复
```bash
# 1. 创建 Bug 报告
cat > .harness/prd/bug-login-timeout.md << EOF
# Bug: 登录超时

## 问题
用户登录时偶尔超时

## 重现步骤
1. 打开登录页面
2. 输入用户名密码
3. 点击登录
4. 等待 30 秒后超时

## 期望
登录应在 5 秒内完成
EOF

# 2. 启动修复流程
/harness swarm start --mode bugfix

# 智能体团队会自动：
# - 分析问题
# - 定位代码
# - 修复 Bug
# - 添加测试
# - 部署修复
```

### 场景 3: 代码重构
```bash
# 1. 创建重构计划
cat > .harness/prd/refactor-auth.md << EOF
# 重构: 认证模块

## 目标
优化认证模块性能和可维护性

## 改进点
- 提取公共逻辑
- 优化数据库查询
- 添加缓存层
EOF

# 2. 启动重构
/harness swarm start --mode refactor

# 智能体团队会自动：
# - 分析现有代码
# - 设计重构方案
# - 逐步重构
# - 确保测试通过
# - 更新文档
```

## 监控和调试

### 查看智能体日志
```bash
# 查看所有智能体日志
/harness agent logs --all

# 查看特定智能体日志
/harness agent logs --role builder

# 实时跟踪日志
/harness agent logs --role coordinator --follow
```

### 查看执行计划
```bash
# 列出所有执行计划
/harness plans list

# 查看特定计划
/harness plans show EP-001

# 查看计划进度
/harness plans progress EP-001
```

### 查看质量报告
```bash
# 生成质量报告
/harness audit

# 查看架构违规
/harness enforce --check

# 查看测试覆盖率
/harness test coverage
```

## 故障处理

### 智能体失败
```bash
# 重启失败的智能体
/harness agent restart --role builder

# 重新分配任务
/harness tasks reassign TASK-001 --to builder-2
```

### 任务阻塞
```bash
# 查看阻塞原因
/harness tasks blocked

# 手动解除阻塞
/harness tasks unblock TASK-001
```

### 回滚部署
```bash
# 回滚到上一版本
/harness deploy rollback

# 回滚到指定版本
/harness deploy rollback --version v1.1.0
```

## 最佳实践

### 1. PRD 编写
- 清晰描述需求
- 提供用例和场景
- 明确验收标准
- 包含非功能需求

### 2. 任务分解
- 任务粒度适中（2-4 小时）
- 明确依赖关系
- 设置合理优先级
- 预留缓冲时间

### 3. 代码审查
- 自动审查为主
- 关键代码人工审查
- 及时反馈问题
- 记录审查决策

### 4. 测试策略
- 单元测试覆盖核心逻辑
- 集成测试覆盖关键流程
- E2E 测试覆盖用户场景
- 性能测试覆盖瓶颈点

### 5. 部署策略
- 灰度发布
- 金丝雀部署
- 蓝绿部署
- 快速回滚

## 集成示例

### GitHub Actions
```yaml
name: Harness CI/CD

on:
  push:
    branches: [main]

jobs:
  harness:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Harness
        run: |
          /harness swarm start --ci-mode
          /harness swarm wait
          /harness audit
```

### GitLab CI
```yaml
harness:
  stage: build
  script:
    - /harness swarm start --ci-mode
    - /harness swarm wait
    - /harness audit
  only:
    - main
```

### Jenkins
```groovy
pipeline {
  agent any
  stages {
    stage('Harness') {
      steps {
        sh '/harness swarm start --ci-mode'
        sh '/harness swarm wait'
        sh '/harness audit'
      }
    }
  }
}
```

## 总结

Harness Engineering v2 提供了一个完全自主的智能体团队系统，实现了从需求到部署的全流程自动化。通过 PRD 驱动开发、自动审批和持续监控，最大程度减少人工干预，提高开发效率和代码质量。
