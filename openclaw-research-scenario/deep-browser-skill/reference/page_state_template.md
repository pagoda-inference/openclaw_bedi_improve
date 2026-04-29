# Page State Template

Use this template to create page state files in `states/` directory.

## Template

```markdown
# Page State: {state-id}

> State ID: {state-id}
> Created: {timestamp}
> Updated: {timestamp}

## Basic Info

- **URL**: {page-url}
- **Title**: {page-title}
- **Status**: {pending|analyzing|analyzed|failed}

## Page Elements

| Ref | Tag | Text | Visible | Role |
|-----|-----|------|---------|------|
| 1 | {tag} | {text} | {✓|✗} | {role} |
| 2 | ... | ... | ... | ... |

## Analysis

**Page Type**: {page-type} (confidence: {confidence})

**Layout**: {layout-pattern}

### Data Regions

- `{selector}`: {description}

### Pagination

- Type: {pagination-type}
- Selector: `{selector}`
- Description: {description}

### Content Summary

- Topic: {main-topic}
- Language: {language}
- Entities: {entity-list}

## Suggested Actions

1. {priority-icon} **{action-type}**
   - Target: `{selector}`
   - Purpose: {purpose}
   - Priority: {high|medium|low}

## Network Requests

Total: {count} requests

| Method | URL | Type |
|--------|-----|------|
| {method} | {url} | {content-type} |

## Notes

- {timestamp}: {note-content}
```

## Usage

1. Copy template to `states/state-{id}.md`
2. Replace placeholders with actual values
3. Use FileOps to update sections as needed

## Example

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

## Analysis

**Page Type**: listing (confidence: 0.95)

**Layout**: two-column

### Data Regions

- `.product-grid`: Main product listing

### Pagination

- Type: click
- Selector: `.next-page`
- Description: Click to load next page

## Suggested Actions

1. 🔴 **click**
   - Target: `.search-button`
   - Purpose: Submit search query
   - Priority: high

## Network Requests

Total: 15 requests

| Method | URL | Type |
|--------|-----|------|
| GET | /api/products | application/json |

## Notes

- 10:00:05: Initial page load successful
- 10:00:10: Found 50 products on first page
```
