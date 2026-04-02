#!/usr/bin/env python3
"""Agent 5: Search UI - Android Compose and iOS SwiftUI"""
from pathlib import Path

def main():
    print("\n" + "="*70)
    print("Agent 5: Search UI".center(70))
    print("="*70 + "\n")

    # Android Search Screen
    compose_content = '''package com.trademe.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import com.trademe.models.ListingModel

@Composable
fun SearchScreen(
    onSearch: (String) -> Unit = {},
    listings: List<ListingModel> = emptyList(),
    isLoading: Boolean = false
) {
    var searchQuery by remember { mutableStateOf("") }

    Column(modifier = Modifier.fillMaxSize()) {
        // Search bar
        TextField(
            value = searchQuery,
            onValueChange = { searchQuery = it },
            modifier = Modifier
                .fillMaxWidth()
                .padding(8.dp),
            placeholder = { Text("Search listings...") },
            singleLine = true
        )

        Button(
            onClick = { onSearch(searchQuery) },
            modifier = Modifier
                .fillMaxWidth()
                .padding(8.dp)
        ) {
            Text("Search")
        }

        // Results
        if (isLoading) {
            CircularProgressIndicator(modifier = Modifier.align(androidx.compose.ui.Alignment.CenterHorizontally))
        } else if (listings.isEmpty()) {
            Text("No listings found", modifier = Modifier.padding(16.dp))
        } else {
            LazyColumn(modifier = Modifier.fillMaxSize()) {
                items(listings.size) { index ->
                    ListingCard(listings[index])
                }
            }
        }
    }
}

@Composable
fun ListingCard(listing: ListingModel) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(8.dp),
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
    ) {
        Column(modifier = Modifier.padding(12.dp)) {
            Text(listing.title, style = MaterialTheme.typography.titleMedium)
            Text("${'$'}{listing.price}")
            listing.category?.let { Text("Category: $it") }
            listing.region?.let { Text("Region: $it") }
        }
    }
}
'''

    path = Path("androidApp/src/main/kotlin/com/trademe/ui/screens/SearchScreen.kt")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(compose_content.strip())
    print(f"✓ Created Android SearchScreen: {path}")

    # iOS SwiftUI
    swiftui_content = '''import SwiftUI

struct SearchView: View {
    @State private var searchText = ""
    @State private var listings: [ListingModel] = []
    @State private var isLoading = false

    var body: some View {
        NavigationView {
            VStack {
                HStack {
                    TextField("Search...", text: $searchText)
                        .textFieldStyle(RoundedBorderTextFieldStyle())

                    Button(action: performSearch) {
                        Image(systemName: "magnifyingglass")
                    }
                }
                .padding()

                if isLoading {
                    ProgressView()
                } else if listings.isEmpty {
                    Text("No listings found")
                        .foregroundColor(.gray)
                } else {
                    List(listings, id: \\.id) { listing in
                        ListingRowView(listing: listing)
                    }
                }
            }
            .navigationTitle("Search")
        }
    }

    private func performSearch() {
        isLoading = true
        // Search triggered
    }
}

struct ListingRowView: View {
    let listing: ListingModel

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(listing.title)
                .font(.headline)
            Text(String(format: "$%.2f", listing.price))
                .foregroundColor(.blue)
            if let category = listing.category {
                Text(category)
                    .font(.caption)
            }
        }
        .padding()
    }
}

struct ListingModel: Identifiable {
    let id: Int
    let title: String
    let price: Double
    let category: String?
}

#Preview {
    SearchView()
}
'''

    path = Path("iosApp/TradeMe/Views/SearchView.swift")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(swiftui_content.strip())
    print(f"✓ Created iOS SearchView: {path}")

    print("\n" + "="*70)
    print("✓ Search UI Setup Complete".center(70))
    print("="*70 + "\n")
    return 0

if __name__ == "__main__":
    exit(main())

