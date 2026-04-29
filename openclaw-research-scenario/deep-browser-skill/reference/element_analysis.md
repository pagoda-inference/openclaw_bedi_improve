# Element Interactivity Analysis

Analyze page elements to determine interactivity and purpose.

## Element List

```
{ELEMENTS}
```

## Analysis Framework

### 1. Interaction Types
Identify how users can interact with each element:
- `click` - Buttons, links, clickable elements
- `type` - Input fields, text areas
- `select` - Dropdown menus
- `scroll` - Scrollable regions
- `hover` - Hover-triggered actions
- `drag` - Draggable elements

### 2. Purpose Inference
Determine why each interactive element exists:
- Navigation (go to another page)
- Action (perform an operation)
- Input (collect user data)
- Display (show/hide content)
- Filter (modify displayed data)

### 3. Importance Ranking
Prioritize elements by their value:
- `high` - Critical for main task (e.g., submit button, main navigation)
- `medium` - Useful but not essential (e.g., filters, secondary nav)
- `low` - Optional or rarely used (e.g., help links, minor actions)

### 4. Expected Outcomes
Predict what will happen when interacting:
- Page navigation
- Content update
- State change
- Data submission
- Modal/dialog opening

### 5. Element Grouping
Identify related elements that work together:
- Forms (input + submit)
- Navigation menus (multiple links)
- Data lists (repeated items)
- Control groups (related actions)

## Output Format

Return JSON with this structure:

```json
{
  "interactive_elements": [
    {
      "ref": 123,
      "interaction_type": "click",
      "purpose": "Submit search query",
      "importance": "high",
      "expected_outcome": "Navigate to search results"
    }
  ],
  "element_groups": [
    {
      "refs": [1, 2, 3],
      "group_type": "form",
      "purpose": "Search functionality"
    }
  ]
}
```

## Analysis Tips

1. **Look for visual cues**: Buttons, links, inputs usually have distinct styling
2. **Consider context**: An input in a header is likely search, in a form is likely data entry
3. **Prioritize by position**: Top-of-page elements are usually more important
4. **Group related items**: Multiple inputs with a submit button form a logical group
5. **Think about user goals**: What would a user want to do on this page?

## Common Patterns

- **Search**: Input + button/magnifying glass icon
- **Navigation**: Multiple links in header/sidebar
- **Forms**: Multiple inputs + submit button
- **Filters**: Dropdowns + checkboxes + apply button
- **Actions**: Buttons like "Add to cart", "Submit", "Save"
- **Pagination**: Numbered links or "Next/Previous"
