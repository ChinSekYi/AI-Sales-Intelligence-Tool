# NewsAPI Information

## About NewsAPI

**Website:** https://newsapi.org

NewsAPI is a simple REST API for searching and retrieving live news articles from around the web.

## Free Tier Limitations

- **100 requests per day** - No extra requests available
- **Articles have a 24-hour delay** - Live headlines not available
- **Search articles up to a month old** - Historical data limited
- **Free for development only** (not for production)

## API Endpoint Used

### `/v2/everything`
Search through millions of articles from various sources.
- Used in: `fetch_news_by_query()` and `fetch_sales_triggers()`
- Searches: title, description, and content fields
- Filters: query, date range, language, sort order

**Search Operators:**
- Exact phrases: `"funding round"`
- Must include: `+bitcoin`
- Must exclude: `-bitcoin`
- Boolean logic: `crypto AND (ethereum OR litecoin) NOT bitcoin`

**Sort Options:**
- `relevancy` - Most closely related to query
- `popularity` - Articles from popular sources
- `publishedAt` - Newest articles first (default)

## Rate Limiting

With 100 requests/day, `fetch_sales_triggers()` makes **3 API calls** (one per active trigger type).
- ~33 sales trigger fetches per day maximum
- Mix with custom searches as needed
