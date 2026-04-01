# CI/CD 集成示例

> ⚠️ 这是一个说明如何在 CI 中使用 Harness 质量检查的示例。
> `harness audit` 和 `harness enforce` 的真实实现仍在开发中。

## 当前可用的 CI 集成

### GitHub Actions - 基础质量检查

```yaml
name: Harness Quality Check

on:
  pull_request:
    branches: [main]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: 安装 Harness
        run: |
          curl -fsSL https://raw.githubusercontent.com/PIGU-PPPgu/harness-skill-v2/main/install.sh | bash
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: 检查 Harness 文档完整性
        run: |
          # 检查必要的文档是否存在
          test -d .harness/docs/product || (echo "缺少产品文档" && exit 1)
          test -d .harness/docs/architecture || (echo "缺少架构文档" && exit 1)
          echo "✓ 文档结构完整"

      - name: 检查执行计划
        run: |
          # 检查是否有活跃的执行计划
          plan_count=$(find .harness/docs/plans/active -name "*.json" 2>/dev/null | wc -l)
          echo "活跃执行计划: $plan_count"
```

## 待实现的 CI 功能

以下功能在路线图中，当前尚未实现：

- `harness check` - 运行真实的仓库约束检查（lint、类型检查）
- `harness doctor` - 检查应用是否可启动、测试是否可跑
- 自动质量门禁（测试覆盖率、lint 错误数）

## 设计原则

Harness Engineering 的 CI 集成应该：

1. **机械化约束**：把质量标准转化为可执行的检查，而不是口头规范
2. **快速反馈**：PR 提交后立即知道是否满足约束
3. **低阻塞**：只在真正重要的问题上阻塞合并

## 参考

- [OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/)
