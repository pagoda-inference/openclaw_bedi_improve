# 元素分析参考文档

本文档提供页面元素交互性分析的方法论和框架，帮助智能体识别可交互元素。

## 分析目标

元素分析的核心目标是理解：
1. **交互类型** - 元素如何被操作
2. **交互目的** - 操作会产生什么结果
3. **重要性等级** - 哪些元素更关键
4. **元素关系** - 元素之间如何协作

## 分析维度

### 1. 交互类型识别

**常见交互类型：**

| 交互类型 | 触发方式 | 典型元素 | 使用场景 |
|---------|---------|---------|---------|
| click | 鼠标点击 | button, a, div | 导航、提交、触发操作 |
| type | 键盘输入 | input, textarea | 表单填写、搜索 |
| select | 下拉选择 | select, dropdown | 选项选择、筛选 |
| scroll | 滚动操作 | div, body | 内容浏览、加载更多 |
| hover | 鼠标悬停 | a, div | 显示菜单、提示信息 |
| drag | 拖拽操作 | div, img | 排序、移动元素 |

**识别方法：**
- 查看HTML标签类型（button, input, a等）
- 检查事件监听器（onclick, onchange等）
- 观察CSS样式（cursor: pointer等）
- 测试实际交互行为

### 2. 交互目的推断

**常见目的类型：**

| 目的类型 | 特征 | 示例 |
|---------|------|------|
| 导航 | 跳转到其他页面 | 链接、菜单项 |
| 操作 | 执行特定功能 | 提交按钮、删除按钮 |
| 输入 | 收集用户数据 | 表单字段、搜索框 |
| 显示 | 展示/隐藏内容 | 展开/折叠按钮 |
| 筛选 | 修改显示内容 | 下拉选择、复选框 |

**推断方法：**
- 分析元素文本内容（按钮文字、链接文本）
- 查看元素位置（导航栏、表单中、内容区）
- 检查相关元素（表单的提交按钮）
- 理解上下文（搜索框旁边的搜索按钮）

### 3. 重要性评估

**重要性等级：**

```
高 (high)
├─ 主要操作按钮（提交、购买、搜索）
├─ 关键导航链接（首页、登录）
└─ 必填表单字段

中 (medium)
├─ 次要操作（分享、收藏）
├─ 辅助导航（帮助、关于）
└─ 可选表单字段

低 (low)
├─ 装饰性元素
├─ 辅助功能（打印、分享到社交媒体）
└─ 可选操作
```

**评估标准：**
- 是否影响主要任务流程
- 使用频率高低
- 对用户目标的重要性
- 是否为必需操作

### 4. 元素分组

**常见分组类型：**

| 分组类型 | 特征 | 示例 |
|---------|------|------|
| form | 表单相关元素 | 登录表单：用户名+密码+提交 |
| navigation | 导航相关元素 | 主导航：首页+产品+关于 |
| list | 列表项 | 商品列表：多个商品卡片 |
| menu | 菜单项 | 下拉菜单：多个选项 |

**分组方法：**
- 查找父容器元素（form, nav, ul）
- 识别共同功能（都是搜索相关）
- 分析空间关系（相邻的元素）
- 理解逻辑关系（输入+提交）

## 分析工具

### 浏览器开发工具

**元素检查：**
```javascript
// 查看元素事件
getEventListeners(element)

// 检查元素属性
element.attributes

// 查看元素样式
window.getComputedStyle(element)
```

**交互测试：**
```javascript
// 模拟点击
element.click()

// 模拟输入
element.value = 'test'
element.dispatchEvent(new Event('input'))

// 检查可交互性
element.isContentEditable
element.disabled
```

### 选择器定位

**CSS选择器：**
```javascript
// 按类型查找
document.querySelectorAll('button')
document.querySelectorAll('input[type="text"]')

// 按属性查找
document.querySelectorAll('[onclick]')
document.querySelectorAll('[role="button"]')

// 按类名查找
document.querySelectorAll('.btn-primary')
document.querySelectorAll('.submit-button')
```

**XPath：**
```javascript
// 查找按钮
//button[contains(text(), '提交')]

// 查找输入框
//input[@type='text']

// 查找链接
//a[contains(@href, 'product')]
```

## 分析输出

### 元素列表格式

分析结果应保存为Markdown格式的元素列表：

```markdown
## Page Elements

| Ref | Tag | Text | Visible | Role | Priority |
|-----|-----|------|---------|------|----------|
| 1 | button | 提交 | ✓ | submit | high |
| 2 | input | | ✓ | textbox | high |
| 3 | a | 首页 | ✓ | link | medium |

## Element Groups

### 登录表单
- Elements: [2, 3, 1]
- Purpose: 用户登录
- Type: form

### 主导航
- Elements: [4, 5, 6]
- Purpose: 页面导航
- Type: navigation
```

### 交互建议格式

```markdown
## Suggested Actions

1. 🔴 **click**
   - Target: [1]
   - Purpose: 提交登录表单
   - Priority: high
   - Expected: 跳转到用户主页

2. 🟡 **type**
   - Target: [2]
   - Purpose: 输入用户名
   - Priority: high
   - Expected: 文本显示在输入框
```

## 分析流程

### 标准流程

```
1. 页面扫描
   ├─ 获取所有元素
   ├─ 识别元素类型
   └─ 标记可见性

2. 交互性判断
   ├─ 检查HTML标签
   ├─ 查看事件监听
   └─ 测试交互行为

3. 目的推断
   ├─ 分析元素文本
   ├─ 查看上下文
   └─ 理解功能逻辑

4. 重要性评估
   ├─ 判断任务相关性
   ├─ 评估使用频率
   └─ 确定优先级

5. 分组归类
   ├─ 查找父容器
   ├─ 识别功能组
   └─ 记录关系
```

### 特殊情况处理

**隐藏元素：**
- 检查display: none
- 检查visibility: hidden
- 检查opacity: 0
- 标记为不可见

**动态元素：**
- 等待元素出现
- 监听DOM变化
- 使用动态选择器

**禁用元素：**
- 检查disabled属性
- 检查aria-disabled
- 标记为不可交互

## 最佳实践

1. **优先级排序**
   - 先分析高优先级元素
   - 关注主要任务流程
   - 不要忽略次要元素

2. **上下文理解**
   - 结合页面类型分析
   - 考虑用户目标
   - 理解业务逻辑

3. **验证测试**
   - 实际测试交互
   - 验证预期结果
   - 记录异常情况

4. **持续更新**
   - 页面变化时重新分析
   - 更新元素列表
   - 调整优先级

## 常见问题

**Q: 如何判断元素是否可交互？**
A: 检查HTML标签、事件监听器、CSS样式，并实际测试交互行为

**Q: 如何处理动态加载的元素？**
A: 等待元素加载完成，或使用MutationObserver监听DOM变化

**Q: 如何识别元素的真实用途？**
A: 结合元素文本、位置、上下文和实际交互测试综合判断

## 相关参考

- [页面分析参考](page_analysis.md)
- [网络分析参考](network_analysis.md)
- [浏览器操作参考](browser_operations_reference.md)
