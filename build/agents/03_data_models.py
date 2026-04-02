#!/usr/bin/env python3
"""Agent 3: Data Models - Core data structures"""
from pathlib import Path

def main():
    print("\n" + "="*70)
    print("Agent 3: Data Models".center(70))
    print("="*70 + "\n")

    content = '''package com.trademe.models

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class ListingModel(
    val id: Long,
    val title: String,
    val price: Double,
    val imageUrl: String? = null,
    val category: String? = null,
    val region: String? = null,
    val isFavorite: Boolean = false
)

@Serializable
data class SearchFilter(
    val searchQuery: String,
    val categoryId: String? = null,
    val minPrice: Double? = null,
    val maxPrice: Double? = null,
    val sortBy: SortOption = SortOption.RELEVANCE,
    val pageSize: Int = 20,
    val pageNumber: Int = 1
)

enum class SortOption { RELEVANCE, PRICE_LOW_HIGH, PRICE_HIGH_LOW, NEWEST, ENDING_SOON }

@Serializable
data class SearchResultsModel(
    val listings: List<ListingModel>,
    val totalCount: Int,
    val pageNumber: Int,
    val pageSize: Int,
    val hasMoreResults: Boolean
)

@Serializable
data class FavoriteListing(
    val listingId: Long,
    val title: String,
    val price: Double,
    val imageUrl: String? = null,
    val savedDate: String
)
'''

    path = Path("shared/src/commonMain/kotlin/com/trademe/models/ListingModel.kt")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip())
    print(f"✓ Created: {path}")

    # Repository interface
    repo_content = '''package com.trademe.database

import com.trademe.models.ListingModel
import com.trademe.models.SearchFilter
import com.trademe.models.SearchResultsModel
import com.trademe.models.FavoriteListing

interface ListingRepository {
    suspend fun searchListings(filter: SearchFilter): Result<SearchResultsModel>
    suspend fun getListingDetails(id: Long): Result<ListingModel>
    suspend fun addFavorite(listing: ListingModel): Result<FavoriteListing>
    suspend fun removeFavorite(id: Long): Result<Unit>
    suspend fun getFavorites(): Result<List<FavoriteListing>>
    suspend fun isFavorite(id: Long): Result<Boolean>
}

interface LocalCache {
    suspend fun saveListing(listing: ListingModel)
    suspend fun getListing(id: Long): ListingModel?
    suspend fun getAllListings(): List<ListingModel>
    suspend fun clearCache()
}

class InMemoryCache : LocalCache {
    private val cache = mutableMapOf<Long, ListingModel>()

    override suspend fun saveListing(listing: ListingModel) {
        cache[listing.id] = listing
    }

    override suspend fun getListing(id: Long): ListingModel? = cache[id]
    override suspend fun getAllListings(): List<ListingModel> = cache.values.toList()
    override suspend fun clearCache() { cache.clear() }
}
'''

    path = Path("shared/src/commonMain/kotlin/com/trademe/database/Repository.kt")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(repo_content.strip())
    print(f"✓ Created: {path}")

    print("\n" + "="*70)
    print("✓ Data Models Setup Complete".center(70))
    print("="*70 + "\n")
    return 0

if __name__ == "__main__":
    exit(main())

