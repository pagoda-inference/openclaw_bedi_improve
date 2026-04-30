---
name: deep-browser
description: "深度网页浏览能力，通过交互式浏览发现网站完整内容结构。当需要通过交互获取隐藏内容、逐层探索网站页面层级、或积累浏览知识以供复用时调用。"
user-invocable: false
---

# Deep Browser Skill

通过交互式浏览逐层发现网站完整内容结构，以只读方式深度探索网站。

## 核心目的

Deep Browser 的核心目的是**通过交互/互动来获得下一层次网页的地址，进而获得网站的所有内容**。

许多网页的内容并不会直接展示在初始页面上，而是需要通过交互才能展开。Deep Browser 通过系统化地与页面交互元素配合，逐层发现网站的完整内容结构，最终获取网站的全部可访问信息。

### 逐层探索模式

```
入口页面
├── 导航链接 → 子页面1
│   ├── 更多链接 → 孙页面1-1
│   └── 更多链接 → 孙页面1-2
├── 导航链接 → 子页面2
│   └── 展开菜单 → 隐藏内容
├── 折叠区域 → 展开后内容
└── 分页控件 → 第2页、第3页...
```

每一层通过交互发现新的入口，再深入探索，直到覆盖网站所有可访问内容。

## ⚠️ 只读约束

**本技能以只读方式操作网站，禁止任何写入行为。**

### 允许的操作（读取行为）

- ✅ 点击导航链接 → 进入新页面
- ✅ 展开折叠菜单 → 显示隐藏内容
- ✅ 滚动页面 → 加载更多条目
- ✅ 切换标签页 → 查看不同分类
- ✅ 触发下拉菜单 → 获取选项列表
- ✅ 搜索输入 → 获取搜索结果（搜索是读取行为）
- ✅ 分页导航 → 获取更多列表条目
- ✅ 筛选/排序 → 改变内容展示方式

### 禁止的操作（写入行为）

- ❌ 提交注册/登录表单 → 会创建会话或账号
- ❌ 提交联系表单/反馈 → 会发送消息
- ❌ 点击"购买"/"下单"按钮 → 会产生交易
- ❌ 修改/编辑已有数据 → 会改变网站状态
- ❌ 删除操作 → 不可逆的写入行为
- ❌ 发布/上传内容 → 会向网站写入数据

### 表单处理策略

当遇到表单时：

1. **搜索表单** → 可以输入关键词并点击搜索按钮（搜索是读取行为）
2. **筛选表单** → 可以选择筛选条件（筛选是读取行为）
3. **登录/注册表单** → 仅记录入口，不填写也不提交
4. **联系/反馈表单** → 仅记录入口，不填写也不提交
5. **数据修改表单** → 仅记录入口，不填写也不提交

**判断标准**：如果表单提交的目的是**获取/展示信息**（如搜索、筛选），则允许；如果表单提交的目的是**创建/修改数据**（如注册、下单、发送消息），则禁止。

## 何时使用

✅ **使用此技能当：**

- **需要通过交互发现隐藏内容**
  - 折叠菜单中的链接
  - 动态加载的更多条目
  - 需要切换标签才能看到的分类
  - 触发下拉菜单后的子选项

- **需要逐层探索网站结构**
  - 从入口页面发现所有子页面
  - 跟踪导航链接到深层内容
  - 构建完整的网站内容地图
  - 覆盖网站所有可访问页面

- **数据需要页面交互才能获取**
  - 通过用户操作加载的数据（点击、滚动、输入）
  - 需要多步导航才能到达的内容
  - 由交互触发的动态内容
  - 分页或无限滚动中的数据

- **需要深度页面分析和理解**
  - 识别页面中的导航入口
  - 理解页面的交互模式
  - 发现API端点和数据源
  - 构建可复用的网站探索模式

## 何时不使用

❌ **不使用此技能当：**

- 简单单页检查 → 使用标准浏览器工具
- 静态内容提取 → 使用web-fetch
- 可用API访问数据 → 直接使用API
- 需要提交表单完成任务 → 本技能禁止写入操作
- 快速搜索或简单获取 → 直接使用web-search或web-fetch

## 前置要求

### 必需依赖

**主要模式：**
- **OpenCLI** - 浏览器自动化工具
  - 安装：`pip install opencli` 或遵循OpenCLI安装指南
  - 验证：`opencli --version`
- **LLM访问** - 用于智能页面分析
  - OpenAI API密钥或兼容的LLM端点
  - 验证：`opencli llm ask "test"`

**降级模式：**
- **web-fetch工具** - 用于静态内容获取
- **web-search工具** - 用于查找相关页面

### 环境设置

```bash
# 初始化环境
python scripts/init_environment.py

# 验证依赖
python scripts/init_environment.py --check-deps
```

## 核心能力

### 1. 交互驱动的页面发现

通过交互发现隐藏的页面和内容：

| 交互方式 | 发现的内容 | 只读判断 |
|---------|-----------|---------|
| 点击导航链接 | 新的页面URL | ✅ 允许 |
| 展开折叠区域 | 隐藏的内容区块 | ✅ 允许 |
| 滚动页面 | 动态加载的条目 | ✅ 允许 |
| 切换标签页 | 不同分类的内容 | ✅ 允许 |
| 触发下拉菜单 | 子菜单选项 | ✅ 允许 |
| 搜索输入+搜索按钮 | 搜索结果页面 | ✅ 允许 |
| 分页导航 | 更多列表条目 | ✅ 允许 |
| 提交注册/登录表单 | 登录后内容 | ❌ 禁止 |
| 提交联系/反馈表单 | 提交确认 | ❌ 禁止 |

### 2. LLM驱动的分析

使用 `reference/` 目录中的结构化参考文档：

- **页面分析** (`reference/page_analysis.md`)
  - 页面类型识别
  - 布局模式检测
  - 数据区域映射
  - 导航入口发现

- **元素分析** (`reference/element_analysis.md`)
  - 交互性检测
  - 只读/写入分类（关键：判断元素是否安全操作）
  - 导航入口识别
  - 元素分组

- **网络分析** (`reference/network_analysis.md`)
  - API端点发现
  - 数据源识别
  - 直接API潜力评估

### 3. 降级机制

当浏览器工具（OpenCLI, browser-automation）不可用时，自动降级到：

- **web-fetch** - 获取静态页面内容
- **web-search** - 查找相关页面和信息

**降级工作流：**
1. 检测浏览器工具可用性
2. 如果不可用 → 使用web-fetch获取页面内容
3. 使用web-search查找相关页面
4. 对获取的内容应用相同的分析参考
5. 将结果存储到模式文件

**降级限制：**
- 无法与动态内容交互
- 无法发现交互才能展现的内容
- 无法处理认证
- 仅限于公开可访问的页面

### 4. 记忆系统

基于Markdown的模式存储在 `browser-patterns/` 目录：

```
browser-patterns/
├── sites/
│   ├── example.com.md    # 网站模式
│   └── INDEX.md          # 模式索引
└── plans/
    ├── task-001.md       # 浏览计划
    └── INDEX.md          # 计划索引
```

### 5. Python脚本

`scripts/` 目录中的辅助脚本：

- `browser_operations.py` - 浏览器导航和交互操作
- `file_operations.py` - 简单的文件操作工具
- `memory_manager.py` - 长期模式文件管理
- `init_environment.py` - 环境设置

## 使用方法

### 1. 初始化环境

```bash
python scripts/init_environment.py
```

创建：
- `browser-patterns/sites/` 目录
- `browser-patterns/plans/` 目录
- `states/` 目录（用于上下文隔离）
- 索引文件

### 2. 逐层探索工作流

这是 Deep Browser 的核心工作流：

```
步骤1：打开入口页面
  └─ open(url)

步骤2：分析当前页面
  ├─ get_state() → 获取页面元素
  ├─ 读取 reference/page_analysis.md → 分析页面结构
  └─ 读取 reference/element_analysis.md → 识别交互元素

步骤3：分类交互元素
  ├─ 导航类（链接、菜单）→ 执行交互，发现新页面URL
  ├─ 展示类（折叠、标签）→ 执行交互，发现隐藏内容
  ├─ 搜索类（搜索框）→ 输入关键词，执行搜索
  └─ 写入类（表单提交）→ 记录入口，不执行提交

步骤4：执行安全交互
  ├─ 对导航类/展示类/搜索类 → click/scroll/type_text
  ├─ 获取交互后的新状态 → get_state()
  └─ 记录发现的新的页面URL和内容

步骤5：深入下一层
  ├─ 对发现的新页面URL → open(new_url)
  └─ 重复步骤2-4

步骤6：保存到记忆
  ├─ 提取网站导航结构
  ├─ 保存到模式文件
  └─ 更新索引
```

### 3. 使用状态文件进行上下文隔离

**核心概念**：将页面状态写入文件而不是保存在内存中，以实现更好的隔离。

```python
from scripts.file_operations import FileOps

FileOps.write("states/state-001.md", page_state_content)
content = FileOps.read("states/state-001.md")

FileOps.replace_section(
    "states/state-001.md",
    start_marker="## 页面元素",
    end_marker="## 分析结果",
    new_content=elements_table
)

FileOps.replace_lines(
    "states/state-001.md",
    start_line=10,
    end_line=15,
    new_lines=["新行 1", "新行 2"]
)
```

**优势**：
- 智能体不需要记住所有上下文
- 状态跨会话持久化
- 可以手动审查/编辑
- 支持多页面并行处理

### 4. 使用参考文档进行分析

智能体读取参考文件并创建结构化的状态文件：

**步骤1：读取分析参考**
```markdown
读取 reference/page_analysis.md
```

**步骤2：应用到页面内容**
- 使用参考框架分析页面结构
- 识别页面类型、布局、数据区域
- **识别所有导航入口和交互元素**
- **对每个交互元素判断只读/写入属性**

**步骤3：创建状态文件**
```markdown
使用 reference/page_state_template.md
创建 states/state-{id}.md 包含分析结果
```

**步骤4：更新状态文件**
```python
FileOps.replace_section(
    "states/state-001.md",
    "## 页面元素",
    "## 分析结果",
    elements_table
)
```

### 5. 保存到记忆

```python
from scripts.memory_manager import MemoryManager

manager = MemoryManager()

pattern_content = """# example.com

> 域名: example.com
> 创建时间: 2026-04-28

## 页面层级

### 首页
- 导航链接: /products, /about, /contact

### /products (列表页)
- 分页: 点击式，.next-page
- 每页50个商品
- 子页面: /products/{id}

### /about (内容页)
- 无交互入口

### /contact (表单页)
- ⚠️ 写入类表单，未提交
- 入口已记录
"""

manager.create_site_pattern("example.com", pattern_content)
content = manager.read_site_pattern("example.com")
results = manager.search_patterns("product")
patterns = manager.list_site_patterns()
```

### 6. 浏览器操作

**参考**：详见 `reference/browser_operations_reference.md` 获取详细操作指南。

**核心操作：**
- **导航**: open(), get_url(), get_title()
- **状态**: get_state(), extract()
- **交互**: click(), type_text(), scroll()
- **数据**: get_text(), screenshot()
- **网络**: network()

**代码示例：**
```python
from scripts.browser_operations import DeepBrowser

browser = DeepBrowser()

browser.open("https://example.com")
state = browser.get_state()

# 安全交互：点击导航链接
browser.click(target=123)  # 导航链接 → 允许

# 安全交互：搜索
browser.type_text(target=456, text="query")  # 搜索框 → 允许
browser.click(target=789)  # 搜索按钮 → 允许

# ❌ 禁止：提交表单
# browser.click(target=999)  # 提交按钮 → 禁止

data = browser.extract()
```

### 7. 降级使用（当浏览器不可用时）

当浏览器工具不可用时，使用web-fetch和web-search：

```markdown
# 降级工作流
1. 尝试 browser.open() → 失败
2. 检测浏览器不可用
3. 使用web-fetch获取页面内容
4. 使用web-search查找相关页面
5. 对获取的内容应用分析参考
6. 将结果存储到模式文件
```

**注意**：降级模式下无法通过交互发现隐藏内容，只能获取静态页面。

## 分析工作流

### 步骤1：创建状态文件

1. 生成唯一状态ID
2. 在 `states/` 目录创建状态文件
3. 用基本结构初始化

### 步骤2：捕获页面状态

1. 打开目标URL
2. 获取页面状态
3. 用以下内容更新状态文件：
   - 基本信息（URL、标题）
   - 页面元素（表格格式，标注只读/写入属性）
   - 网络请求

### 步骤3：应用分析参考

1. 读取 `reference/page_analysis.md`
2. 应用到页面内容
3. **识别所有导航入口和交互元素**
4. 用分析结果更新状态文件

### 步骤4：生成交互行动计划

1. 读取 `reference/element_analysis.md`
2. 识别可交互元素
3. **对每个元素判断：只读操作 or 写入操作**
4. 用建议操作更新状态文件（标注安全/禁止）

### 步骤5：执行安全交互

1. 智能体读取状态文件
2. **仅执行标记为安全的操作**
3. 记录交互后发现的新页面URL
4. 用结果更新状态文件
5. 添加观察备注

### 步骤6：深入下一层

1. 对发现的新页面URL，重复步骤1-5
2. 直到覆盖所有可访问内容
3. 将完整的网站结构保存到记忆

## 记忆格式

### 状态文件结构

```markdown
# 页面状态: state-001

> 状态ID: state-001
> 创建时间: 2026-04-28T10:00:00Z
> 更新时间: 2026-04-28T10:30:00Z

## 基本信息

- **URL**: https://example.com/products
- **标题**: 商品列表
- **状态**: analyzed

## 页面元素

| 引用 | 标签 | 文本 | 可见 | 角色 | 安全性 |
|------|------|------|------|------|--------|
| 1 | a | 商品详情 | ✓ | link | ✅ 只读 |
| 2 | a | 下一页 | ✓ | link | ✅ 只读 |
| 3 | button | 展开筛选 | ✓ | button | ✅ 只读 |
| 4 | input | 搜索 | ✓ | search | ✅ 只读 |
| 5 | button | 提交订单 | ✓ | submit | ❌ 写入 |

## 分析结果

**页面类型**: listing (置信度: 0.95)

**布局模式**: two-column

### 导航入口

- `/products/123` → 商品详情页（通过元素1）
- `/products?page=2` → 第2页（通过元素2）

### 交互发现

- 元素3：展开筛选面板 → 显示更多筛选选项
- 元素4：搜索框 → 输入关键词后展示搜索结果

### 写入类元素（禁止操作）

- 元素5：提交订单按钮 → 会产生交易，禁止点击

## 建议操作

1. ✅ **click** (安全)
   - 目标: 元素1
   - 目的: 进入商品详情页
   - 预期: 发现新的子页面

2. ✅ **click** (安全)
   - 目标: 元素2
   - 目的: 加载下一页
   - 预期: 发现更多商品条目

3. ✅ **click** (安全)
   - 目标: 元素3
   - 目的: 展开筛选面板
   - 预期: 发现筛选选项

4. ❌ **click** (禁止)
   - 目标: 元素5
   - 原因: 提交订单是写入操作
   - 处理: 记录入口，不执行

## 网络请求

总计: 15 个请求

| 方法 | URL | 类型 |
|------|-----|------|
| GET | /api/products | application/json |

## 备注

- 初始页面加载成功 (10:00:05)
- 发现3个导航入口，1个写入类元素 (10:00:10)
```

### 模式文件结构

```markdown
# example.com

> 域名: example.com
> 学习时间: 2026-04-28T10:00:00Z
> 最后使用: 2026-04-28T10:30:00Z

## 页面层级

### 首页 (/)
- 导航入口: /products, /about, /contact
- 交互发现: 主导航菜单、搜索框

### 商品列表 (/products)
- 类型: listing
- 分页: 点击式，.next-page
- 导航入口: /products/{id}
- 交互发现: 筛选面板、排序选项

### 商品详情 (/products/{id})
- 类型: product
- 导航入口: 相关商品链接
- ⚠️ 写入类: 加入购物车按钮（未操作）

### 联系页面 (/contact)
- 类型: form
- ⚠️ 写入类: 联系表单（未提交）
- 入口已记录

## 选择器

| 名称 | 选择器 | 安全性 |
|------|--------|--------|
| nav_products | #nav-products | ✅ 只读 |
| search_box | #search | ✅ 只读 |
| next_page | .next-page | ✅ 只读 |
| add_to_cart | .add-to-cart | ❌ 写入 |
| contact_submit | #contact-submit | ❌ 写入 |

## 备注

- 网站需要JavaScript才能正常显示
- 商品列表每页50个条目
```

### 计划文件结构

```markdown
# 浏览计划: 探索example.com完整结构

> 任务ID: task-001
> 目标: 发现网站所有可访问页面
> 深度: 0/3
> 状态: in-progress
> 创建时间: 2026-04-28T10:00:00Z

## 进度

- 总层级: 3
- 已探索: 1
- 进行中: 1
- 待探索: 1

## 层级探索

### 第1层: 首页 ✅

- 操作: open
- 参数: {"url": "https://example.com"}
- 发现入口: /products, /about, /contact

### 第2层: 商品列表 🔄

- 操作: open
- 参数: {"url": "https://example.com/products"}
- 发现入口: /products/{id}, 分页
- ⚠️ 跳过: 加入购物车按钮（写入操作）

### 第3层: 商品详情 ⏳

- 操作: open
- 参数: {"url": "https://example.com/products/123"}
- 待探索

## 写入类入口记录

| 页面 | 元素 | 类型 | 原因 |
|------|------|------|------|
| /products | 加入购物车 | 表单提交 | 会修改购物车数据 |
| /contact | 提交联系表单 | 表单提交 | 会发送消息 |
```

## 与智能体集成

智能体通过以下方式使用此技能：

1. **读取参考** 从 `reference/` 目录
2. **分析页面** 识别导航入口和交互元素
3. **判断安全性** 对每个交互元素分类只读/写入
4. **执行安全交互** 仅执行只读操作
5. **记录发现** 保存新发现的页面URL和内容
6. **深入探索** 对新页面重复上述流程
7. **存储模式** 将网站结构保存到记忆

## 最佳实践

1. **始终先初始化** 环境
2. **分析前读取参考**
3. **交互前判断安全性** - 只执行只读操作
4. **记录写入类入口** - 不执行但记录存在
5. **逐层深入探索** - 不遗漏任何导航入口
6. **发现时使用直接API** - 如果API可获取相同数据
7. **成功探索后保存模式** - 积累网站知识

## 限制

### 只读约束限制
- 无法访问需要登录的页面
- 无法提交任何表单
- 无法完成需要写入操作的流程
- 某些内容可能只能通过表单提交后才能访问

### 主要模式（浏览器工具）
- 需要OpenCLI或browser-automation工具
- 需要LLM进行基于参考的分析
- 模式存储随网站多样性增长
- 初始分析比关键词匹配慢

### 降级模式（web-fetch + web-search）
- 无法与动态内容交互
- 无法发现交互才能展现的内容
- 无法处理认证
- 仅限于公开可访问的页面
- 无实时页面状态监控
- 无法捕获网络请求

## 相关技能

### 主要工具
- `browser-automation` - 标准浏览器控制
- `web-fetch` - 简单内容提取
- `web-search` - 搜索和查找信息

### 降级工具
- `web-fetch` + `web-search` - 浏览器不可用时的替代方案

### 领域技能
- `market-research-collector` - 数据采集工作流
