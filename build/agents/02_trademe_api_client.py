#!/usr/bin/env python3
"""
Agent 2: TradeMe Data Client - Real-Time Scraper
Creates RealTimeScraperClient and TradeMeApiClient for on-demand scraping
"""

from pathlib import Path

def create_listing_models():
    """Create listing data models"""
    content = '''package com.trademe.api.models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class ListingsResponse(
    @SerialName("listings")
    val listings: List<Listing> = emptyList(),
    @SerialName("total_count")
    val totalCount: Int = 0,
    @SerialName("timestamp")
    val timestamp: String? = null
)

@Serializable
data class Listing(
    @SerialName("id")
    val listingId: String,
    @SerialName("title")
    val title: String,
    @SerialName("priceDisplay")
    val priceDisplay: String,
    @SerialName("price")
    val startPrice: Double? = null,
    @SerialName("imageUrl")
    val image: ListingImage? = null,
    @SerialName("category")
    val category: String? = null,
    @SerialName("region")
    val region: String? = null,
    @SerialName("url")
    val url: String? = null,
    @SerialName("scraped_at")
    val scrapedAt: String? = null,
    @SerialName("source")
    val source: String? = "webscraper"
)

@Serializable
data class ListingImage(
    @SerialName("imageUrl")
    val url: String? = null
)
'''

    path = Path("shared/src/commonMain/kotlin/com/trademe/api/models/ListingModels.kt")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip())
    print(f"✓ Created: {path}")

def create_realtime_scraper_client():
    """Create RealTimeScraperClient"""
    content = '''package com.trademe.api.client

import io.ktor.client.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.request.*
import io.ktor.client.statement.*
import io.ktor.http.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.serialization.json.Json
import com.trademe.api.models.ListingsResponse

/**
 * Real-Time Web Scraper Client
 * Calls scraper API endpoint for on-demand scraping
 */
class RealTimeScraperClient(
    private val scraperUrl: String = "http://localhost:5000"
) {
    private val httpClient = HttpClient {
        install(ContentNegotiation) {
            json(Json {
                ignoreUnknownKeys = true
                isLenient = true
            })
        }
    }

    /**
     * Search listings - scrapes on each request
     */
    suspend fun searchListings(
        searchString: String = "",
        page: Int = 1,
        pageSize: Int = 20,
        categoryId: String? = null
    ): Result<ListingsResponse> {
        return try {
            if (searchString.isBlank()) {
                return Result.success(ListingsResponse(
                    listings = emptyList(),
                    totalCount = 0
                ))
            }

            val response = httpClient.get("$scraperUrl/search") {
                parameter("q", searchString)
                parameter("pages", 2)
                timeout {
                    requestTimeoutMillis = 60000
                }
            }

            if (response.status.isSuccess()) {
                val json = response.bodyAsText()
                val data = Json.decodeFromString<ScraperResponse>(json)

                Result.success(ListingsResponse(
                    listings = data.listings,
                    totalCount = data.totalCount
                ))
            } else {
                Result.failure(Exception("Scraper error: ${response.status}"))
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    fun close() {
        httpClient.close()
    }
}

@kotlinx.serialization.Serializable
internal data class ScraperResponse(
    @kotlinx.serialization.SerialName("success")
    val success: Boolean = true,
    @kotlinx.serialization.SerialName("query")
    val query: String = "",
    @kotlinx.serialization.SerialName("total_count")
    val totalCount: Int = 0,
    @kotlinx.serialization.SerialName("listings")
    val listings: List<com.trademe.api.models.Listing> = emptyList()
)
'''

    path = Path("shared/src/commonMain/kotlin/com/trademe/api/client/RealTimeScraperClient.kt")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip())
    print(f"✓ Created: {path}")

def create_trademe_api_client():
    """Create TradeMeApiClient (real-time edition)"""
    content = '''package com.trademe.api.client

import com.trademe.api.models.ListingsResponse

/**
 * TradeMeApiClient - Real-Time Web Scraper Edition
 * Scrapes listings on-demand for each search query
 */
class TradeMeApiClient(
    private val scraperClient: RealTimeScraperClient = RealTimeScraperClient()
) {
    /**
     * Search listings - calls scraper API on-demand
     */
    suspend fun searchListings(
        searchString: String,
        page: Int = 1,
        pageSize: Int = 20,
        categoryId: String? = null
    ): Result<ListingsResponse> {
        return scraperClient.searchListings(
            searchString = searchString,
            page = page,
            pageSize = pageSize,
            categoryId = categoryId
        )
    }

    fun close() {
        scraperClient.close()
    }
}
'''

    path = Path("shared/src/commonMain/kotlin/com/trademe/api/client/TradeMeApiClient.kt")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip())
    print(f"✓ Created: {path}")

def main():
    print("\n" + "="*70)
    print("Agent 2: TradeMe Data Client (Real-Time Scraper)".center(70))
    print("="*70 + "\n")

    print("📋 Creating data models...")
    create_listing_models()

    print("\n🔗 Creating RealTimeScraperClient...")
    create_realtime_scraper_client()

    print("\n🔗 Creating TradeMeApiClient...")
    create_trademe_api_client()

    print("\n" + "="*70)
    print("✓ TradeMe Data Client Setup Complete".center(70))
    print("="*70 + "\n")

    return 0

if __name__ == "__main__":
    exit(main())

