# 页面分析参考文档

本文档提供页面结构分析的方法论和框架，帮助智能体理解网页结构。

## 分析目标

页面分析的核心目标是理解：
1. **页面用途** - 这个页面是做什么的
2. **内容结构** - 信息如何组织
3. **交互方式** - 用户如何与页面互动
4. **数据分布** - 数据在哪里，如何提取

## 分析维度

### 1. 页面类型识别

**常见页面类型：**

| 类型 | 特征 | 示例 |
|------|------|------|
| listing | 列表展示，通常有分页 | 商品列表、文章列表 |
| product | 单个实体详情 | 商品详情页、文章详情 |
| search | 搜索结果展示 | 搜索结果页 |
| login | 用户认证 | 登录、注册页面 |
| form | 数据收集 | 联系表单、调查问卷 |
| content | 信息展示 | 关于我们、帮助文档 |
| checkout | 交易流程 | 购物车、结算页 |
| dashboard | 数据概览 | 用户中心、控制面板 |

**识别方法：**
- 查看页面标题和主要标题（h1）
- 观察主要内容区域的布局
- 识别关键交互元素（按钮、表单）
- 分析URL路径和参数

### 2. 布局模式分析

**常见布局模式：**

```
单列布局 (single-column)
┌─────────────┐
│   Header    │
├─────────────┤
│   Content   │
│             │
├─────────────┤
│   Footer    │
└─────────────┘

双列布局 (two-column)
┌─────────────┐
│   Header    │
├──────┬──────┤
│ Main │ Side │
│      │ bar  │
├──────┴──────┤
│   Footer    │
└─────────────┘

三列布局 (three-column)
┌─────────────┐
│   Header    │
├──┬────┬─────┤
│L │Main│  R  │
│  │    │     │
├──┴────┴─────┤
│   Footer    │
└─────────────┘
```

**分析方法：**
- 使用浏览器开发工具查看DOM结构
- 识别主要容器元素（div, section, article）
- 观察CSS类名（container, wrapper, sidebar等）
- 检查响应式断点

### 3. 数据区域定位

**数据区域特征：**

| 数据类型 | HTML特征 | CSS选择器示例 |
|---------|---------|--------------|
| 商品列表 | ul/ol, div.grid | .product-list, .products |
| 文章列表 | article, div.post | .article-list, .posts |
| 表格数据 | table | table, .data-table |
| 表单 | form | form, .contact-form |
| 导航 | nav, ul.menu | nav, .navigation |

**定位方法：**
1. 查找重复元素（列表项、卡片）
2. 识别数据容器
3. 确定数据字段（标题、价格、描述等）
4. 验证选择器稳定性

### 4. 分页机制识别

**分页类型：**

| 类型 | 特征 | 识别方法 |
|------|------|---------|
| click | 页码按钮、上一页/下一页 | 查找分页导航元素 |
| scroll | 滚动加载更多 | 监听滚动事件，观察内容变化 |
| load-more | "加载更多"按钮 | 查找按钮文本或图标 |
| none | 单页内容 | 无分页元素 |

**识别步骤：**
1. 查找分页相关元素
2. 检查是否有"下一页"、"加载更多"等文本
3. 测试交互行为
4. 记录选择器和交互方式

### 5. 表单分析

**表单要素：**

```
表单结构：
┌─────────────────────────┐
│ Form Element            │
│  ┌─────────────────┐   │
│  │ Input Field 1   │   │
│  └─────────────────┘   │
│  ┌─────────────────┐   │
│  │ Input Field 2   │   │
│  └─────────────────┘   │
│  ┌─────────────────┐   │
│  │  Submit Button  │   │
│  └─────────────────┘   │
└─────────────────────────┘
```

**分析要点：**
- 表单用途（搜索、登录、联系等）
- 必填字段识别（required属性、*标记）
- 输入类型（text、email、password等）
- 验证规则（pattern、minlength等）
- 提交方式（按钮、回车等）

### 6. 导航路径发现

**导航类型：**

| 导航类型 | 位置 | 用途 |
|---------|------|------|
| 主导航 | 页面顶部 | 主要页面切换 |
| 侧边导航 | 页面左侧 | 分类、筛选 |
| 面包屑 | 内容顶部 | 层级导航 |
| 页脚导航 | 页面底部 | 辅助链接 |

**发现方法：**
- 查找nav元素
- 识别链接文本和目标
- 分析导航层级关系
- 记录重要链接

## 分析工具

### 浏览器开发工具

**元素检查：**
```javascript
// 获取元素信息
document.querySelector('selector')

// 查看元素属性
element.getAttribute('class')

// 获取元素文本
element.textContent
```

**网络监控：**
- 打开Network面板
- 筛选XHR/Fetch请求
- 查看请求参数和响应

### 选择器测试

**CSS选择器：**
```javascript
// 测试选择器
document.querySelectorAll('.product-item')

// 验证选择器唯一性
document.querySelectorAll('.product-item').length
```

**XPath：**
```javascript
// 使用XPath
document.evaluate(
  '//div[@class="product"]',
  document,
  null,
  XPathResult.ANY_TYPE,
  null
)
```

## 分析输出

### 状态文件格式

分析结果应保存为Markdown格式的状态文件：

```markdown
# Page State: {state-id}

## Basic Info
- URL: {url}
- Title: {title}
- Type: {page-type}

## Layout
- Pattern: {layout-pattern}
- Main regions: {regions}

## Data Regions
| Selector | Type | Description |
|----------|------|-------------|
| .products | product-list | 商品列表 |

## Pagination
- Type: {type}
- Selector: {selector}

## Forms
| Purpose | Selector | Fields |
|---------|----------|--------|
| Search | .search-form | keyword |

## Actions
1. {action-type}: {target} - {purpose}
```

## 最佳实践

1. **从整体到局部**
   - 先识别页面类型和布局
   - 再定位具体数据区域
   - 最后分析细节元素

2. **验证选择器**
   - 使用开发工具测试
   - 检查选择器稳定性
   - 考虑动态内容影响

3. **记录发现**
   - 及时记录分析结果
   - 更新状态文件
   - 标注不确定项

4. **迭代优化**
   - 初步分析后验证
   - 根据实际情况调整
   - 持续完善分析结果

## 常见问题

**Q: 如何处理动态加载的内容？**
A: 等待内容加载完成，或触发加载事件后再分析

**Q: 如何识别反爬机制？**
A: 观察请求头要求、验证码、登录墙等

**Q: 选择器不稳定怎么办？**
A: 使用多个备选选择器，或基于内容特征定位

## 相关参考

- [元素分析参考](element_analysis.md)
- [网络分析参考](network_analysis.md)
- [页面状态模板](page_state_template.md)
