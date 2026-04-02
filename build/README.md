# Local Build System - Agent-Based

This directory contains the local build agents for the TradeMe project. Instead of relying on GitHub Actions, all agents run locally as Python scripts.

## Quick Start

### Run All Agents
```bash
python build/orchestrator.py
```

### Run Specific Agent
```bash
# Agent 1: KMP Setup
python build/agents/01_kmp_setup.py

# Agent 2: TradeMe API Client
python build/agents/02_trademe_api_client.py

# Agent 3: Data Models
python build/agents/03_data_models.py

# Agent 4: Image Loading
python build/agents/04_image_loading.py

# Agent 5: Search UI
python build/agents/05_search_ui.py

# Agent 6: Search Integration
python build/agents/06_search_integration.py
```

### Verbose Output
```bash
python build/orchestrator.py --verbose
```

## Agent Descriptions

### 1. KMP Project Setup (`01_kmp_setup.py`)
**Time**: 2-3 minutes
**Creates**:
- Project directory structure
- Gradle build files (build.gradle.kts)
- Settings configuration
- Gradle wrapper

**Output**:
```
shared/src/commonMain/kotlin/com/trademe/
androidApp/src/main/kotlin/com/trademe/
iosApp/TradeMe/Views/
```

### 2. TradeMe API Client (`02_trademe_api_client.py`)
**Time**: 2-3 minutes
**Creates**:
- ListingModels.kt (data structures)
- RealTimeScraperClient.kt (calls scraper API)
- TradeMeApiClient.kt (main API client)

**Key Feature**: Real-time scraping on each search query

### 3. Data Models (`03_data_models.py`)
**Time**: 2-3 minutes
**Creates**:
- ListingModel.kt
- SearchFilter.kt
- SearchResultsModel.kt
- FavoriteListing.kt
- Repository interface
- InMemoryCache implementation

### 4. Image Loading (`04_image_loading.py`)
**Time**: 2-3 minutes
**Creates**:
- ImageCache interface
- InMemoryImageCache (LRU cache)
- ImageLoader interface
- DefaultImageLoader implementation

### 5. Search UI (`05_search_ui.py`)
**Time**: 3-4 minutes
**Creates**:
- **Android**: SearchScreen.kt (Compose), ListingCard.kt
- **iOS**: SearchView.swift (SwiftUI), ListingRowView.swift

### 6. Search Integration (`06_search_integration.py`)
**Time**: 2-3 minutes
**Creates**:
- SearchViewModel.kt (state management)
- SearchRepositoryImpl.kt (data layer)
- SearchState sealed class

## After Local Build

### 1. Build Project Locally
```bash
./gradlew clean build
./gradlew :shared:build
./gradlew :androidApp:build
```

### 2. Start Scraper Server
```bash
python .github/scraper/scraper.py --server
# Runs on http://localhost:5000
```

### 3. Run Application
```bash
# Android
./gradlew :androidApp:run

# Or open in Android Studio
# File → Open → Select project root
# Run with emulator/device
```

### 4. Test Search
- Launch the app
- Search for listings
- Watch real-time scraping happen!

## Project Structure After Build

```
androidTradeMeKing/
├── shared/
│   └── src/commonMain/kotlin/com/trademe/
│       ├── api/
│       │   ├── client/
│       │   │   ├── TradeMeApiClient.kt
│       │   │   └── RealTimeScraperClient.kt
│       │   └── models/
│       │       └── ListingModels.kt
│       ├── models/
│       │   └── ListingModel.kt
│       ├── database/
│       │   └── Repository.kt
│       ├── image/
│       │   └── ImageLoader.kt
│       ├── search/
│       │   └── SearchRepositoryImpl.kt
│       └── viewmodel/
│           └── SearchViewModel.kt
├── androidApp/
│   └── src/main/kotlin/com/trademe/
│       ├── ui/screens/SearchScreen.kt
│       └── viewmodel/...
└── iosApp/
    └── TradeMe/Views/SearchView.swift
```

## Key Features Implemented

✅ Real-time web scraping (no cached data)
✅ Ktor HTTP client integration
✅ Repository pattern for data access
✅ ViewModel with StateFlow
✅ Image caching system
✅ Android Compose UI
✅ iOS SwiftUI UI
✅ Kotlin Multiplatform architecture

## Troubleshooting

### Agent fails to run
```bash
# Check if Python is installed
python --version

# Run with verbose output
python build/orchestrator.py --verbose
```

### Missing directories
```bash
# Manually create if needed
mkdir -p shared/src/commonMain/kotlin/com/trademe
mkdir -p androidApp/src/main/kotlin/com/trademe
mkdir -p iosApp/TradeMe/Views
```

### Gradle build fails
```bash
# Ensure Java 17+ is installed
java -version

# Update Gradle
./gradlew --version
```

## Customization

Each agent script is standalone and can be modified:
- Change file paths
- Modify code generation
- Add more files
- Customize structure

## Benefits Over GitHub Actions

✅ **Local Control**: Run anytime, no GitHub API needed
✅ **Fast Iteration**: Test changes immediately
✅ **Offline**: Works without internet (except scraper)
✅ **Debugging**: Easy to debug and modify agents
✅ **No Logs to View**: Results visible immediately
✅ **Parallel Execution**: Can run multiple agents in parallel (future enhancement)

## Next Steps

1. Run `python build/orchestrator.py`
2. Wait for all agents to complete (~12-16 min)
3. Verify project structure was created
4. Build with Gradle
5. Start scraper server
6. Test the app!

---

**Local Build System Ready!** 🚀

All agents are set up and ready to build your TradeMe app locally.

