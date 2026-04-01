# 用户认证功能开发示例

> ⚠️ 这是一个说明 Harness Engineering 工作流的示例，展示人类和 agent 如何协作。
> 当前实现仍在开发中，部分步骤需要手动完成。

## 场景

为一个 Web 应用添加 JWT 用户认证功能。

## 工作流

### 1. 人类：定义目标和验收标准

在 `.harness/docs/product/auth-feature.md` 中写清楚：

```markdown
# 用户认证功能

## 目标
为 API 添加 JWT 认证，保护需要登录的接口。

## 验收标准
- [ ] POST /api/login 接受 email/password，返回 JWT token
- [ ] 受保护接口在无 token 时返回 401
- [ ] Token 过期时间 24 小时
- [ ] 密码使用 bcrypt 哈希存储

## 技术约束
- 使用现有的 User 数据模型
- 不引入新的数据库依赖
- 测试覆盖率 ≥ 80%
```

### 2. 人类：创建执行计划

```bash
harness plan create "用户认证" "添加 JWT 认证系统"
# 输出: Created execution plan: EP-20260401-120000
```

### 3. Agent：执行开发循环

```bash
export ANTHROPIC_API_KEY=your_key
harness run EP-20260401-120000
```

Agent 会自动：
1. 读取 `.harness/docs/` 下的所有文档
2. 理解仓库结构和现有代码
3. 创建工作分支
4. 实现代码
5. 运行测试，失败则自动修复
6. 创建 PR

### 4. 人类：Review PR

人类负责：
- 验证业务逻辑是否正确
- 检查安全实现
- 提供 review 意见

### 5. Agent：响应 review

Agent 读取 review 评论，自动修改代码，更新 PR。

### 6. 人类：验收并合并

确认满足验收标准后，人类合并 PR。

---

## 关键原则

**人类负责**：目标、验收标准、架构决策、安全审查、最终合并

**Agent 负责**：读文档、写代码、跑测试、开 PR、响应 review

## 当前实现状态

- ✅ `harness init` - 初始化文档结构
- ✅ `harness plan create` - 创建执行计划
- ✅ `harness run` - 启动 agent 主循环（框架就绪，AI 调用待接入）
- ⏳ AI 模型集成（需要 ANTHROPIC_API_KEY）
- ⏳ 自动 PR 创建（需要 gh CLI）
