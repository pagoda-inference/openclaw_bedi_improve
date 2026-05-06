---
name: deep-browser
description: "网站探索器：给定需求，在网站中寻找数据所在位置、获取数据、形成记忆。通过交互发现网站完整结构，输出探索报告和适配器建议。"
user-invocable: false
allowed-tools: Bash(opencli:*), Read, Write, Edit
---

# Deep Browser Skill

网站探索器：给定需求，在网站中寻找数据所在位置、获取数据、形成记忆。

## 核心诉求

给定一个相对抽象模糊的需求（或精细的需求），在一个网站中：

1. **找到数据在哪里** — 数据在哪些页面？通过什么交互才能到达？
2. **获取数据** — 数据是 API 返回的还是页面渲染的？怎么提取？
3. **形成记忆** — 网站结构、数据分布、交互模式，供后续复用

## 浏览器后端

使用 OpenCLI 的 browser 命令操作浏览器。OpenCLI 复用用户已登录的 Chrome，具备反检测能力。

```bash
# 环境检查
opencli doctor

# 站点分析（一步完成分类 + 反爬检测）
opencli browser analyze <url>

# 页面操作
opencli browser open <url>          # 打开页面
opencli browser state               # 获取页面快照（带 [N] 元素引用）
opencli browser find --css <sel>    # CSS 查找元素
opencli browser click <target>      # 点击元素
opencli browser type <target> <text># 输入文本
opencli browser scroll <direction>  # 滚动页面
opencli browser select <target> <opt># 选择下拉选项
opencli browser keys <key>          # 按键

# 数据获取
opencli browser get title           # 获取标题
opencli browser get url             # 获取 URL
opencli browser get text <target>   # 获取元素文本
opencli browser get value <target>  # 获取表单值
opencli browser extract             # 提取页面内容（分块）

# 网络分析
opencli browser network             # 列出网络请求（带 shape 预览）
opencli browser network --detail <key>  # 获取完整响应体
opencli browser network --filter "f1,f2" # 按字段过滤

# 等待
opencli browser wait selector "<css>" # 等待元素出现
opencli browser wait text "<text>"    # 等待文本出现

# 标签页
opencli browser tab list            # 列出标签页
opencli browser tab new [url]       # 新建标签页
opencli browser tab close [id]      # 关闭标签页
```

### 降级方案

当 OpenCLI 不可用时：

| 优先级 | 方案 | 能力 |
|--------|------|------|
| 1 | OpenCLI | 完整：交互 + 网络分析 + 登录态 |
| 2 | OpenClaw browser tool | 部分：交互可用，无登录态 |
| 3 | web-fetch + web-search | 受限：仅静态内容 |

## ⚠️ 只读约束

**本技能以只读方式操作网站，禁止任何写入行为。**

### 允许的操作

- ✅ 点击导航链接 → 进入新页面
- ✅ 展开折叠菜单 → 显示隐藏内容
- ✅ 滚动页面 → 加载更多条目
- ✅ 切换标签页 → 查看不同分类
- ✅ 搜索输入 → 获取搜索结果
- ✅ 分页导航 → 获取更多列表条目
- ✅ 筛选/排序 → 改变内容展示方式

### 禁止的操作

- ❌ 提交注册/登录表单
- ❌ 提交联系/反馈表单
- ❌ 购买/下单/删除操作
- ❌ 修改/编辑已有数据
- ❌ 发布/上传内容

**判断标准**：操作目的是获取/展示信息 → 允许；操作目的是创建/修改数据 → 禁止。

## 何时使用

✅ **使用此技能当：**

- 需要在一个网站中找到特定数据在哪里
- 需要通过交互才能发现隐藏内容
- 需要理解网站的完整结构和数据分布
- 需要发现 API 端点和数据获取方式
- 需要积累网站知识供后续复用

❌ **不使用此技能当：**

- 简单的静态页面抓取 → 用 web-fetch
- 已知 API 直接获取数据 → 直接调用 API
- 需要提交表单完成任务 → 本技能禁止写入

## 工作流

### Phase 1：预检

```
1. opencli doctor
   └─ 检查环境是否就绪

2. opencli browser analyze <url>
   └─ 一步获取：
      ├─ Pattern 分类（A/B/C/D/E）
      ├─ 反爬检测
      ├─ SSR 全局变量检测
      └─ 下一步建议

3. 读取站点记忆
   ├─ ~/.opencli/sites/<site>/endpoints.json
   ├─ ~/.opencli/sites/<site>/field-map.json
   └─ ~/.opencli/sites/<site>/notes.md
   └─ 命中 → 跳到 Phase 3 验证
   └─ 未命中 → 继续 Phase 2
```

### Phase 2：探索

根据 Pattern 选择策略：

| Pattern | 站点类型 | 探索策略 |
|---------|---------|---------|
| A | SPA / JSON XHR | network 优先，发现 API 端点 |
| B | SSR / inline data | state 抽取 + network 深层数据 |
| C | JSONP / script src | bundle 搜索 + HTML 提取 |
| D | Token / CSRF | token 排查 + 降级 |
| E | 流式 | 找 HTTP 轮询接口 |

**逐层探索**：

```
1. opencli browser open <url>
2. opencli browser state → 获取页面快照
3. 分析快照，识别：
   ├─ 导航入口 → 记录 URL
   ├─ 展示交互 → 执行交互，发现隐藏内容
   ├─ 搜索/筛选 → 执行获取结果
   └─ 写入操作 → 记录入口，不执行
4. opencli browser network → 发现 API 端点
5. 对发现的每个新 URL，重复步骤 1-4
6. 直到覆盖所有可访问内容
```

**关键命令组合**：

```bash
# 打开页面 + 获取快照 + 查看网络
opencli browser open "https://example.com" \
  && opencli browser state \
  && opencli browser network

# 交互后重新获取状态
opencli browser click 3 \
  && opencli browser wait selector ".content" \
  && opencli browser state

# 滚动加载更多
opencli browser scroll down \
  && opencli browser wait time 2 \
  && opencli browser state

# 搜索
opencli browser type 5 "关键词" \
  && opencli browser keys Enter \
  && opencli browser wait text "搜索结果" \
  && opencli browser state
```

### Phase 3：记忆

将探索结果写入站点记忆：

```
~/.opencli/sites/<site>/
  endpoints.json     — 发现的 API 端点
  field-map.json     — 字段代号 → 含义
  notes.md           — 探索笔记
  structure.md       — 网站结构（页面层级、导航入口）
```

### Phase 4：输出

输出探索报告，包含：

```markdown
# 网站探索报告

## 需求
{用户的需求}

## 站点信息
- URL: {url}
- Pattern: {A/B/C/D/E}
- 反爬: {检测结果}

## 数据位置
| 数据 | 所在页面 | 获取方式 | API 端点 |
|------|---------|---------|---------|
| {数据1} | /products | 列表页 | GET /api/products |
| {数据2} | /products/{id} | 详情页 | GET /api/products/{id} |

## 网站结构
{页面层级图}

## 适配器建议
- Strategy: PUBLIC / COOKIE / HEADER
- 推荐端点: {endpoint}
- 字段映射: {field_map}
```

## 相关 Skill

本 Skill 专注**探索阶段**，以下 Skill 在流程的其他阶段发挥作用。Agent 可根据需要切换。

### opencli-browser

**用途**：浏览器操作参考文档

当需要查阅 `opencli browser *` 命令的详细说明时参考此 Skill。本 Skill 的浏览器操作命令均来自 opencli-browser 的定义。

- 命令语法、参数、返回格式
- match_level 容错机制
- Compound 表单控件信息
- 标签页管理和 lease 生命周期

### opencli-adapter-author

**用途**：将探索结果沉淀为可复用 CLI 适配器

当 Deep Browser 完成探索、输出适配器建议后，Agent 可切换到此 Skill 将建议落地为实际的 CLI 命令。

**衔接方式**：
- Deep Browser 输出 → 探索报告 + 适配器建议（Strategy、endpoint、字段映射）
- opencli-adapter-author 接收 → 编写适配器代码 → `opencli browser verify` 验证

**关键流程**：
```
Deep Browser 探索报告
  ├─ Pattern 分类 → adapter-author 的 site-recon 决策树输入
  ├─ endpoints.json → adapter-author 的 endpoint 验证输入
  ├─ field-map.json → adapter-author 的字段解码输入
  └─ 适配器建议 → adapter-author 的 Strategy 选择依据
```

### opencli-usage

**用途**：OpenCLI 命令总览和站点发现

当需要了解 OpenCLI 有哪些可用命令、已有哪些站点适配器时参考此 Skill。

- `opencli list` — 查看所有已安装的适配器
- `opencli <site> -h` — 查看站点子命令
- Strategy 标签（PUBLIC/COOKIE/HEADER/INTERCEPT/UI/LOCAL）

**使用场景**：探索前先检查目标站点是否已有适配器，避免重复探索。

### opencli-autofix

**用途**：修复已损坏的适配器

当基于 Deep Browser 探索结果生成的适配器在后续使用中失败时，使用此 Skill 自动诊断和修复。

- SELECTOR 错误 → DOM 变化
- EMPTY_RESULT → API 响应变化
- API_ERROR → 端点迁移

### smart-search

**用途**：智能搜索路由

当用户需求比较模糊时，先用此 Skill 路由到最佳搜索源，找到目标网站后再用 Deep Browser 深入探索。

**衔接方式**：
```
用户模糊需求 → smart-search 找到目标网站列表 → Deep Browser 深入探索
```

### 协作流程图

```
用户需求
  │
  ├─ 模糊需求？ → smart-search → 找到目标网站
  │
  ▼
deep-browser（本 Skill）
  ├─ 探索网站结构
  ├─ 发现 API 端点
  ├─ 形成站点记忆
  └─ 输出探索报告 + 适配器建议
  │
  ├─ 需要沉淀为 CLI？ → opencli-adapter-author
  │                         ├─ 编写适配器
  │                         └─ opencli browser verify
  │
  ├─ 适配器后续损坏？ → opencli-autofix
  │
  └─ 需要查阅命令？ → opencli-usage / opencli-browser
```

## 参考文档

| 文档 | 用途 |
|------|------|
| [站点侦察](reference/site_recon.md) | Pattern A/B/C/D/E 分类和对应策略 |
| [站点记忆](reference/site_memory.md) | 记忆格式和读写时机 |
| [浏览器操作参考](reference/browser_operations_reference.md) | OpenCLI 命令详细说明 |
| [页面分析](reference/page_analysis.md) | 页面结构分析方法 |
| [元素分析](reference/element_analysis.md) | 元素交互性和安全性判断 |
| [网络分析](reference/network_analysis.md) | API 发现和数据源识别 |
| [页面状态模板](reference/page_state_template.md) | 状态文件标准格式 |

## Python 辅助脚本

`scripts/` 目录提供辅助功能（非浏览器操作）：

- `file_operations.py` — 状态文件读写
- `memory_manager.py` — 站点记忆管理
- `init_environment.py` — 环境初始化（检查 opencli 可用性）

## 最佳实践

1. **先 analyze 再探索** — `opencli browser analyze` 一步完成分类
2. **先 state 再操作** — 每次操作前获取快照，操作后重新获取
3. **network 优先于 DOM** — API 数据比页面抓取更可靠
4. **交互前判断安全性** — 只执行只读操作
5. **链式调用** — 用 `&&` 连接命令，保持会话上下文
6. **及时写记忆** — 探索完成后立即写入站点记忆
7. **输出适配器建议** — 帮助后续用 opencli 沉淀为 CLI

## 限制

- 禁止任何写入操作
- 降级模式下无法与动态内容交互
- 需要登录的内容只能记录入口
- 反爬严格的网站可能无法完全探索
