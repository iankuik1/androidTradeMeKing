#!/usr/bin/env python3
"""
TradeMe Web Scraper - Real-Time Scraper
Scrapes listings from trademe.co.nz on-demand for search queries
Can be used as:
1. Command-line tool: python scraper.py --query "iphone"
2. HTTP server: python scraper.py --server
3. Library: import and use TradeGeMeScraper directly
"""

import asyncio
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
import logging
from pathlib import Path
import argparse

from playwright.async_api import async_playwright, Page
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, quote
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TradeGeMeScraper:
    """Web scraper for TradeMe listings"""

    BASE_URL = "https://www.trademe.co.nz"
    SEARCH_URL = f"{BASE_URL}/Browse/Search.aspx"

    def __init__(self, headless: bool = True, timeout: int = 30000):
        self.headless = headless
        self.timeout = timeout
        self.listings: List[Dict] = []
        self.page: Optional[Page] = None
        self.browser = None
        self.context = None

    async def __aenter__(self):
        """Async context manager entry"""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit - cleanup"""
        await self.close()

    async def init_browser(self):
        """Initialize Playwright browser"""
        logger.info("Initializing Playwright browser...")
        try:
            playwright = await async_playwright().start()
            self.browser = await playwright.chromium.launch(
                headless=self.headless,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )
            self.context = await self.browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            self.page = await self.context.new_page()
            logger.info("Browser initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize browser: {e}")
            raise

    async def close(self):
        """Close browser and context"""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            logger.info("Browser closed")
        except Exception as e:
            logger.error(f"Error closing browser: {e}")

    async def search_listings(
        self,
        search_query: str = "",
        category: str = "0",
        page_num: int = 1,
        max_pages: int = 3
    ) -> List[Dict]:
        """
        Search for listings on TradeMe

        Args:
            search_query: Search query string
            category: Category ID (0 = all)
            page_num: Starting page number
            max_pages: Maximum pages to scrape

        Returns:
            List of listing dictionaries
        """
        listings = []

        for page in range(page_num, page_num + max_pages):
            try:
                logger.info(f"Scraping page {page}...")

                # Navigate to search page
                url = f"{self.SEARCH_URL}?q={search_query}&cid={category}&p={page}"
                await self.page.goto(url, wait_until='networkidle')

                # Wait for listings to load
                await self.page.wait_for_selector('[data-listing-id]', timeout=5000)

                # Get page content
                content = await self.page.content()
                soup = BeautifulSoup(content, 'html.parser')

                # Extract listings
                page_listings = await self._extract_listings(soup)
                listings.extend(page_listings)

                logger.info(f"Found {len(page_listings)} listings on page {page}")

                # Be respectful - add delay between requests
                await asyncio.sleep(2)

            except Exception as e:
                logger.warning(f"Error scraping page {page}: {e}")
                continue

        return listings

    async def _extract_listings(self, soup: BeautifulSoup) -> List[Dict]:
        """Extract listing information from page HTML"""
        listings = []

        try:
            # Find all listing containers
            listing_elements = soup.find_all('div', {'data-listing-id': True})
            logger.info(f"Found {len(listing_elements)} listing elements")

            for element in listing_elements:
                try:
                    listing = self._parse_listing_element(element)
                    if listing:
                        listings.append(listing)
                except Exception as e:
                    logger.warning(f"Error parsing individual listing: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error extracting listings: {e}")

        return listings

    def _parse_listing_element(self, element) -> Optional[Dict]:
        """Parse a single listing element"""
        try:
            # Extract basic info
            listing_id = element.get('data-listing-id', '')

            # Title
            title_elem = element.find('span', {'class': re.compile('.*title.*')})
            title = title_elem.get_text(strip=True) if title_elem else "Unknown"

            # Price
            price_elem = element.find('span', {'class': re.compile('.*price.*')})
            price_text = price_elem.get_text(strip=True) if price_elem else "$0"
            price = self._parse_price(price_text)

            # Image URL
            img_elem = element.find('img')
            image_url = img_elem.get('src', '') if img_elem else None
            if image_url and not image_url.startswith('http'):
                image_url = urljoin(self.BASE_URL, image_url)

            # Category
            category_elem = element.find('span', {'class': re.compile('.*category.*')})
            category = category_elem.get_text(strip=True) if category_elem else "Other"

            # Region
            region_elem = element.find('span', {'class': re.compile('.*region.*')})
            region = region_elem.get_text(strip=True) if region_elem else "Unknown Region"

            # Listing URL
            link_elem = element.find('a', {'href': True})
            listing_url = link_elem.get('href', '') if link_elem else ""
            if listing_url and not listing_url.startswith('http'):
                listing_url = urljoin(self.BASE_URL, listing_url)

            return {
                'id': listing_id,
                'title': title,
                'price': price,
                'priceDisplay': price_text,
                'imageUrl': image_url,
                'category': category,
                'region': region,
                'url': listing_url,
                'scraped_at': datetime.now().isoformat(),
                'source': 'webscraper'
            }

        except Exception as e:
            logger.warning(f"Error parsing listing element: {e}")
            return None

    @staticmethod
    def _parse_price(price_text: str) -> float:
        """Extract numeric price from price text"""
        try:
            # Remove currency symbols and text
            price_str = price_text.replace('$', '').replace(',', '').strip()

            # Extract first number
            match = re.search(r'[\d.]+', price_str)
            if match:
                return float(match.group())
            return 0.0
        except Exception as e:
            logger.warning(f"Error parsing price '{price_text}': {e}")
            return 0.0

    async def scrape_featured_listings(self) -> List[Dict]:
        """Scrape featured/popular listings from homepage"""
        logger.info("Scraping featured listings...")

        try:
            await self.page.goto(self.BASE_URL, wait_until='networkidle')
            content = await self.page.content()
            soup = BeautifulSoup(content, 'html.parser')

            return await self._extract_listings(soup)
        except Exception as e:
            logger.error(f"Error scraping featured listings: {e}")
            return []

    async def scrape_category(self, category_id: str, max_pages: int = 2) -> List[Dict]:
        """Scrape all listings in a specific category"""
        logger.info(f"Scraping category {category_id}...")
        return await self.search_listings(
            search_query="",
            category=category_id,
            page_num=1,
            max_pages=max_pages
        )


async def scrape_trademe(search_query: str = "", max_pages: int = 2) -> List[Dict]:
    """
    Main scraping function - real-time search

    Args:
        search_query: What to search for (e.g., "iphone", "laptop")
        max_pages: How many pages of results to scrape

    Returns:
        List of listing dictionaries
    """
    logger.info(f"Starting TradeMe web scraper for query: '{search_query}'...")
    all_listings = []

    async with TradeGeMeScraper(headless=True) as scraper:
        try:
            await scraper.init_browser()

            if search_query.strip():
                # Search for specific query
                logger.info(f"Searching for: '{search_query}'")
                listings = await scraper.search_listings(
                    search_query=search_query,
                    max_pages=max_pages
                )
                all_listings.extend(listings)
            else:
                # No query - scrape featured/popular listings
                logger.info("No search query - scraping featured listings...")
                featured = await scraper.scrape_featured_listings()
                all_listings.extend(featured)

            # Remove duplicates based on listing ID
            unique_listings = {}
            for listing in all_listings:
                listing_id = listing.get('id', '')
                if listing_id and listing_id not in unique_listings:
                    unique_listings[listing_id] = listing

            all_listings = list(unique_listings.values())
            logger.info(f"Total unique listings collected: {len(all_listings)}")

        except Exception as e:
            logger.error(f"Scraping error: {e}")
            raise

    return all_listings


def save_listings_json(listings: List[Dict], output_file: str = "listings.json"):
    """Save listings to JSON file"""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        'timestamp': datetime.now().isoformat(),
        'total_count': len(listings),
        'listings': listings
    }

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

    logger.info(f"Saved {len(listings)} listings to {output_path}")
    return output_path


def save_listings_json(listings: List[Dict], output_file: str = "listings.json"):
    """Save listings to JSON file"""
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        'timestamp': datetime.now().isoformat(),
        'total_count': len(listings),
        'listings': listings
    }

    with open(output_path, 'w') as f:
        json.dump(data, f, indent=2)

    logger.info(f"Saved {len(listings)} listings to {output_path}")
    return output_path


def serve_http_server():
    """Start HTTP server for on-demand scraping"""
    try:
        from flask import Flask, request, jsonify
    except ImportError:
        logger.error("Flask not installed. Run: pip install flask")
        return

    app = Flask(__name__)

    @app.route('/search', methods=['GET', 'POST'])
    def search():
        """
        Search endpoint
        Usage: POST /search?q=iphone&pages=2
        or: POST /search with JSON body {"query": "iphone", "pages": 2}
        """
        try:
            # Get parameters
            if request.method == 'POST' and request.is_json:
                data = request.get_json()
                query = data.get('query', '')
                max_pages = data.get('pages', 2)
            else:
                query = request.args.get('q', '')
                max_pages = int(request.args.get('pages', 2))

            logger.info(f"HTTP search request: query='{query}', pages={max_pages}")

            # Run scraper
            listings = asyncio.run(scrape_trademe(query, max_pages))

            return jsonify({
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'query': query,
                'total_count': len(listings),
                'listings': listings
            })

        except Exception as e:
            logger.error(f"Search error: {e}")
            return jsonify({
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }), 500

    @app.route('/health', methods=['GET'])
    def health():
        """Health check endpoint"""
        return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})

    @app.route('/', methods=['GET'])
    def index():
        """API documentation"""
        return jsonify({
            'name': 'TradeMe Web Scraper API',
            'endpoints': {
                'GET /health': 'Health check',
                'POST /search?q=query&pages=2': 'Search by query',
                'POST /search (JSON body)': 'Search with JSON body'
            },
            'example': {
                'url': 'http://localhost:5000/search?q=iphone&pages=2',
                'json_body': {
                    'query': 'iphone',
                    'pages': 2
                }
            }
        })

    logger.info("Starting HTTP server on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)


async def main():
    """Main entry point - handles CLI and direct execution"""
    parser = argparse.ArgumentParser(description='TradeMe Web Scraper')
    parser.add_argument('--query', '-q', default='', help='Search query')
    parser.add_argument('--pages', '-p', type=int, default=2, help='Number of pages to scrape')
    parser.add_argument('--output', '-o', default='listings.json', help='Output JSON file')
    parser.add_argument('--server', '-s', action='store_true', help='Start HTTP server')

    args = parser.parse_args()

    if args.server:
        # Start HTTP server for on-demand scraping
        serve_http_server()
    else:
        # Run scraper for query
        listings = await scrape_trademe(args.query, args.pages)
        save_listings_json(listings, args.output)
        logger.info("Web scraping completed successfully!")



if __name__ == "__main__":
    asyncio.run(main())

