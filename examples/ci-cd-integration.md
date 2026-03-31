# CI/CD 集成示例

## GitHub Actions

创建 `.github/workflows/harness.yml`:

```yaml
name: Harness CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  harness-check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: 安装 Harness
        run: |
          curl -fsSL https://raw.githubusercontent.com/PIGU-PPPgu/harness-skill-v2/main/install.sh | bash
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: 质量审计
        run: harness audit

      - name: 架构约束检查
        run: harness enforce --check

      - name: 生成报告
        if: always()
        run: |
          mkdir -p reports
          cp .harness/quality/* reports/ || true

      - name: 上传报告
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: quality-reports
          path: reports/

  harness-deploy:
    runs-on: ubuntu-latest
    needs: harness-check
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v3

      - name: 安装 Harness
        run: |
          curl -fsSL https://raw.githubusercontent.com/PIGU-PPPgu/harness-skill-v2/main/install.sh | bash
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: 部署
        env:
          DEPLOY_KEY: ${{ secrets.DEPLOY_KEY }}
        run: |
          # 这里会调用 DevOps 智能体进行部署
          echo "部署到生产环境..."
```

## GitLab CI

创建 `.gitlab-ci.yml`:

```yaml
stages:
  - check
  - test
  - deploy

variables:
  HARNESS_VERSION: "2.0.0"

before_script:
  - curl -fsSL https://raw.githubusercontent.com/PIGU-PPPgu/harness-skill-v2/main/install.sh | bash
  - export PATH="$HOME/.local/bin:$PATH"

harness-audit:
  stage: check
  script:
    - harness audit
    - harness enforce --check
  artifacts:
    paths:
      - .harness/quality/
    expire_in: 1 week
  only:
    - main
    - develop
    - merge_requests

harness-test:
  stage: test
  script:
    - harness swarm start --ci-mode
    - harness swarm wait
  artifacts:
    reports:
      junit: .harness/quality/test-report.xml
  only:
    - main
    - develop

harness-deploy:
  stage: deploy
  script:
    - echo "部署到生产环境..."
  environment:
    name: production
  only:
    - main
  when: manual
```

## Jenkins

创建 `Jenkinsfile`:

```groovy
pipeline {
  agent any

  environment {
    HARNESS_HOME = "${HOME}/.local/bin"
  }

  stages {
    stage('Setup') {
      steps {
        sh '''
          curl -fsSL https://raw.githubusercontent.com/PIGU-PPPgu/harness-skill-v2/main/install.sh | bash
          export PATH="${HARNESS_HOME}:$PATH"
        '''
      }
    }

    stage('Quality Check') {
      steps {
        sh '''
          export PATH="${HARNESS_HOME}:$PATH"
          harness audit
          harness enforce --check
        '''
      }
    }

    stage('Test') {
      steps {
        sh '''
          export PATH="${HARNESS_HOME}:$PATH"
          harness swarm start --ci-mode
          harness swarm wait
        '''
      }
      post {
        always {
          junit '.harness/quality/test-report.xml'
          archiveArtifacts artifacts: '.harness/quality/**/*', allowEmptyArchive: true
        }
      }
    }

    stage('Deploy') {
      when {
        branch 'main'
      }
      steps {
        input message: '确认部署到生产环境?'
        sh '''
          export PATH="${HARNESS_HOME}:$PATH"
          echo "部署到生产环境..."
        '''
      }
    }
  }

  post {
    always {
      cleanWs()
    }
    success {
      echo '✅ Pipeline 执行成功'
    }
    failure {
      echo '❌ Pipeline 执行失败'
    }
  }
}
```

## CircleCI

创建 `.circleci/config.yml`:

```yaml
version: 2.1

executors:
  harness-executor:
    docker:
      - image: cimg/node:18.0
    working_directory: ~/project

jobs:
  quality-check:
    executor: harness-executor
    steps:
      - checkout
      - run:
          name: 安装 Harness
          command: |
            curl -fsSL https://raw.githubusercontent.com/PIGU-PPPgu/harness-skill-v2/main/install.sh | bash
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> $BASH_ENV

      - run:
          name: 质量审计
          command: harness audit

      - run:
          name: 架构检查
          command: harness enforce --check

      - store_artifacts:
          path: .harness/quality
          destination: quality-reports

  test:
    executor: harness-executor
    steps:
      - checkout
      - run:
          name: 安装 Harness
          command: |
            curl -fsSL https://raw.githubusercontent.com/PIGU-PPPgu/harness-skill-v2/main/install.sh | bash
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> $BASH_ENV

      - run:
          name: 运行测试
          command: |
            harness swarm start --ci-mode
            harness swarm wait

      - store_test_results:
          path: .harness/quality

  deploy:
    executor: harness-executor
    steps:
      - checkout
      - run:
          name: 部署
          command: echo "部署到生产环境..."

workflows:
  version: 2
  build-test-deploy:
    jobs:
      - quality-check
      - test:
          requires:
            - quality-check
      - deploy:
          requires:
            - test
          filters:
            branches:
              only: main
```

## Travis CI

创建 `.travis.yml`:

```yaml
language: node_js
node_js:
  - "18"

before_install:
  - curl -fsSL https://raw.githubusercontent.com/PIGU-PPPgu/harness-skill-v2/main/install.sh | bash
  - export PATH="$HOME/.local/bin:$PATH"

script:
  - harness audit
  - harness enforce --check
  - harness swarm start --ci-mode
  - harness swarm wait

after_success:
  - |
    if [ "$TRAVIS_BRANCH" = "main" ]; then
      echo "部署到生产环境..."
    fi

cache:
  directories:
    - node_modules
    - $HOME/.local/bin
```

## 自定义 CI/CD 脚本

创建 `scripts/ci.sh`:

```bash
#!/usr/bin/env bash

set -euo pipefail

echo "🚀 开始 CI/CD 流程..."

# 1. 质量检查
echo "📊 执行质量审计..."
harness audit

# 2. 架构约束检查
echo "🏗️ 检查架构约束..."
harness enforce --check

# 3. 运行测试
echo "🧪 运行测试..."
harness swarm start --ci-mode
harness swarm wait

# 4. 生成报告
echo "📝 生成报告..."
harness docs generate

# 5. 部署（仅在 main 分支）
if [ "${CI_BRANCH:-}" = "main" ]; then
    echo "🚢 部署到生产环境..."
    # 部署逻辑
fi

echo "✅ CI/CD 流程完成!"
```

## Docker 集成

创建 `Dockerfile.ci`:

```dockerfile
FROM node:18-alpine

# 安装 Harness
RUN apk add --no-cache curl bash && \
    curl -fsSL https://raw.githubusercontent.com/PIGU-PPPgu/harness-skill-v2/main/install.sh | bash

ENV PATH="/root/.local/bin:${PATH}"

WORKDIR /app

COPY . .

# 运行 CI 检查
RUN harness audit && \
    harness enforce --check

CMD ["harness", "swarm", "start", "--ci-mode"]
```

使用:
```bash
docker build -f Dockerfile.ci -t my-app-ci .
docker run my-app-ci
```

## 质量门禁配置

创建 `.harness/quality-gates.json`:

```json
{
  "gates": [
    {
      "name": "测试覆盖率",
      "metric": "coverage",
      "threshold": 80,
      "operator": ">=",
      "blocking": true
    },
    {
      "name": "Lint 错误",
      "metric": "lint_errors",
      "threshold": 0,
      "operator": "==",
      "blocking": true
    },
    {
      "name": "架构违规",
      "metric": "architecture_violations",
      "threshold": 0,
      "operator": "==",
      "blocking": true
    },
    {
      "name": "API 响应时间",
      "metric": "api_response_time_p95",
      "threshold": 100,
      "operator": "<=",
      "blocking": false
    }
  ]
}
```

## 通知集成

### Slack 通知

创建 `.harness/notifications/slack.json`:

```json
{
  "webhook_url": "https://hooks.slack.com/services/YOUR/WEBHOOK/URL",
  "channel": "#deployments",
  "events": [
    "deployment_started",
    "deployment_completed",
    "deployment_failed",
    "quality_gate_failed"
  ],
  "template": {
    "deployment_completed": {
      "text": "✅ 部署成功",
      "blocks": [
        {
          "type": "section",
          "text": {
            "type": "mrkdwn",
            "text": "*部署成功* :rocket:\n环境: {{environment}}\n版本: {{version}}"
          }
        }
      ]
    }
  }
}
```

### Email 通知

创建 `.harness/notifications/email.json`:

```json
{
  "smtp": {
    "host": "smtp.gmail.com",
    "port": 587,
    "secure": false,
    "auth": {
      "user": "your-email@gmail.com",
      "pass": "your-password"
    }
  },
  "recipients": [
    "team@example.com"
  ],
  "events": [
    "deployment_failed",
    "quality_gate_failed"
  ]
}
```

## 监控集成

### Prometheus

创建 `.harness/monitoring/prometheus.yml`:

```yaml
scrape_configs:
  - job_name: 'harness'
    static_configs:
      - targets: ['localhost:9090']
    metrics_path: '/metrics'
    scrape_interval: 15s
```

### Grafana Dashboard

创建 `.harness/monitoring/grafana-dashboard.json`:

```json
{
  "dashboard": {
    "title": "Harness Engineering Metrics",
    "panels": [
      {
        "title": "部署频率",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(harness_deployments_total[1h])"
          }
        ]
      },
      {
        "title": "质量指标",
        "type": "stat",
        "targets": [
          {
            "expr": "harness_test_coverage_percent"
          }
        ]
      }
    ]
  }
}
```

## 最佳实践

### 1. 分支策略
- `main`: 生产环境，自动部署
- `develop`: 开发环境，自动部署
- `feature/*`: 功能分支，仅运行测试

### 2. 质量门禁
- 所有 PR 必须通过质量审计
- 测试覆盖率不低于 80%
- 无架构违规

### 3. 部署策略
- 使用蓝绿部署或金丝雀部署
- 自动回滚失败的部署
- 保留最近 5 个版本

### 4. 监控告警
- 部署失败立即告警
- 质量指标下降告警
- 性能指标异常告警
