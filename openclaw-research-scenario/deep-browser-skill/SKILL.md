---
name: deep-browser
description: "Deep web browsing capability with intelligent page understanding and systematic navigation. Invoke when needing to deeply explore websites, understand page structures, navigate complex flows, or accumulate browsing knowledge for reuse."
user-invocable: false
---

# Deep Browser Skill

Advanced browser automation with LLM intelligence for complex web interactions.

## When to Use

✅ **USE this skill when:**

- **Data requires page interaction**
  - Information behind login forms
  - Data loaded via user actions (click, scroll, input)
  - Content requiring multi-step workflows
  - Dynamic content triggered by interactions

- **In-depth page interaction needed**
  - Multi-step form submissions
  - Complex navigation flows
  - Dynamic content loading (infinite scroll, load more)
  - Authentication-required pages

- **Comprehensive data collection**
  - Extract structured data from multiple pages
  - Collect data across pagination
  - Gather data requiring multiple interactions
  - Build complete datasets from websites

- **Complex page analysis**
  - Pages with dynamic content or anti-bot measures
  - Need to understand page structure before acting
  - Identify data regions and extraction patterns
  - Discover API endpoints and data sources

- **Building reusable patterns**
  - Create website interaction templates
  - Accumulate knowledge for future visits
  - Share patterns across tasks

## When NOT to Use

❌ **DON'T use this skill when:**

- Simple single-page checks → use standard browser tool
- Static content extraction → use web-fetch
- API-based data access available → use API directly
- User already logged in and just needs navigation → use browser-automation skill
- Quick search or simple fetch → use web-search or web-fetch directly

## Prerequisites

### Required Dependencies

**Primary Mode:**
- **OpenCLI** - Browser automation tool
  - Install: `pip install opencli` or follow OpenCLI installation guide
  - Verify: `opencli --version`
- **LLM Access** - For intelligent page analysis
  - OpenAI API key or compatible LLM endpoint
  - Verify: `opencli llm ask "test"`

**Fallback Mode:**
- **web-fetch tool** - For static content retrieval
- **web-search tool** - For finding related pages

### Environment Setup

```bash
# Initialize environment
python scripts/init_environment.py

# Verify dependencies
python scripts/init_environment.py --check-deps
```

## Core Capabilities

### 1. LLM-Powered Analysis

Uses structured references in `reference/` directory:

- **Page Analysis** (`reference/page_analysis.md`)
  - Page type identification
  - Layout pattern detection
  - Data region mapping
  - Pagination discovery

- **Element Analysis** (`reference/element_analysis.md`)
  - Interactivity detection
  - Purpose inference
  - Importance ranking
  - Element grouping

- **Network Analysis** (`reference/network_analysis.md`)
  - API endpoint discovery
  - Data source identification
  - Direct API potential assessment

### 2. Fallback Mechanism

When browser tools (OpenCLI, browser-automation) are unavailable, automatically falls back to:

- **web-fetch** - Retrieve static page content
- **web-search** - Find relevant pages and information

**Fallback Workflow:**
1. Detect browser tool availability
2. If unavailable → use web-fetch to get page content
3. Use web-search to find related pages
4. Apply same analysis references to fetched content
5. Store results in pattern files

**Limitations of Fallback:**
- Cannot interact with dynamic content
- Cannot submit forms or click buttons
- Cannot handle authentication
- Limited to publicly accessible pages

### 3. Memory System

Markdown-based patterns in `browser-patterns/` directory:

```
browser-patterns/
├── sites/
│   ├── example.com.md    # Website patterns
│   └── INDEX.md          # Pattern index
└── plans/
    ├── task-001.md       # Browsing plans
    └── INDEX.md          # Plan index
```

### 4. Python Scripts

Helper scripts in `scripts/` directory:

- `browser_operations.py` - Browser navigation and interaction operations
- `file_operations.py` - Simple file manipulation utilities
- `memory_manager.py` - Long-term pattern file management
- `init_environment.py` - Environment setup

## Usage

### 1. Initialize Environment

```bash
python scripts/init_environment.py
```

Creates:
- `browser-patterns/sites/` directory
- `browser-patterns/plans/` directory
- `states/` directory (for context isolation)
- Index files

### 2. Context Isolation with State Files

**Key Concept**: Instead of keeping page state in memory, write it to files for better isolation.

```python
from scripts.file_operations import FileOps

# Simple file operations
FileOps.write("states/state-001.md", page_state_content)
content = FileOps.read("states/state-001.md")

# Replace section
FileOps.replace_section(
    "states/state-001.md",
    start_marker="## Page Elements",
    end_marker="## Analysis",
    new_content=elements_table
)

# Replace by line numbers
FileOps.replace_lines(
    "states/state-001.md",
    start_line=10,
    end_line=15,
    new_lines=["New line 1", "New line 2"]
)
```

**Benefits**:
- Agent doesn't need to remember all context
- State persists across sessions
- Can be reviewed/edited manually
- Enables parallel processing of multiple pages

### 3. Use References for Analysis

Agent reads reference files and creates structured state files:

**Step 1: Read Analysis Reference**
```markdown
Read reference/page_analysis.md
```

**Step 2: Apply to Page Content**
- Analyze page structure using reference framework
- Identify page type, layout, data regions
- Generate structured JSON analysis

**Step 3: Create State File**
```markdown
Use reference/page_state_template.md
Create states/state-{id}.md with analysis results
```

**Step 4: Update State File**
```python
FileOps.replace_section(
    "states/state-001.md",
    "## Page Elements",
    "## Analysis",
    elements_table
)
```

### 4. Save to Memory

```python
from scripts.memory_manager import MemoryManager

manager = MemoryManager()

# Create pattern file
pattern_content = """# example.com

> Domain: example.com
> Created: 2026-04-28

## Page Types

### listing

- Product grid layout
- Pagination controls

## Selectors

- search_box: #search
"""

manager.create_site_pattern("example.com", pattern_content)

# Read pattern
content = manager.read_site_pattern("example.com")

# Search patterns
results = manager.search_patterns("product")

# List all patterns
patterns = manager.list_site_patterns()
```

### 5. Browser Operations

**Reference**: See `reference/browser_operations_reference.md` for detailed operations guide.

**Core Operations:**
- **Navigation**: open(), get_url(), get_title()
- **State**: get_state(), extract()
- **Interaction**: click(), type_text(), scroll()
- **Data**: get_text(), screenshot()
- **Network**: network()

**Code Example:**
```python
from scripts.browser_operations import DeepBrowser

browser = DeepBrowser()

# Open page
browser.open("https://example.com")

# Get state
state = browser.get_state()

# Interact
browser.click(target=123)
browser.type_text(target=456, text="query")

# Extract
data = browser.extract()
```

### 6. Fallback Usage (When Browser Unavailable)

When browser tools are not available, use web-fetch and web-search:

```markdown
# Fallback workflow
1. Try browser.open() → fails
2. Detect browser unavailable
3. Use web-fetch to get page content
4. Use web-search to find related pages
5. Apply analysis references to fetched content
6. Store results in pattern files
```

**Example:**
```markdown
# Instead of browser interaction
web-fetch url="https://example.com"
→ Returns static HTML content

# Search for related pages
web-search query="example.com products"
→ Returns list of relevant URLs

# Analyze fetched content
Read reference/page_analysis.md
Apply to fetched HTML
→ Returns structured analysis
```

**Note:** Fallback has limitations - cannot interact with dynamic content, forms, or authenticated pages.

## Analysis Workflow

### Step 1: Create State File

1. Generate unique state ID
2. Create state file in `states/` directory
3. Initialize with basic structure

### Step 2: Capture Page State

1. Open target URL
2. Get page state
3. Update state file with:
   - Basic info (URL, title)
   - Page elements (table format)
   - Network requests

### Step 3: Apply Analysis References

1. Read `reference/page_analysis.md`
2. Apply to page content
3. Update state file with analysis results

### Step 4: Generate Action Plan

1. Read `reference/element_analysis.md`
2. Identify interactive elements
3. Update state file with suggested actions

### Step 5: Execute and Update

1. Agent reads state file
2. Executes suggested actions
3. Updates state file with results
4. Adds notes for observations

### 6. Save to Long-term Memory

1. Extract patterns from state
2. Save to pattern files
3. Update statistics

## Memory Format

### State File Structure

```markdown
# Page State: state-001

> State ID: state-001
> Created: 2026-04-28T10:00:00Z
> Updated: 2026-04-28T10:30:00Z

## Basic Info

- **URL**: https://example.com/products
- **Title**: Product Listing
- **Status**: analyzed

## Page Elements

| Ref | Tag | Text | Visible | Role |
|-----|-----|------|---------|------|
| 1 | button | Search | ✓ | button |
| 2 | input | | ✓ | textbox |
| 3 | a | Next Page | ✓ | link |

## Analysis

**Page Type**: listing (confidence: 0.95)

**Layout**: two-column

### Data Regions

- `.product-grid`: Main product listing
- `.sidebar`: Filter options

### Pagination

- Type: click
- Selector: `.next-page`
- Description: Click to load next page

### Content Summary

- Topic: Product catalog
- Language: en
- Entities: products, categories

## Suggested Actions

1. 🔴 **click**
   - Target: `.search-button`
   - Purpose: Submit search query
   - Priority: high

2. 🟡 **type**
   - Target: `#search-input`
   - Purpose: Enter search terms
   - Priority: medium

## Network Requests

Total: 15 requests

| Method | URL | Type |
|--------|-----|------|
| GET | /api/products | application/json |
| POST | /api/search | application/json |

## Notes

- Initial page load successful (10:00:05)
- Found 50 products on first page (10:00:10)
```

### Pattern File Structure

```markdown
# example.com

> Domain: example.com
> Learned: 2026-04-28T10:00:00Z
> Last used: 2026-04-28T10:30:00Z
> Success: 5 | Failure: 0

## Page Types

<!-- Document discovered page types -->

### listing

**Indicators:**
- Product grid layout
- Pagination controls

**Data Regions:**
| Selector | Type | Description |
|----------|------|-------------|
| .product-grid | product-list | Main listing |

**Pagination:**
- Type: click
- Selector: .next-page

## Selectors

| Name | Selector |
|------|----------|
| search_box | #search |
| submit_btn | .search-btn |

## Notes

<!-- Add observations -->
```

### Plan File Structure

```markdown
# Browsing Plan: Collect product data

> Task ID: task-001
> Goal: Collect product data
> Depth: 0/3
> Status: pending
> Created: 2026-04-28T10:00:00Z

## Progress

- Total steps: 5
- Completed: 2
- In progress: 1
- Pending: 2

## Steps

### Step 1: Navigate to listing ✅

- Action: open
- Params: {"url": "https://example.com/products"}
- Expected: Product listing page loaded

### Step 2: Extract products ✅

- Action: extract
- Params: {"selector": ".product-item"}
- Expected: Product data collected

## Collected Data

<!-- Add collected data -->
```

## Integration with Agent

The agent uses this skill by:

1. **Reading reference** from `reference/` directory
2. **Applying reference** to current context
3. **Executing actions** via browser operations
4. **Storing results** in pattern files
5. **Learning patterns** for future use

## Best Practices

1. **Always initialize** environment first
2. **Read references** before analysis
3. **Save patterns** after successful interactions
4. **Update statistics** to track success rates
5. **Use direct APIs** when discovered
6. **Combine with standard tools** for simple cases

## Limitations

### Primary Mode (Browser Tools)
- Requires OpenCLI or browser-automation tool
- LLM needed for reference-based analysis
- Pattern storage grows with site diversity
- Initial analysis slower than keyword matching

### Fallback Mode (web-fetch + web-search)
- Cannot interact with dynamic content
- Cannot submit forms or click buttons
- Cannot handle authentication
- Limited to publicly accessible pages
- No real-time page state monitoring
- Cannot capture network requests

## Related Skills

### Primary Tools
- `browser-automation` - Standard browser control
- `web-fetch` - Simple content extraction
- `web-search` - Search and find information

### Fallback Tools
- `web-fetch` + `web-search` - Alternative when browser unavailable

### Domain Skills
- `market-research-collector` - Data collection workflows
