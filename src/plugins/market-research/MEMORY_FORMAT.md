# 网站模式记忆格式规范

## 文件位置

```
~/.openclaw/deep-browser/patterns/
├── INDEX.md                    # 索引文件
├── amazon.com.md               # Amazon 网站模式
├── twitter.com.md              # Twitter 网站模式
└── ...
```

## INDEX.md 格式

```markdown
# 网站模式索引

| 域名 | 文件 | 页面类型 | 最后使用 | 成功率 |
|------|------|---------|---------|--------|
| amazon.com | [amazon.com.md](./amazon.com.md) | listing, product | 2024-01-15 | 95% |
| twitter.com | [twitter.com.md](./twitter.com.md) | feed, profile | 2024-01-14 | 88% |
| zhihu.com | [zhihu.com.md](./zhihu.com.md) | search, article | 2024-01-13 | 92% |
```

## 网站模式文件格式

```markdown
# amazon.com

> 域名: amazon.com
> 学习时间: 2024-01-10
> 最后使用: 2024-01-15
> 成功次数: 19
> 失败次数: 1

## 页面类型

### listing（商品列表页）

**识别特征**：
- URL 包含 `/s?k=` 或 `/gp/search`
- 页面包含 `.s-result-list` 元素
- 文本包含 "results" 或 "结果"

**数据区域**：
| 选择器 | 类型 | 说明 |
|--------|------|------|
| `.s-result-list` | product-list | 商品列表容器 |
| `.s-result-item` | product-card | 单个商品卡片 |
| `h2 a.a-link-normal` | product-title | 商品标题 |
| `.a-price .a-offscreen` | product-price | 商品价格 |

**分页机制**：
- 类型: click
- 选择器: `.s-pagination-next`
- 操作: 点击"下一页"按钮

**操作流程**：
```
1. 等待 .s-result-list 加载
2. 采集所有 .s-result-item
3. 点击 .s-pagination-next
4. 等待新内容加载
5. 重复步骤 2-4 直到没有下一页
```

### product（商品详情页）

**识别特征**：
- URL 包含 `/dp/` 或 `/gp/product/`
- 页面包含 `#productTitle` 元素
- 文本包含 "Add to Cart" 或 "购买"

**数据区域**：
| 选择器 | 类型 | 说明 |
|--------|------|------|
| `#productTitle` | title | 商品标题 |
| `.a-price .a-offscreen` | price | 当前价格 |
| `.a-price-whole` | price-whole | 整数部分 |
| `#feature-bullets` | features | 商品特性 |
| `#productDescription` | description | 商品描述 |

**API 端点**：
```
GET /gp/product/ajax-handlers/apparel-show-size-chart.html
返回: { sizes: [...], colors: [...] }
```

## 导航流程

### search-to-product（搜索到商品）

**目的**: 从搜索页进入商品详情

**步骤**：
```
Step 1: 在搜索框输入关键词
  - 选择器: #twotabsearchtextbox
  - 操作: type "{keyword}"
  - 等待: 输入完成

Step 2: 点击搜索按钮
  - 选择器: #nav-search-submit-button
  - 操作: click
  - 等待: .s-result-list 出现

Step 3: 点击商品卡片
  - 选择器: h2 a.a-link-normal
  - 操作: click
  - 等待: #productTitle 出现
```

### pagination-flow（分页浏览）

**目的**: 浏览所有搜索结果

**步骤**：
```
循环直到 .s-pagination-next 不存在:
  Step 1: 采集当前页商品
    - 选择器: .s-result-item
    - 操作: collect

  Step 2: 点击下一页
    - 选择器: .s-pagination-next
    - 操作: click
    - 等待: .s-result-list 重新加载
```

## API 端点

| 端点 | 方法 | 用途 | 数据结构 |
|------|------|------|---------|
| `/gp/product/ajax-handlers/apparel-show-size-chart.html` | GET | 获取尺码信息 | `{ sizes: string[] }` |
| `/gp/product/ajax-handlers/reviews.html` | GET | 获取评论 | `{ reviews: Review[] }` |

## 注意事项

- 需要登录才能查看某些价格
- 部分商品有地区限制
- 价格可能因用户而异
```

## 浏览计划文件格式

```
~/.openclaw/deep-browser/plans/
├── INDEX.md
├── task-20240115-abc123.md
└── ...
```

### INDEX.md 格式

```markdown
# 浏览计划索引

| 任务ID | 目标 | 状态 | 文件 | 创建时间 |
|--------|------|------|------|---------|
| task-20240115-abc123 | 采集 AI Agent 市场 | 进行中 | [task-20240115-abc123.md](./task-20240115-abc123.md) | 2024-01-15 |
| task-20240114-xyz789 | 竞品分析 | 已完成 | [task-20240114-xyz789.md](./task-20240114-xyz789.md) | 2024-01-14 |
```

### 浏览计划文件格式

```markdown
# 浏览计划: AI Agent 市场规模

> 任务ID: task-20240115-abc123
> 目标: 采集 AI Agent 市场规模数据
> 当前深度: 1
> 最大深度: 3
> 状态: 进行中
> 创建时间: 2024-01-15 10:00:00

## 进度概览

- 总步骤: 8
- 已完成: 3
- 进行中: 1
- 待执行: 4

## 执行步骤

### Step 1: 打开搜索页面 ✅

- 状态: 已完成
- 操作: navigate
- 参数: url = "https://www.google.com"
- 执行时间: 2024-01-15 10:01:00
- 结果: 页面加载成功

### Step 2: 输入搜索关键词 ✅

- 状态: 已完成
- 操作: type
- 参数: target = 5, text = "AI Agent 市场规模"
- 依赖: Step 1
- 执行时间: 2024-01-15 10:01:30
- 结果: 输入成功

### Step 3: 执行搜索 ✅

- 状态: 已完成
- 操作: click
- 参数: target = 6
- 依赖: Step 2
- 执行时间: 2024-01-15 10:02:00
- 结果: 搜索结果已加载

### Step 4: 采集搜索结果 🔄

- 状态: 进行中
- 操作: collect
- 参数: selector = "#search .g"
- 依赖: Step 3
- 开始时间: 2024-01-15 10:02:30
- 重试次数: 0

### Step 5: 访问第一个结果 ⏳

- 状态: 待执行
- 操作: click
- 参数: target = 10
- 依赖: Step 4
- 预期: 进入详情页

### Step 6: 采集详情页内容 ⏳

- 状态: 待执行
- 操作: collect
- 参数: selector = "article"
- 依赖: Step 5
- 预期: 获取文章内容

### Step 7: 返回搜索结果 ⏳

- 状态: 待执行
- 操作: navigate
- 参数: direction = "back"
- 依赖: Step 6
- 预期: 返回搜索页

### Step 8: 保存网站模式 ⏳

- 状态: 待执行
- 操作: remember
- 参数: site_pattern_id = "google-search"
- 依赖: Step 7
- 预期: 模式已保存

## 已采集数据

### Step 4 的数据

```json
{
  "items": [
    {
      "title": "AI Agent 市场规模报告 2024",
      "url": "https://example.com/report",
      "snippet": "AI Agent 市场预计在 2024 年达到..."
    }
  ],
  "count": 10
}
```

## 执行日志

```
[10:01:00] Step 1 开始: navigate to google.com
[10:01:05] Step 1 完成: 页面加载成功
[10:01:30] Step 2 开始: 输入搜索关键词
[10:01:32] Step 2 完成: 输入成功
[10:02:00] Step 3 开始: 执行搜索
[10:02:15] Step 3 完成: 搜索结果已加载
[10:02:30] Step 4 开始: 采集搜索结果
...
```
```

## 三、索引机制实现

```typescript
// 索引文件路径
const PATTERNS_INDEX = path.join(MEMORY_BASE_DIR, "patterns", "INDEX.md");
const PLANS_INDEX = path.join(MEMORY_BASE_DIR, "plans", "INDEX.md");

// 解析索引
private async parsePatternsIndex(): Promise<Array<{
  domain: string;
  file: string;
  pageTypes: string[];
  lastUsed: string;
  successRate: string;
}>> {
  const content = await fs.readFile(PATTERNS_INDEX, "utf-8");
  const lines = content.split("\n").filter(l => l.startsWith("|") && !l.includes("---"));
  
  // 跳过表头
  return lines.slice(1).map(line => {
    const [domain, file, pageTypes, lastUsed, successRate] = 
      line.split("|").map(s => s.trim()).filter(Boolean);
    return { domain, file, pageTypes: pageTypes.split(", "), lastUsed, successRate };
  });
}

// 更新索引
private async updatePatternsIndex(entry: {
  domain: string;
  file: string;
  pageTypes: string[];
  lastUsed: string;
  successRate: string;
}): Promise<void> {
  const index = await this.parsePatternsIndex();
  const existing = index.find(i => i.domain === entry.domain);
  
  if (existing) {
    Object.assign(existing, entry);
  } else {
    index.push(entry);
  }
  
  const content = this.generateIndexMarkdown(index);
  await fs.writeFile(PATTERNS_INDEX, content);
}

// 生成索引 Markdown
private generateIndexMarkdown(entries: Array<{...}>): string {
  const header = `# 网站模式索引

| 域名 | 文件 | 页面类型 | 最后使用 | 成功率 |
|------|------|---------|---------|--------|
`;
  
  const rows = entries.map(e => 
    `| ${e.domain} | [${e.file}](./${e.file}) | ${e.pageTypes.join(", ")} | ${e.lastUsed} | ${e.successRate} |`
  ).join("\n");
  
  return header + rows;
}
```

## 四、MD 文件读写实现

```typescript
// 读取网站模式
private async readSitePattern(domain: string): Promise<SitePattern | null> {
  const filePath = path.join(MEMORY_BASE_DIR, "patterns", `${domain}.md`);
  const content = await fs.readFile(filePath, "utf-8");
  return this.parsePatternMarkdown(content);
}

// 解析 MD 文件
private parsePatternMarkdown(content: string): SitePattern {
  const frontmatter = this.parseFrontmatter(content);
  const sections = this.parseSections(content);
  
  return {
    id: frontmatter.domain,
    domain: frontmatter.domain,
    page_types: this.parsePageTypes(sections),
    navigation_flows: this.parseNavigationFlows(sections),
    data_endpoints: this.parseDataEndpoints(sections),
    selectors: this.parseSelectors(sections),
    learned_at: frontmatter.学习时间,
    last_used: frontmatter.最后使用,
    success_count: parseInt(frontmatter.成功次数),
    failure_count: parseInt(frontmatter.失败次数),
  };
}

// 写入网站模式
private async writeSitePattern(pattern: SitePattern): Promise<void> {
  const content = this.generatePatternMarkdown(pattern);
  const filePath = path.join(MEMORY_BASE_DIR, "patterns", `${pattern.domain}.md`);
  await fs.writeFile(filePath, content);
  
  // 更新索引
  await this.updatePatternsIndex({
    domain: pattern.domain,
    file: `${pattern.domain}.md`,
    pageTypes: Object.keys(pattern.page_types),
    lastUsed: pattern.last_used,
    successRate: `${Math.round(pattern.success_count / (pattern.success_count + pattern.failure_count) * 100)}%`,
  });
}
```

这样设计的好处：
1. **可读性**：MD 文件可以直接查看和编辑
2. **版本控制友好**：可以 git diff 看变化
3. **索引机制**：快速查找和定位
4. **结构化**：清晰的章节划分

要我继续完善这个实现吗？