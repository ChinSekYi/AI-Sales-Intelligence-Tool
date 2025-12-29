import json
import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from newsapi import NewsApiClient

from config.default_triggers import DEFAULT_TRIGGERS

# Load environment variables from config/.env
config_env_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "config", ".env"
)
load_dotenv(dotenv_path=config_env_path)
newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))


def fetch_news_by_query(
    query='patent OR "intellectual property"', days_back=30, sort_by="publishedAt"
):
    """
    Fetch news articles from NewsAPI by search query
    Search for news articles that mention a specific topic or keyword

    Args:
        query: Search query string
        days_back: Number of days to look back
        sort_by: Sort order (popularity, publishedAt, relevancy)
    """
    from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    to_date = datetime.now().strftime("%Y-%m-%d")
    exclude_domains = "arxiv.org,ieee.org,springer.com"  # exclude journal articles

    try:
        response = newsapi.get_everything(
            q=query,
            from_param=from_date,
            to=to_date,
            sort_by=sort_by,
            language="en",
            exclude_domains=exclude_domains,
        )
        track_api_usage()  # Track this API call
        return response
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None


def fetch_top_headlines(country="sg", category=None, sources=None):
    """
    Fetch top headlines from NewsAPI
    Get the current top headlines for a country or category

    Args:
        country: Country code (e.g., 'sg', 'us', 'gb', 'cn', 'au', 'in', etc.)
        category: Category (general, business, technology, science, health, sports, entertainment, etc.)
        sources: Comma-separated string of news sources to include (e.g., 'bbc-news,cnn')
    """
    try:
        response = newsapi.get_top_headlines(
            country=country, category=category, sources=sources
        )
        track_api_usage()  # Track this API call
        return response
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None


def fetch_sales_triggers(
    trigger_queries=None, days_back=7, sort_by="publishedAt", region=None
):
    """
    Fetch sales trigger news for Patsnap's sales team
    Searches for articles with specified keywords indicating potential sales triggers

    Args:
        trigger_queries: Dict of {trigger_name: query_string}. If None, uses DEFAULT_TRIGGERS from config.
        days_back: Number of days to look back
        sort_by: Sort order (popularity, publishedAt, relevancy)
        region: Optional region filter (e.g., 'Singapore', 'Asia', 'United States')

    Returns:
        dict: Combined news data with articles from all sales trigger queries
    """
    # Use default triggers if none provided
    if trigger_queries is None:
        trigger_queries = DEFAULT_TRIGGERS

    # Add region filter if specified
    queries_with_region = {}
    if region:
        for name, query in trigger_queries.items():
            queries_with_region[name] = f"({query}) AND {region}"
    else:
        queries_with_region = trigger_queries

    all_articles = []
    from_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    to_date = datetime.now().strftime("%Y-%m-%d")

    for trigger_name, query in queries_with_region.items():
        try:
            response = newsapi.get_everything(
                q=query,
                from_param=from_date,
                to=to_date,
                sort_by=sort_by,
                language="en",
            )
            track_api_usage()  # Track this API call

            if response.get("status") == "ok" and response.get("articles"):
                # Add source query tag to each article
                for article in response["articles"]:
                    article["trigger_type"] = (
                        trigger_name  # Use short name instead of query
                    )
                all_articles.extend(response["articles"])
                print(f"Found {len(response['articles'])} articles for: {query}")
        except Exception as e:
            print(f"Error fetching news for '{query}': {e}")
            continue

    # Remove duplicates based on URL
    unique_articles = deduplicate_articles(all_articles)

    return {
        "status": "ok",
        "totalResults": len(unique_articles),
        "articles": unique_articles,
    }


# Helper function for API usage tracking
def track_api_usage():
    """Track API calls locally to estimate quota usage"""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(data_dir, exist_ok=True)
    usage_file = os.path.join(data_dir, ".api_usage.json")

    today = datetime.now().date().isoformat()

    # Load existing usage
    usage_data = {}
    if os.path.exists(usage_file):
        try:
            with open(usage_file, "r") as f:
                usage_data = json.load(f)
        except:
            usage_data = {}

    # Update today's count
    if today not in usage_data:
        usage_data[today] = 0
    usage_data[today] += 1

    # Clean up old entries (keep last 7 days only)
    cutoff_date = (datetime.now() - timedelta(days=7)).date().isoformat()
    usage_data = {k: v for k, v in usage_data.items() if k >= cutoff_date}

    # Save
    with open(usage_file, "w") as f:
        json.dump(usage_data, f, indent=2)


def get_api_usage_today():
    """Get number of API calls made today"""
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    usage_file = os.path.join(data_dir, ".api_usage.json")
    today = datetime.now().date().isoformat()

    if os.path.exists(usage_file):
        try:
            with open(usage_file, "r") as f:
                usage_data = json.load(f)
                return usage_data.get(today, 0)
        except:
            return 0
    return 0


# Helper function to deduplicate articles
def deduplicate_articles(articles):
    """Remove duplicate articles based on URL"""
    seen_urls = set()
    unique = []
    for article in articles:
        url = article.get("url")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique.append(article)
    return unique


def save_news_to_file(news_data, filename="news_data.json", query_params=None):
    """
    Save news data to a JSON file in the data directory with metadata

    Args:
        news_data: The news data dict from API
        filename: Name of file to save to
        query_params: Optional dict of query parameters used (days_back, region, etc.)
    """
    if news_data:
        data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        os.makedirs(data_dir, exist_ok=True)

        # Add metadata
        fetched_at = datetime.now()
        data_with_metadata = {
            "metadata": {
                "fetched_at": fetched_at.isoformat(),
                "expires_at": (fetched_at + timedelta(hours=24)).isoformat(),
                "query_params": query_params or {},
            },
            "status": news_data.get("status"),
            "totalResults": news_data.get("totalResults"),
            "articles": news_data.get("articles", []),
        }

        filepath = os.path.join(data_dir, filename)
        with open(filepath, "w") as f:
            json.dump(data_with_metadata, f, indent=2)
        print(f"News data saved to {filepath}")

        return filepath
    return None


if __name__ == "__main__":
    print("Fetching sales trigger news for Patsnap (Singapore focus)...")
    print("=" * 50)

    # Fetch sales triggers for Singapore
    news = fetch_sales_triggers(days_back=7, sort_by="publishedAt", region="Singapore")

    if news:
        print(f"\nStatus: {news.get('status')}")
        print(f"Total Unique Articles: {news.get('totalResults')}")
        print(f"Articles Retrieved: {len(news.get('articles', []))}")

        # Save to file
        save_news_to_file(news, filename="sales_triggers.json")

        # Print first 3 articles as examples
        if news.get("articles"):
            print("\n" + "=" * 50)
            print("Sample Sales Trigger Articles:")
            print("=" * 50)
            for i, article in enumerate(news["articles"][:3], 1):
                print(f"\n{i}. {article.get('title')}")
                print(f"   Source: {article.get('source', {}).get('name')}")
                print(f"   Published: {article.get('publishedAt')}")
                print(f"   Trigger Type: {article.get('trigger_type')}")
                print(f"   URL: {article.get('url')}")
