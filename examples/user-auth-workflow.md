# 示例: 用户认证功能开发

这个示例展示了如何使用 Harness Engineering v2 从零开始开发一个用户认证功能。

## 步骤 1: 初始化项目

```bash
# 创建项目目录
mkdir my-app
cd my-app

# 初始化 Harness
harness init
```

## 步骤 2: 编写 PRD

创建 `.harness/prd/user-auth.md`:

```markdown
# 用户认证功能

## 功能概述
实现完整的用户认证系统，包括注册、登录、登出和密码重置功能。

## 目标用户
所有需要访问系统的用户

## 功能需求

### 核心功能
1. 用户注册
   - 邮箱注册
   - 密码强度验证
   - 邮箱验证

2. 用户登录
   - 邮箱/密码登录
   - JWT token 认证
   - 记住我功能

3. 用户登出
   - 清除 token
   - 清除会话

4. 密码重置
   - 发送重置邮件
   - 验证重置链接
   - 更新密码

## 用户故事

### 故事 1: 用户注册
**作为** 新用户
**我想要** 注册账号
**以便** 使用系统功能

**验收标准**:
- [ ] 可以使用邮箱和密码注册
- [ ] 密码需要至少 8 位，包含大小写字母和数字
- [ ] 注册后收到验证邮件
- [ ] 验证邮箱后才能登录

### 故事 2: 用户登录
**作为** 已注册用户
**我想要** 登录系统
**以便** 访问我的数据

**验收标准**:
- [ ] 可以使用邮箱和密码登录
- [ ] 登录成功后获得 JWT token
- [ ] 可以选择"记住我"保持登录状态
- [ ] 登录失败显示错误信息

## 非功能需求

### 性能
- 登录 API 响应时间: < 100ms
- 注册 API 响应时间: < 200ms

### 安全
- 密码使用 bcrypt 加密
- JWT token 有效期 24 小时
- 刷新 token 有效期 7 天
- 实现 CSRF 保护

### 可用性
- 系统可用性: 99.9%
- 错误率: < 0.1%

## 技术约束
- 使用 Node.js + Express
- 使用 PostgreSQL 数据库
- 使用 JWT 进行认证
- 使用 bcrypt 加密密码

## 时间线
- 设计阶段: 2h
- 开发阶段: 6h
- 测试阶段: 2h
- 上线时间: 1h
```

## 步骤 3: 启动智能体团队

```bash
harness swarm start
```

输出:
```
🚀 启动智能体团队...
📋 找到 1 个 PRD 文件
📝 创建执行计划: EP-20240115-100000
🤖 启动 Coordinator 智能体...
✅ 智能体团队启动成功

使用 'harness swarm status' 查看进度
使用 'harness agent logs --role coordinator' 查看日志
```

## 步骤 4: 监控进度

```bash
harness swarm status
```

输出:
```
智能体团队状态:

┌─────────────┬──────────┬────────────┬──────────┐
│ 智能体      │ 状态     │ 当前任务   │ 进度     │
├─────────────┼──────────┼────────────┼──────────┤
│ Coordinator │ 运行中   │ 任务分配   │ 100%     │
│ Architect   │ 运行中   │ 架构设计   │ 75%      │
│ Builder     │ 运行中   │ 代码实现   │ 50%      │
│ Reviewer    │ 空闲     │ -          │ -        │
│ Tester      │ 空闲     │ -          │ -        │
│ Doc Writer  │ 空闲     │ -          │ -        │
│ DevOps      │ 空闲     │ -          │ -        │
└─────────────┴──────────┴────────────┴──────────┘

总体进度: 3/10 任务完成 (30%)
```

## 步骤 5: 查看执行计划

```bash
cat .harness/plans/execution-plan-EP-20240115-100000.md
```

内容:
```markdown
# 执行计划 EP-20240115-100000: 用户认证系统

## 目标
实现完整的用户认证系统

## 任务分解
1. [ARCH-001] 架构设计 (@architect) - 2h ✅
2. [BUILD-001] 实现数据库模型 (@builder) - 1h ✅
3. [BUILD-002] 实现认证 API (@builder) - 3h ⏳
4. [BUILD-003] 实现前端组件 (@builder) - 2h ⏸️
5. [TEST-001] 编写单元测试 (@tester) - 1h ⏸️
6. [TEST-002] 编写集成测试 (@tester) - 1h ⏸️
7. [DOC-001] 编写 API 文档 (@doc-writer) - 0.5h ⏸️
8. [DOC-002] 更新用户文档 (@doc-writer) - 0.5h ⏸️
9. [DEPLOY-001] 配置 CI/CD (@devops) - 0.5h ⏸️
10. [DEPLOY-001] 部署上线 (@devops) - 0.5h ⏸️

## 状态
- [x] ARCH-001 已完成
- [x] BUILD-001 已完成
- [ ] BUILD-002 进行中 (75%)
- [ ] BUILD-003 待开始
- [ ] TEST-001 待开始
- [ ] TEST-002 待开始
- [ ] DOC-001 待开始
- [ ] DOC-002 待开始
- [ ] DEPLOY-001 待开始
- [ ] DEPLOY-002 待开始
```

## 步骤 6: 查看架构决策

```bash
cat .harness/decisions/ADR-001.md
```

内容:
```markdown
# ADR-001: 选择 JWT 作为认证方案

## 状态
已接受

## 上下文
需要实现用户认证系统，考虑了 Session 和 JWT 两种方案。

### 考虑的方案

#### 方案 1: Session-based 认证
**优点**:
- 服务端可以主动失效 session
- 更容易实现单点登录

**缺点**:
- 需要服务端存储 session
- 水平扩展需要 session 共享
- 移动端支持不友好

#### 方案 2: JWT 认证
**优点**:
- 无状态，易于扩展
- 支持跨域
- 移动端友好
- 可以包含用户信息

**缺点**:
- 无法主动失效 token
- Token 体积较大

## 决策
选择 JWT，因为：
1. 系统需要支持移动端
2. 需要水平扩展能力
3. 可以通过短期 token + 刷新 token 解决失效问题

## 后果
- 需要实现 token 刷新机制
- 需要处理 token 失效问题
- 需要在客户端安全存储 token
```

## 步骤 7: 查看生成的代码

智能体会自动创建 PR，可以查看:

```bash
# 查看 PR 列表
gh pr list

# 查看 PR 详情
gh pr view 1
```

PR 内容示例:
```markdown
## 变更说明
实现用户认证 API

## 实现细节
- 添加 User 模型
- 实现注册接口 POST /api/auth/register
- 实现登录接口 POST /api/auth/login
- 实现登出接口 POST /api/auth/logout
- 添加 JWT 中间件
- 添加密码加密

## 测试
- ✅ 单元测试覆盖率 87%
- ✅ 所有测试通过

## 检查清单
- [x] 代码符合架构约束
- [x] 添加了单元测试
- [x] 更新了类型定义
- [x] 无 lint 错误

## 关联
- 执行计划: EP-20240115-100000
- ADR: ADR-001
```

## 步骤 8: 查看测试报告

```bash
cat .harness/quality/test-report-20240115.md
```

内容:
```markdown
## 测试结果
- 单元测试: 45/45 通过
- 集成测试: 12/12 通过
- E2E 测试: 5/5 通过
- 覆盖率: 87%

## 性能指标
- 注册 API: 平均 85ms
- 登录 API: 平均 45ms
- 验证 API: 平均 12ms

## 安全检查
- ✅ 密码正确加密
- ✅ JWT 签名验证
- ✅ CSRF 保护
- ✅ SQL 注入防护
```

## 步骤 9: 查看文档

```bash
cat docs/api/auth.md
```

内容:
```markdown
# 认证 API

## POST /api/auth/register
注册新用户

**请求**:
```json
{
  "email": "user@example.com",
  "password": "Password123",
  "name": "John Doe"
}
```

**响应**:
```json
{
  "message": "注册成功，请查收验证邮件"
}
```

## POST /api/auth/login
用户登录

**请求**:
```json
{
  "email": "user@example.com",
  "password": "Password123"
}
```

**响应**:
```json
{
  "token": "eyJhbGc...",
  "refreshToken": "eyJhbGc...",
  "user": {
    "id": "123",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```
```

## 步骤 10: 部署

智能体会自动配置 CI/CD 并部署:

```bash
# 查看部署状态
harness agent logs --role devops
```

输出:
```
2024-01-15 22:00:00 [DevOps] 开始部署...
2024-01-15 22:00:30 [DevOps] 运行测试... ✅
2024-01-15 22:01:00 [DevOps] 构建镜像... ✅
2024-01-15 22:02:00 [DevOps] 推送镜像... ✅
2024-01-15 22:03:00 [DevOps] 部署到生产环境... ✅
2024-01-15 22:03:30 [DevOps] 健康检查... ✅
2024-01-15 22:04:00 [DevOps] 部署完成! 🎉
```

## 总结

整个过程完全自动化，从 PRD 到部署上线，无需人工干预。智能体团队自动完成了:

1. ✅ 架构设计和技术决策
2. ✅ 数据库模型设计
3. ✅ API 实现
4. ✅ 前端组件实现
5. ✅ 单元测试和集成测试
6. ✅ API 文档生成
7. ✅ CI/CD 配置
8. ✅ 部署上线

总耗时: 约 11 小时（实际并行执行约 6 小时）

## 查看完整日志

```bash
# 查看所有智能体的工作日志
harness agent logs --all

# 查看质量审计报告
harness audit

# 查看架构约束检查
harness enforce --check
```
