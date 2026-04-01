# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-04-01

### 🔄 重大重构 - 回归 OpenAI 原文精神

基于 Codex 深度评估，发现我们严重误读了 OpenAI 的 Harness Engineering 文章。本次更新完全重构了项目定位和实现方向。

### Changed
- **核心理念**：从"零人工干预"改为"Humans steer. Agents execute."
- **项目定位**：从"通用自动化框架"改为"仓库改造方法论"
- **README**：完全重写，纠正对 OpenAI 原文的误读
- **文档**：去除所有"零干预""全自动"等误导性表述

### 重构进行中（实现层尚未完成）
- 顶层定位已重写，但 CLI 实现仍在重构中
- 旧的 `swarm/tasks/agent` 命令体系正在被替换为单主循环
- examples/ 目录的旧示例待更新

### 已开始实现
- `src/harness_runtime.py`：真正的执行计划管理和 Git 集成
- `src/agent_loop.py`：单主循环 agent 框架
- `harness run`：新的主入口命令（替代 `swarm start`）
- `harness plan create`：创建执行计划

### 核心发现（来自 Codex 评估）

**我们的四层误读**：
1. 把"零手写代码"误读成"零人工干预"
2. 把"team of agents"误读成"固定七角色流水线"
3. 把"repo-specific harness engineering"误读成"可安装的通用自治开发框架"
4. 把 OpenAI 的内部结果当成通用营销指标外推

**OpenAI 原文真正说的是**：
- "Humans always remain in the loop"（人类始终在环）
- 人类负责：目标、优先级、验收、架构决策、风险判断
- Agent 负责：写代码、测试、PR、响应 review
- 强依赖于特定仓库的结构和工具，不能泛化

**当前实现的问题**：
- 所有命令都是空壳，只打印硬编码输出
- 没有真正的 agent runtime
- 没有 Git/PR 集成
- 没有 CI/CD 流水线
- 本质上是"概念文档 + 演示脚本"

### Next Steps

需要重新实现：
1. 单主循环（不是多角色流水线）
2. 结构化知识系统（docs/）
3. 可执行环境（worktree、浏览器、日志）
4. 机械化约束（custom lint、CI）
5. Execution plan 作为一等公民
6. 持续 garbage collection

## [2.0.0] - 2026-01-15

### Added
- 零干预智能体团队系统（已证实为误读）
- 7 个自主智能体角色（不符合原文）
- PRD 驱动的开发流程（过度解读）
- 自动审批模式（原文未提及）
- 智能体间直接通信协议
- 执行计划跟踪系统
- 架构决策记录 (ADR)
- 质量审计工具
- 架构约束强制执行
- CI/CD 集成支持
- 实时日志监控
- 任务管理系统

### Changed
- 从工具优先改为智能体优先的架构（误读）
- 扩展了原有的 4 个智能体角色到 7 个（不符合原文）
- 增强了自动化程度，减少人工干预（与原文相反）

### Features
- `harness init` - 初始化项目结构
- `harness swarm start` - 启动智能体团队
- `harness swarm status` - 查看智能体状态
- `harness swarm stop/pause/resume` - 控制智能体
- `harness tasks list` - 查看任务列表
- `harness agent logs` - 查看智能体日志
- `harness audit` - 质量审计
- `harness enforce` - 架构约束检查
- `harness docs generate` - 生成文档
- `harness garden` - 代码清理

**注**：以上功能大部分是空壳实现，不执行真实操作。

## [1.0.0] - 2025-12-01

### Added
- 初始版本
- 基础架构约束检查
- 质量标准定义
- Golden Rules 系统
