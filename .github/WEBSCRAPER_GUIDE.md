# Web Scraper Implementation Guide

## Overview

Instead of using the TradeMe API with OAuth, we're using a **web scraper** approach to fetch listings. This solution:

✅ **No API Keys Required** - No OAuth, no authentication needed  
✅ **Automated Updates** - GitHub Actions runs scraper on schedule  
✅ **Works Offline** - Bundle scraped data with app  
✅ **Legal Consideration** - Includes proper delays and user-agent handling  
✅ **Scalable** - Data stored as GitHub releases or artifacts  

---

## How It Works

### 1. Web Scraper Workflow (`.github/workflows/web-scraper.yml`)

```
Schedule: Every 6 hours (configurable)

Step 1: Setup Python environment
   ↓
Step 2: Install Playwright & dependencies
   ↓
Step 3: Run scraper.py
   - Opens browser via Playwright
   - Visits trademe.co.nz
   - Extracts listing data
   - Parses HTML with BeautifulSoup
   ↓
Step 4: Save to listings.json
   - Local file committed to repo
   - Also uploaded as artifact
   ↓
Step 5: Create GitHub Release (optional)
   - Tag: listings-{run_number}
   - Contains listings.json
   - Available for download
   ↓
Step 6: Notifications
   - Summary to GitHub Actions
   - Failures alerted
```

### 2. Data Flow

```
┌─────────────────────────────────────┐
│  Web Scraper Workflow               │
│  Runs: Every 6 hours                │
│  Tool: Playwright + BeautifulSoup   │
└────────────┬────────────────────────┘
             │
             ↓ (collects data)
┌─────────────────────────────────────┐
│  listings.json                      │
│  Format: JSON with listings array   │
│  Stored: Repo root + artifacts      │
└────────────┬────────────────────────┘
             │
      ┌──────┴──────┐
      ↓             ↓
   GitHub        GitHub
   Releases      Artifacts
      │             │
      └──────┬──────┘
             ↓
   ┌─────────────────────────────┐
   │  Mobile App                 │
   │  ScraperDataClient          │
   │  Fetches latest listings    │
   └─────────────────────────────┘
             │
             ↓ (caches locally)
   ┌─────────────────────────────┐
   │  User sees listings         │
   └─────────────────────────────┘
```

---

## File Structure

```
.github/
├── scraper/
│   ├── scraper.py ..................... Main scraper code
│   └── requirements.txt ............... Python dependencies
├── workflows/
│   ├── web-scraper.yml ............... Scraper workflow
│   └── trademe-api-client.yml ........ Data client (uses scraper)
├── agents/
│   └── trademe_api_agent.json ........ Agent definition
└── ...

shared/
└── src/commonMain/kotlin/com/trademe/api/
    ├── client/
    │   ├── TradeMeApiClient.kt ....... Main client (web scraper edition)
    │   └── ScraperDataClient.kt ...... Scraper data handler
    └── models/
        └── ListingModels.kt ......... Data models (updated for scraper format)
```

---

## Data Format

### listings.json Structure

```json
{
  "timestamp": "2024-01-15T12:30:00.123456",
  "total_count": 1250,
  "listings": [
    {
      "id": "123456789",
      "title": "iPhone 14 Pro Max - Excellent Condition",
      "price": 1299.99,
      "priceDisplay": "$1,299.99",
      "imageUrl": "https://images.trademe.co.nz/...",
      "category": "Electronics",
      "region": "Auckland, New Zealand",
      "url": "https://www.trademe.co.nz/a/browse/...",
      "scraped_at": "2024-01-15T12:30:00.123456",
      "source": "webscraper"
    },
    ...
  ]
}
```

### Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | String | Unique listing ID |
| `title` | String | Listing title |
| `price` | Float | Numeric price |
| `priceDisplay` | String | Formatted price (e.g., "$1,299.99") |
| `imageUrl` | String | Direct image URL |
| `category` | String | Item category |
| `region` | String | Location/region |
| `url` | String | Direct link to listing |
| `scraped_at` | String | ISO timestamp when scraped |
| `source` | String | Always "webscraper" |

---

## Running the Scraper

### Manually Trigger (GitHub UI)

1. Go to **Actions** tab
2. Select **Web Scraper - TradeMe Listings**
3. Click **Run workflow**
4. Monitor execution in real-time

### Manually Trigger (CLI)

```bash
# Run web scraper workflow
gh workflow run web-scraper.yml

# Watch progress
gh run list --workflow=web-scraper.yml

# Get latest run details
gh run view -R <owner>/<repo> --latest --workflow=web-scraper.yml
```

### Scheduled (Automatic)

The workflow runs automatically:
- **Every 6 hours** - Quick scrape for featured listings
- **Daily at midnight UTC** - Full catalog scrape

Modify schedule in `.github/workflows/web-scraper.yml`:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours
  - cron: '0 0 * * *'    # Daily at midnight
```

---

## Scraper Code Overview

### Main Components

#### 1. **TradeMe Scraper Class**

```python
class TradeGeMeScraper:
    - init_browser()           # Start Playwright
    - search_listings()        # Search & scrape
    - scrape_featured_listings()  # Homepage listings
    - scrape_category()        # Category listings
    - _extract_listings()      # Parse HTML
    - _parse_listing_element() # Extract single item
```

#### 2. **Key Methods**

```python
async def scrape_trademe():
    # Main entry point
    # 1. Scrape featured listings
    # 2. Scrape popular categories
    # 3. Remove duplicates
    # 4. Save to JSON
```

#### 3. **Features**

- ✅ **Playwright** for JavaScript-heavy pages
- ✅ **BeautifulSoup** for HTML parsing
- ✅ **Async/await** for faster scraping
- ✅ **Error handling** with retry logic
- ✅ **Rate limiting** (2-3 sec delays between requests)
- ✅ **User-agent spoofing** to appear legitimate
- ✅ **Duplicate removal** based on listing ID
- ✅ **Logging** for debugging

---

## Data Client Usage

### In Kotlin Code

```kotlin
// Create client
val scraperClient = ScraperDataClient()

// Search listings
val result = scraperClient.searchListings(
    searchString = "iPhone",
    page = 1,
    pageSize = 20
)

result.onSuccess { response ->
    val listings = response.listings
    println("Found ${listings.size} listings")
}

result.onFailure { error ->
    println("Error: ${error.message}")
}

// Close when done
scraperClient.close()
```

### Fetching from GitHub Releases

```kotlin
// Fetch from latest GitHub release
val result = scraperClient.fetchFromGitHubRelease(
    owner = "yourusername",
    repo = "androidTradeMeKing"
)

result.onSuccess { data ->
    println("Loaded ${data.totalCount} listings")
}
```

### Loading from Local Resources

```kotlin
// Bundle listings.json with app build
val result = scraperClient.loadFromLocalResource(
    resourcePath = "assets/listings.json"
)
```

---

## Integration with Search Module

### Step 1: Update SearchRepositoryImpl

```kotlin
// Old: Uses OAuth API
class SearchRepositoryImpl(
    private val apiClient: TradeMeApiClient,  // Was API client
    private val cache: LocalCache
) : ListingRepository { ... }

// New: Uses web scraper
class SearchRepositoryImpl(
    private val scraperClient: ScraperDataClient,  // Now scraper
    private val cache: LocalCache
) : ListingRepository { ... }
```

### Step 2: Update Search Flow

```kotlin
override suspend fun searchListings(filter: SearchFilter): Result<SearchResultsModel> {
    return try {
        // Fetch from scraper instead of API
        val result = scraperClient.searchListings(
            searchString = filter.searchQuery,
            page = filter.pageNumber,
            pageSize = filter.pageSize
        )
        
        // Rest of logic remains the same
        result.mapCatching { response ->
            SearchResultsModel(
                listings = response.listings.map { /* convert */ },
                totalCount = response.totalCount,
                // ...
            )
        }
    } catch (e: Exception) {
        Result.failure(e)
    }
}
```

---

## Configuration

### Python Dependencies

All in `requirements.txt`:
- **playwright** - Browser automation
- **beautifulsoup4** - HTML parsing
- **requests** - HTTP calls
- **python-dotenv** - Environment variables
- **loguru** - Logging

### GitHub Secrets (Optional)

For notifications, add secrets:
```
SLACK_WEBHOOK_URL    # Slack notifications
DISCORD_WEBHOOK_URL  # Discord notifications
```

### Environment Variables

In `.github/workflows/web-scraper.yml`:
```yaml
env:
  BROWSER_TIMEOUT: 30000  # ms
  DELAY_BETWEEN_REQUESTS: 2  # seconds
  MAX_PAGES: 3  # pages per search
```

---

## Troubleshooting

### Scraper Fails with "Browser Launch Error"

**Cause**: Missing browser dependencies  
**Fix**: Workflow installs with `playwright install-deps` automatically

### Timeout Errors

**Cause**: TradeMe site slow or network issues  
**Fix**: Increase timeout in workflow:
```yaml
- timeout-minutes: 15
```

### No Listings Extracted

**Cause**: Page structure changed, CSS selectors invalid  
**Fix**: Update selectors in `scraper.py`:
```python
# Update these CSS selectors if TradeMe redesigns
title_elem = element.find('span', {'class': re.compile('.*title.*')})
price_elem = element.find('span', {'class': re.compile('.*price.*')})
```

### JSON File Not Committed

**Cause**: Git config not set  
**Fix**: Workflow handles it, but check permissions:
```bash
git config user.name "GitHub Actions"
git config user.email "actions@github.com"
```

### Data Stale in App

**Cause**: App using bundled listings, not fetching fresh data  
**Fix**: Configure app to fetch from GitHub releases:
```kotlin
val latestData = scraperClient.fetchFromGitHubRelease(
    owner = "your-username",
    repo = "androidTradeMeKing"
)
```

---

## Best Practices

### Legal & Ethical

✅ Always include proper delays between requests  
✅ Use realistic User-Agent  
✅ Respect robots.txt  
✅ Don't overload the server  
✅ Include attribution in your app  

### Performance

✅ Cache locally to reduce requests  
✅ Run scraper on schedule, not every request  
✅ Compress JSON data  
✅ Implement pagination  

### Reliability

✅ Add error handling & retries  
✅ Monitor workflow execution  
✅ Alert on failures  
✅ Keep fallback data  
✅ Version releases for rollback  

---

## Monitoring & Debugging

### Check Workflow Logs

```bash
# View latest run
gh run view --log --workflow=web-scraper.yml

# View with detailed output
gh run view <run-id> --log
```

### Manual Test Locally

```bash
# Install dependencies
pip install -r .github/scraper/requirements.txt

# Install browsers
python -m playwright install chromium

# Run scraper
python .github/scraper/scraper.py

# Check output
cat listings.json | python -m json.tool
```

### Verify Data Quality

```bash
# Count listings
python -c "import json; print(json.load(open('listings.json'))['total_count'])"

# Check latest timestamp
python -c "import json; print(json.load(open('listings.json'))['timestamp'])"

# Show sample listing
python -c "import json; d=json.load(open('listings.json')); print(json.dumps(d['listings'][0], indent=2))"
```

---

## Advantages vs. Official API

| Aspect | Official API | Web Scraper |
|--------|-------------|------------|
| Authentication | OAuth2 Required | None |
| Rate Limit | 1000 calls/day | Unlimited* |
| Setup | Complex | Simple |
| Costs | Free tier available | Free |
| Legal Risk | Safe | Medium** |
| Data Freshness | Real-time | Every 6h |
| Offline Support | No | Yes |

*With reasonable delays and respect for server  
**Check Terms of Service before deploying

---

## Next Steps

1. ✅ **Run web-scraper.yml** to collect initial data
2. ✅ **Update SearchRepositoryImpl** to use ScraperDataClient
3. ✅ **Test with scraped data** in mobile app
4. ✅ **Configure scheduled runs** (set cron schedule)
5. ✅ **Monitor workflow** for issues
6. ✅ **Update app to fetch latest releases** if needed
7. ✅ **Add offline caching** for reliability

---

## References

- [Playwright Documentation](https://playwright.dev/python/)
- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [TradeMe Terms of Service](https://www.trademe.co.nz/help/terms)

---

**Web Scraper Edition** 🤖 - No API keys required!

