# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-01-15

### Added
- 零干预智能体团队系统
- 7 个自主智能体角色 (Coordinator, Architect, Builder, Reviewer, Tester, Doc Writer, DevOps)
- PRD 驱动的开发流程
- 自动审批模式
- 智能体间直接通信协议
- 执行计划跟踪系统
- 架构决策记录 (ADR)
- 质量审计工具
- 架构约束强制执行
- CI/CD 集成支持
- 实时日志监控
- 任务管理系统

### Changed
- 从工具优先改为智能体优先的架构
- 扩展了原有的 4 个智能体角色到 7 个
- 增强了自动化程度，减少人工干预

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

## [1.0.0] - 2024-01-01

### Added
- 初始版本
- 基础架构约束检查
- 质量标准定义
- Golden Rules 系统
