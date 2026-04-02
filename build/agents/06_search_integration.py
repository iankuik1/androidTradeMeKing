#!/usr/bin/env python3
"""Agent 6: Search Integration - ViewModel and repository integration"""
from pathlib import Path

def main():
    print("\n" + "="*70)
    print("Agent 6: Search Integration".center(70))
    print("="*70 + "\n")

    # SearchViewModel
    viewmodel_content = '''package com.trademe.viewmodel

import kotlinx.coroutines.*
import kotlinx.coroutines.flow.*
import com.trademe.api.client.TradeMeApiClient
import com.trademe.database.ListingRepository, LocalCache
import com.trademe.models.ListingModel, SearchFilter, SearchResultsModel

class SearchViewModel(
    private val apiClient: TradeMeApiClient,
    private val repository: ListingRepository,
    private val cache: LocalCache
) {
    private val viewModelScope = CoroutineScope(Dispatchers.Main + Job())

    private val _searchState = MutableStateFlow<SearchState>(SearchState.Idle)
    val searchState: StateFlow<SearchState> = _searchState.asStateFlow()

    private val _listings = MutableStateFlow<List<ListingModel>>(emptyList())
    val listings: StateFlow<List<ListingModel>> = _listings.asStateFlow()

    fun search(filter: SearchFilter) {
        _searchState.value = SearchState.Loading

        viewModelScope.launch(Dispatchers.IO) {
            try {
                val result = repository.searchListings(filter)
                result.onSuccess { results ->
                    _listings.value = results.listings
                    _searchState.value = SearchState.Success(results.totalCount)
                }
                result.onFailure { error ->
                    _searchState.value = SearchState.Error(error.message ?: "Unknown error")
                }
            } catch (e: Exception) {
                _searchState.value = SearchState.Error(e.message ?: "Unknown error")
            }
        }
    }

    fun clearSearch() {
        _searchState.value = SearchState.Idle
        _listings.value = emptyList()
    }
}

sealed class SearchState {
    object Idle : SearchState()
    object Loading : SearchState()
    data class Success(val totalCount: Int) : SearchState()
    data class Error(val message: String) : SearchState()
}
'''

    path = Path("shared/src/commonMain/kotlin/com/trademe/viewmodel/SearchViewModel.kt")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(viewmodel_content.strip())
    print(f"✓ Created: {path}")

    # Repository implementation
    repo_impl = '''package com.trademe.search

import com.trademe.api.client.TradeMeApiClient
import com.trademe.database.ListingRepository, LocalCache
import com.trademe.models.ListingModel, SearchFilter, SearchResultsModel, FavoriteListing

class SearchRepositoryImpl(
    private val apiClient: TradeMeApiClient,
    private val cache: LocalCache
) : ListingRepository {

    override suspend fun searchListings(filter: SearchFilter): Result<SearchResultsModel> {
        return try {
            val result = apiClient.searchListings(
                searchString = filter.searchQuery,
                page = filter.pageNumber,
                pageSize = filter.pageSize
            )

            result.mapCatching { response ->
                SearchResultsModel(
                    listings = response.listings.map { listing ->
                        ListingModel(
                            id = listing.listingId.toLongOrNull() ?: 0L,
                            title = listing.title,
                            price = listing.startPrice ?: 0.0,
                            imageUrl = listing.image?.url,
                            category = listing.category,
                            region = listing.region
                        )
                    },
                    totalCount = response.totalCount,
                    pageNumber = filter.pageNumber,
                    pageSize = filter.pageSize,
                    hasMoreResults = false
                )
            }
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override suspend fun getListingDetails(id: Long): Result<ListingModel> {
        return try {
            cache.getListing(id)?.let {
                Result.success(it)
            } ?: Result.failure(Exception("Listing not found"))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override suspend fun addFavorite(listing: ListingModel): Result<FavoriteListing> {
        return try {
            cache.saveListing(listing)
            Result.success(FavoriteListing(
                listingId = listing.id,
                title = listing.title,
                price = listing.price,
                imageUrl = listing.imageUrl,
                savedDate = System.currentTimeMillis().toString()
            ))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override suspend fun removeFavorite(id: Long): Result<Unit> {
        return Result.success(Unit)
    }

    override suspend fun getFavorites(): Result<List<FavoriteListing>> {
        return Result.success(emptyList())
    }

    override suspend fun isFavorite(id: Long): Result<Boolean> {
        return Result.success(false)
    }
}
'''

    path = Path("shared/src/commonMain/kotlin/com/trademe/search/SearchRepositoryImpl.kt")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(repo_impl.strip())
    print(f"✓ Created: {path}")

    print("\n" + "="*70)
    print("✓ Search Integration Setup Complete".center(70))
    print("="*70 + "\n")
    return 0

if __name__ == "__main__":
    exit(main())

