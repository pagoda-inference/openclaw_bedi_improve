# OpenClaw 市场调研能力扩展规划

## 零、准备工作：分支创建与迁移

### 0.1 当前状态

- 当前分支：`main`
- 未跟踪文件：`.trae/`、`openclaw-research-scenario/`
- 本地分支落后于 upstream/main 140 个提交

### 0.2 分支创建步骤

```bash
# 1. 先同步 main 分支
git fetch upstream
git pull upstream main

# 2. 创建新分支
git checkout -b feature/market-research-capability

# 3. 添加现有设计文件
git add openclaw-research-scenario/
git add .trae/

# 4. 提交设计文档
git commit -m "docs: add market research capability design documents"
```

### 0.3 分支命名

`feature/market-research-capability` - 市场调研能力扩展分支

---

## 一、OpenClaw 可扩展点概览

| 类型 | 文件/配置 | 扩展方式 |
|------|----------|---------|
| Bootstrap | `AGENTS.md` | 添加市场调研操作指令 |
| Bootstrap | `SOUL.md` | 定义市场调研 persona |
| Bootstrap | `TOOLS.md` | 添加市场调研工具说明 |
| Bootstrap | `memory/` | 存储市场调研记忆 |
| Skills | `.agents/skills/*/SKILL.md` | 定义独立 Skill |
| Plugin | `src/plugins/market-research/` | 注册 Tool |
| Hook | `src/hooks/bundled/` 或 Plugin Hook | 监听事件、注入逻辑 |
| Config | `openclaw.json` | 配置 agents 默认值 |

---

## 二、Skill 设计（4 个独立 Skill）

### 2.1 Skill 列表

| Skill | 触发状态 | 完成状态 |
|-------|---------|---------|
| market-research-planner | pending | planning_completed |
| market-research-collector | planning_completed | collection_completed |
| market-research-processor | collection_completed | processing_completed |
| market-research-reporter | processing_completed | completed |

### 2.2 状态机

```
pending → planning_completed → collection_completed → processing_completed → completed
```

### 2.3 Skill 文件位置

```
.agents/skills/
├── market-research-planner/
│   └── SKILL.md
├── market-research-collector/
│   └── SKILL.md
├── market-research-processor/
│   └── SKILL.md
└── market-research-reporter/
    └── SKILL.md
```

---

## 三、Plugin Tool 设计（7 个 Tool）

### 3.1 Tool 列表

| Tool | 功能 | 类型 |
|------|------|------|
| task_manager | 任务创建/更新/查询/恢复 | 任务管理 |
| data_cleaner | 文本清理（去HTML、广告、标准化） | 数据处理 |
| data_cleanser | 数据验证（格式、范围、去重） | 数据处理 |
| data_analyzer | 统计分析（计数、求和、趋势） | 数据处理 |
| report_organizer | 按模板组织报告内容 | 报告生成 |
| report_renderer | 渲染 HTML 报告 | 报告生成 |
| deep_browser | OpenCLI 浏览器操作封装 | 浏览器 |

### 3.2 Plugin 文件位置

```
src/plugins/market-research/
├── openclaw.plugin.json
├── src/
│   ├── index.ts
│   └── tools/
│       ├── task-manager.ts
│       ├── data-cleaner.ts
│       ├── data-cleanser.ts
│       ├── data-analyzer.ts
│       ├── report-organizer.ts
│       ├── report-renderer.ts
│       └── deep-browser.ts
└── dist/
```

---

## 四、Hook 机制利用

### 4.1 可用事件类型

| 事件类型 | 触发时机 | 可用于市场调研 |
|---------|---------|---------------|
| `command:new` | `/new` 命令 | 清理上一个任务状态 |
| `command:reset` | `/reset` 命令 | 重置任务目录 |
| `agent:bootstrap` | Agent 启动时 | 注入市场调研配置 |
| `gateway:startup` | Gateway 启动时 | 初始化任务管理器 |
| `session:start` | 会话开始 | 恢复未完成任务 |

### 4.2 推荐的 Hook 设计

#### Hook 1: task-recovery

**目的**：在 Gateway 启动或会话恢复时，自动检测并恢复未完成的任务

**事件**：`gateway:startup`, `session:start`

**逻辑**：
1. 扫描 `~/.openclaw/tasks/` 目录
2. 找到 status 不是 "completed" 的任务
3. 加载任务状态和记忆
4. 通知用户有未完成任务

```
src/hooks/bundled/task-recovery/
├── HOOK.md
└── handler.ts
```

#### Hook 2: research-memory-persist

**目的**：在任务完成或中断时，自动保存关键记忆到 workspace memory/

**事件**：`command:new`, `command:reset`

**逻辑**：
1. 检查当前是否有活跃任务
2. 提取关键发现和数据点
3. 写入 `memory/YYYY-MM-DD-research-{topic}.md`

### 4.3 Plugin Hook 注册

在 Plugin 中注册 Hook：

```typescript
// src/plugins/market-research/src/index.ts
export function register(api: OpenClawPluginApi): void {
  // 注册 Tool
  api.registerTool(new TaskManagerTool());
  // ...

  // 注册 Hook（可选）
  api.registerHook({
    name: "task-recovery",
    events: ["gateway:startup", "session:start"],
    handler: async (event) => {
      // 恢复未完成任务
    }
  });
}
```

---

## 五、任务目录结构

```
~/.openclaw/tasks/{task-id}/
├── task.json              # 任务元信息 + 状态
├── config.json            # 任务配置
├── plan.json              # 调研计划
├── data/
│   ├── raw/               # 原始数据
│   ├── processed/         # 处理后数据
│   └── analysis/          # 分析结果
├── memory/
│   ├── operations.json    # 操作历史
│   └── visited.json       # 已访问 URL
├── output/
│   └── report.html        # 最终报告
└── logs/
    └── task.log
```

---

## 六、测试与验证方案

### 6.1 单元测试

**位置**：`src/plugins/market-research/src/tools/*.test.ts`

**覆盖内容**：
- 每个 Tool 的独立功能测试
- 输入验证测试
- 边界条件测试
- 错误处理测试

**示例**：
```
src/plugins/market-research/src/tools/
├── task-manager.ts
├── task-manager.test.ts      # 单元测试
├── data-cleaner.ts
├── data-cleaner.test.ts      # 单元测试
└── ...
```

**运行命令**：`pnpm test src/plugins/market-research/`

### 6.2 集成测试

**位置**：`src/plugins/market-research/*.integration.test.ts`

**覆盖内容**：
- Tool 之间的协作
- 任务状态流转
- 数据处理管道

**测试场景**：
1. 创建任务 → 规划 → 完成
2. 数据清理 → 验证 → 分析
3. 内容组织 → 渲染 → 输出

### 6.3 E2E 测试

**位置**：`src/plugins/market-research/*.e2e.test.ts`

**覆盖内容**：
- 完整的市场调研流程
- Skill 触发和状态流转
- 报告生成端到端

**测试场景**：
1. 用户发起调研请求 → 生成报告
2. 任务中断 → 恢复 → 继续
3. 多任务并行执行

**运行命令**：`pnpm test:e2e src/plugins/market-research/`

### 6.4 QA 场景测试

**位置**：`qa/scenarios/market-research/`

**场景文件**：
```
qa/scenarios/market-research/
├── quick-research-baseline.md      # 快速调研基准测试
├── deep-research-interrupt.md      # 深度调研中断恢复
├── multi-task-parallel.md          # 多任务并行
└── report-quality-check.md         # 报告质量检查
```

**运行命令**：`pnpm openclaw qa suite --scenario quick-research-baseline`

### 6.5 测试优先级

| 阶段 | 测试类型 | 覆盖目标 |
|------|---------|---------|
| 阶段一 | 单元测试 | 7 个 Tool 的核心功能 |
| 阶段二 | 集成测试 | Tool 协作、状态流转 |
| 阶段三 | E2E 测试 | 完整流程、Skill 触发 |
| 阶段四 | QA 场景 | 真实场景验证 |

---

## 七、各 Skill 详细设计

### 7.1 market-research-planner

**触发条件**：task_manager 创建任务后，状态为 "pending"

**工作流程**：
1. 读取 task.json 获取用户需求
2. 使用 LLM 分析需求，分解为子主题
3. 生成 plan.json
4. 更新 task.json 状态为 "planning_completed"

**使用的 Tool**：read, write, task_manager

---

### 7.2 market-research-collector

**触发条件**：task.json 状态为 "planning_completed"

**工作流程**：
1. 读取 plan.json 获取子主题
2. 对每个子主题：搜索关键词 → 访问页面 → 提取内容
3. 存储到 data/raw/
4. 更新 task.json 状态为 "collection_completed"

**使用的 Tool**：read, write, web_search, deep_browser, task_manager

---

### 7.3 market-research-processor

**触发条件**：task.json 状态为 "collection_completed"

**工作流程**：
1. 读取 data/raw/ 下的原始数据
2. 使用 data_cleaner 清理文本
3. 使用 LLM 提取结构化数据
4. 使用 data_cleanser 验证数据
5. 使用 data_analyzer 分析数据
6. 存储到 data/analysis/
7. 更新 task.json 状态为 "processing_completed"

**使用的 Tool**：read, write, data_cleaner, data_cleanser, data_analyzer, task_manager

---

### 7.4 market-research-reporter

**触发条件**：task.json 状态为 "processing_completed"

**工作流程**：
1. 读取 data/analysis/ 和 plan.json
2. 使用 LLM 选择报告模板
3. 使用 report_organizer 组织内容
4. 使用 report_renderer 渲染 HTML
5. 存储到 output/report.html
6. 更新 task.json 状态为 "completed"

**使用的 Tool**：read, write, report_organizer, report_renderer, task_manager

---

## 八、Bootstrap 文件扩展

### 8.1 AGENTS.md 扩展

在现有 AGENTS.md 中添加市场调研操作指令：

```markdown
## 市场调研能力

当用户请求市场调研、行业分析、竞品研究时：

1. 使用 task_manager 创建任务
2. 根据任务状态自动触发对应 Skill
3. 跟踪进度直到报告生成完成
```

### 8.2 TOOLS.md 扩展

添加市场调研相关工具的使用说明。

---

## 九、文件清单汇总

### 9.1 Skills（4 个）

| 文件路径 | 用途 |
|---------|------|
| `.agents/skills/market-research-planner/SKILL.md` | 调研规划 |
| `.agents/skills/market-research-collector/SKILL.md` | 数据采集 |
| `.agents/skills/market-research-processor/SKILL.md` | 数据处理 |
| `.agents/skills/market-research-reporter/SKILL.md` | 报告生成 |

### 9.2 Plugin（9 个文件）

| 文件路径 | 用途 |
|---------|------|
| `src/plugins/market-research/openclaw.plugin.json` | Plugin 清单 |
| `src/plugins/market-research/src/index.ts` | Plugin 入口 |
| `src/plugins/market-research/src/tools/task-manager.ts` | 任务管理 |
| `src/plugins/market-research/src/tools/data-cleaner.ts` | 文本清理 |
| `src/plugins/market-research/src/tools/data-cleanser.ts` | 数据验证 |
| `src/plugins/market-research/src/tools/data-analyzer.ts` | 数据分析 |
| `src/plugins/market-research/src/tools/report-organizer.ts` | 内容组织 |
| `src/plugins/market-research/src/tools/report-renderer.ts` | HTML 渲染 |
| `src/plugins/market-research/src/tools/deep-browser.ts` | 浏览器操作 |

### 9.3 测试文件

| 文件路径 | 用途 |
|---------|------|
| `src/plugins/market-research/src/tools/*.test.ts` | 单元测试 |
| `src/plugins/market-research/*.integration.test.ts` | 集成测试 |
| `src/plugins/market-research/*.e2e.test.ts` | E2E 测试 |
| `qa/scenarios/market-research/*.md` | QA 场景 |

### 9.4 Hook 文件（可选）

| 文件路径 | 用途 |
|---------|------|
| `src/hooks/bundled/task-recovery/HOOK.md` | 任务恢复 Hook |
| `src/hooks/bundled/task-recovery/handler.ts` | Hook 实现 |

### 9.5 Bootstrap 扩展

| 文件路径 | 扩展内容 |
|---------|---------|
| `~/.openclaw/workspace/AGENTS.md` | 市场调研操作指令 |
| `~/.openclaw/workspace/TOOLS.md` | 工具使用说明 |

---

## 十、实施优先级

### 准备阶段：分支创建

1. 同步 main 分支：`git pull upstream main`
2. 创建新分支：`git checkout -b feature/market-research-capability`
3. 添加设计文件：`git add openclaw-research-scenario/ .trae/`
4. 提交：`git commit -m "docs: add market research capability design documents"`

### 阶段一：基础能力（MVP）+ 单元测试

1. 实现 task_manager Tool + 单元测试
2. 实现 report_renderer Tool + 单元测试
3. 创建 market-research-planner Skill
4. 创建 market-research-reporter Skill
5. 扩展 AGENTS.md
6. **验证**：单元测试通过

### 阶段二：数据处理 + 集成测试

7. 实现 data_cleaner Tool + 单元测试
8. 实现 data_cleanser Tool + 单元测试
9. 实现 data_analyzer Tool + 单元测试
10. 创建 market-research-processor Skill
11. 编写集成测试
12. **验证**：集成测试通过

### 阶段三：数据采集 + E2E 测试

13. 实现 deep_browser Tool（OpenCLI 封装）+ 单元测试
14. 创建 market-research-collector Skill
15. 编写 E2E 测试
16. 编写 QA 场景
17. **验证**：E2E 测试通过、QA 场景通过

### 阶段四：Hook 机制（可选）

18. 实现 task-recovery Hook
19. 实现 research-memory-persist Hook
20. **验证**：Hook 功能测试通过
