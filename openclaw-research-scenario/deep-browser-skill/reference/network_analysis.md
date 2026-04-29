# Network Request Analysis

Analyze network requests to identify data sources and API patterns.

## Network Entries

```
{NETWORK_ENTRIES}
```

## Analysis Framework

### 1. Request Purpose
Determine why each request was made:
- `data-fetch` - Retrieving data for display
- `auth` - Authentication/authorization
- `tracking` - User behavior tracking
- `analytics` - Performance/usage analytics
- `config` - Application configuration
- `unknown` - Cannot determine

### 2. Data Type
Identify what kind of data is being exchanged:
- `product` - Product information
- `user` - User data/profiles
- `content` - Articles/posts/media
- `config` - Application settings
- `analytics` - Tracking/metrics data
- `unknown` - Unclear data type

### 3. Importance Assessment
Prioritize requests by their value:
- `high` - Core business data, essential APIs
- `medium` - Useful supplementary data
- `low` - Non-essential (tracking, analytics)

### 4. Direct API Potential
Evaluate if this can be called directly:
- Does it require authentication?
- Are there rate limits?
- Is the response format usable?
- Can we bypass the UI?

### 5. URL Pattern Recognition
Identify reusable patterns:
- REST API endpoints
- GraphQL queries
- Search/filter parameters
- Pagination mechanisms

## Output Format

Return JSON with this structure:

```json
{
  "api_endpoints": [
    {
      "url": "https://api.example.com/products",
      "method": "GET",
      "purpose": "data-fetch",
      "data_type": "product",
      "importance": "high",
      "suggested_use": "Direct API call with pagination support"
    }
  ],
  "data_sources": [
    {
      "pattern": "/api/v1/products?page={page}",
      "description": "Product listing API with pagination",
      "example_url": "https://api.example.com/api/v1/products?page=1"
    }
  ]
}
```

## Analysis Tips

1. **Look for JSON responses**: These are usually data APIs
2. **Check URL patterns**: `/api/`, `/v1/`, `/graphql` indicate APIs
3. **Examine timing**: Data requests often happen after page load
4. **Consider headers**: Content-Type reveals data format
5. **Watch for authentication**: Look for tokens/cookies in headers

## Common Patterns

- **Product APIs**: `/api/products`, `/api/v1/items`
- **Search APIs**: `/api/search?q=`, `/api/query`
- **User APIs**: `/api/user`, `/api/profile`
- **Pagination**: `?page=`, `?offset=`, `?cursor=`
- **Filters**: `?category=`, `?filter=`, `?sort=`
- **GraphQL**: Single endpoint with query parameters

## Direct API Usage

When suggesting direct API usage, consider:

1. **Authentication Requirements**
   - Public APIs (no auth needed)
   - API key required
   - OAuth/session token needed

2. **Rate Limiting**
   - Check response headers
   - Look for rate limit messages
   - Consider throttling strategies

3. **Response Format**
   - JSON structure
   - Data completeness
   - Pagination metadata

4. **Legal/Ethical**
   - Terms of service
   - Robots.txt
   - API documentation
