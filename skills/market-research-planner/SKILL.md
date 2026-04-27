---
name: market-research-planner
description: "市场调研任务规划，将用户需求分解为可执行的子主题"
trigger: 当 task_manager 创建任务后，状态为 "pending" 且任务类型为 "market_research" 时激活
---

# 调研规划 Skill

## 工作流程

### Step 1: 读取任务信息
读取 task.json 获取用户原始需求。

### Step 2: 需求分析与主题分解
使用 LLM 分析用户需求，输出 JSON 格式的 plan.json：

```json
{
  "topic": "用户需求的简短主题",
  "research_type": "quick | standard | deep",
  "sub_topics": [
    {
      "name": "子主题名称",
      "core_question": "核心问题",
      "keywords": ["关键词1", "关键词2"],
      "priority": 1-5,
      "status": "pending"
    }
  ],
  "estimated_duration_minutes": 预估时长
}
```

### Step 3: 保存 plan.json
在任务目录下创建 plan.json。

### Step 4: 更新任务状态
更新 task.json 状态为 "planning_completed"。

## 使用的 Tool

- read: 读取 task.json
- write: 写入 plan.json
- task_manager: 更新任务状态

## 输出

- 任务目录下生成 plan.json
- task.json 状态更新为 "planning_completed"

## 触发下一个 Skill

当 task.json 状态变为 "planning_completed" 后，market-research-collector Skill 将自动激活。
