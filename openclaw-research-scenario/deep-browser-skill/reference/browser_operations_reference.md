# Browser Operations Reference

This document describes available browser operations and their usage patterns.

## Core Operations

### Navigation

**open(url)**
- Opens a URL in the browser
- Waits for page load to complete
- Returns: `{"status": "opened", "url": url}`

**get_url()**
- Gets current page URL
- Returns: URL string

**get_title()**
- Gets current page title
- Returns: Title string

### Page State

**get_state()**
- Captures current page state
- Returns: `{"elements": [...], "element_count": n, "has_more_below": bool}`
- Elements include: ref, tag, text, visible, role

**extract()**
- Extracts page content
- Returns: Structured content object

### Interaction

**click(target)**
- Clicks element by reference number
- Waits for resulting changes
- Returns: `{"status": "clicked", "target": ref}`

**type_text(target, text)**
- Types text into input element
- Target: element reference number
- Returns: `{"status": "typed", "target": ref, "text": text}`

**scroll(direction, amount)**
- Scrolls page in specified direction
- Direction: "up" or "down"
- Amount: pixels to scroll
- Returns: `{"status": "scrolled", ...}`

### Data Extraction

**get_text(selector)**
- Gets text content of element
- Selector: CSS selector string
- Returns: Text content string

**screenshot(save_path)**
- Takes screenshot of current page
- Save path: file path to save image
- Returns: `{"status": "captured", "path": path}`

### Network

**network(filter_type)**
- Captures network requests
- Filter type: optional filter string
- Returns: List of network entries

## Usage Patterns

### Pattern 1: Basic Navigation

```
1. open(url)
2. get_state()
3. Analyze state
4. Decide next action
```

### Pattern 2: Form Interaction

```
1. get_state()
2. Identify form elements
3. type_text(input_ref, value)
4. click(submit_ref)
5. get_state() to verify result
```

### Pattern 3: Pagination

```
1. get_state()
2. Extract current page data
3. Identify next page element
4. click(next_page_ref)
5. Wait for load
6. Repeat until done
```

### Pattern 4: Search

```
1. get_state()
2. Find search input
3. type_text(search_input, query)
4. click(search_button)
5. get_state() to analyze results
```

## Error Handling

### Common Errors

**Element not found**
- Cause: Element reference doesn't exist
- Solution: Refresh state with get_state()

**Timeout**
- Cause: Page load or operation took too long
- Solution: Increase timeout or check network

**Browser not responding**
- Cause: Browser crashed or froze
- Solution: Restart browser session

### Recovery Strategies

1. **State Refresh**: Call get_state() to get current element references
2. **Retry**: Retry failed operation with fresh state
3. **Fallback**: Use web-fetch if browser unavailable

## Best Practices

1. **Always check state before interaction**
   - Elements may change after page updates
   - Use get_state() to refresh references

2. **Wait for page stability**
   - After clicks, wait for page to settle
   - Check for loading indicators

3. **Use specific selectors**
   - Prefer IDs and unique classes
   - Avoid generic selectors that may match multiple elements

4. **Handle dynamic content**
   - Scroll to load more content
   - Wait for AJAX requests to complete

5. **Verify actions**
   - After interaction, verify expected result
   - Use get_state() or get_url() to confirm

## Limitations

- Cannot interact with OS-level dialogs
- Limited control over browser settings
- May not work with all anti-bot measures
- Requires JavaScript-enabled browser
