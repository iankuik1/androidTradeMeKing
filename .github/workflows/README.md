# TradeMe Agent Workflows

This directory contains GitHub Actions workflows that automate the development of a Kotlin Multiplatform TradeMe application using specialized agents.

## Overview

The TradeMe application is built using a series of automated agent workflows that handle different aspects of the development process. Each workflow corresponds to a specialized agent defined in `.github/agents/`.

## Agent Workflows

### 1. **KMP Project Setup** (`kmp-setup.yml`)
- **Agent**: `KMPProjectSetupAgent`
- **Purpose**: Initialize Kotlin Multiplatform project structure
- **Creates**:
  - Shared module for common code
  - Android and iOS platform modules
  - Gradle build configuration
  - Module structure with proper source sets

### 2. **TradeMe API Client** (`trademe-api-client.yml`)
- **Agent**: `TradeMeAPIClientAgent`
- **Purpose**: Implement API client for TradeMe service
- **Implements**:
  - OAuth2 authentication handler
  - API models (Listing, AuthResponse)
  - Ktor-based HTTP client
  - Search endpoints integration

### 3. **Data Models** (`data-models.yml`)
- **Agent**: `DataModelsAgent`
- **Purpose**: Define core data structures
- **Includes**:
  - ListingModel: Main listing data structure
  - SearchFilter: Advanced filtering options
  - SearchResultsModel: Paginated results
  - FavoriteListing: User favorites tracking
  - Repository pattern for data access
  - LocalCache interface for offline support

### 4. **Image Loading** (`image-loading.yml`)
- **Agent**: `ImageLoadingAgent`
- **Purpose**: Implement image loading and caching
- **Features**:
  - InMemoryImageCache: LRU cache with size limits
  - AndroidDiskImageCache: Persistent disk caching
  - ImageLoader: Network image fetching
  - Automatic cache eviction
  - Image prefetching support

### 5. **Search UI** (`search-ui.yml`)
- **Agent**: `SearchUIAgent`
- **Purpose**: Build platform-specific UI components
- **Android (Compose)**:
  - SearchScreen with input and filters
  - ListingCard component
  - SearchFilterChips for options
  - Material Design 3 styling
- **iOS (SwiftUI)**:
  - SearchView native interface
  - ListingRowView for listings
  - Async image loading
  - Native iOS styling

### 6. **Search Integration** (`search-integration.yml`)
- **Agent**: `SearchIntegrationAgent`
- **Purpose**: Connect UI to data layer
- **Implements**:
  - SearchViewModel: State management
  - SearchRepositoryImpl: Repository pattern
  - SearchUseCase: Business logic
  - AndroidSearchViewModel: Android adapter
  - Pagination support
  - Favorites management

## Workflow Execution

### Manual Execution

Trigger individual workflows through GitHub Actions UI:

1. Go to your repository's **Actions** tab
2. Select the desired workflow
3. Click **Run workflow**

### Automated Orchestration

Run all workflows in sequence:

```bash
# Trigger the orchestration workflow
gh workflow run agent-orchestration.yml
```

This will execute all agents in the correct dependency order.

## Project Structure

After all workflows complete, your project structure will be:

```
androidTradeMeKing/
├── .github/
│   ├── agents/              # Agent definitions
│   │   ├── kmp_setup_agent.json
│   │   ├── trademe_api_agent.json
│   │   ├── data_models_agent.json
│   │   ├── image_loading_agent.json
│   │   ├── search_ui_agent.json
│   │   └── search_integration_agent.json
│   └── workflows/           # Workflow automations
│       ├── kmp-setup.yml
│       ├── trademe-api-client.yml
│       ├── data-models.yml
│       ├── image-loading.yml
│       ├── search-ui.yml
│       ├── search-integration.yml
│       └── agent-orchestration.yml
├── shared/                  # Kotlin Multiplatform shared module
│   ├── src/
│   │   ├── commonMain/
│   │   │   └── kotlin/com/trademe/
│   │   │       ├── api/              # API client
│   │   │       │   ├── auth/         # Authentication
│   │   │       │   ├── models/       # API models
│   │   │       │   └── client/       # HTTP client
│   │   │       ├── models/           # Data models
│   │   │       ├── database/         # Cache and repository
│   │   │       ├── image/            # Image loading
│   │   │       ├── search/           # Search logic
│   │   │       └── viewmodel/        # State management
│   │   ├── androidMain/              # Android-specific code
│   │   └── iosMain/                  # iOS-specific code
│   └── build.gradle.kts
├── androidApp/              # Android application
│   ├── src/main/
│   │   ├── kotlin/com/trademe/
│   │   │   ├── ui/
│   │   │   │   ├── screens/          # UI screens
│   │   │   │   └── components/       # Reusable components
│   │   │   └── viewmodel/            # Android ViewModels
│   │   └── res/                      # Resources (strings, colors, etc)
│   └── build.gradle.kts
└── iosApp/                  # iOS application
    ├── TradeMe/
    │   └── Views/                    # SwiftUI views
    └── build.gradle.kts
```

## Key Features

### 🔐 Authentication
- OAuth2 authentication with TradeMe API
- Token refresh mechanism
- Secure credential storage

### 🔍 Search Functionality
- Full-text search capabilities
- Advanced filtering (price, category, region)
- Sort options (relevance, price, date)
- Pagination support

### 📱 Multi-Platform UI
- Android: Jetpack Compose
- iOS: SwiftUI
- Shared code for business logic
- Platform-specific optimizations

### 📦 Data Management
- In-memory caching with LRU eviction
- Persistent disk caching (Android)
- Repository pattern
- Offline browsing support

### 🖼️ Image Handling
- Lazy loading with cache
- LRU memory cache with size limits
- Disk cache with expiration (Android)
- Automatic prefetching

### 📊 State Management
- Reactive state with StateFlow
- Coroutine-based async operations
- Error handling and recovery
- Loading states

## Dependencies

The workflows will configure these key dependencies:

### Kotlin Multiplatform
- Kotlin: 1.9.20+
- Gradle: Latest

### Shared Module
- Ktor Client: 2.3.0
- Kotlin Serialization: 1.9.20

### Android
- Jetpack Compose: Latest
- Coil (Image loading): Latest
- androidx.lifecycle: Latest

### iOS
- SwiftUI: iOS 14+
- Async/Await support

## Configuration

### OAuth Credentials

Before running the application, configure OAuth credentials:

1. Register with TradeMe Developer API
2. Get OAuth Client ID and Secret
3. Set environment variables:
   ```bash
   export TRADEME_CLIENT_ID=your_client_id
   export TRADEME_CLIENT_SECRET=your_client_secret
   ```

### Gradle Properties

Create `local.properties`:
```properties
sdk.dir=/path/to/android/sdk
```

## Running Workflows

### Via GitHub CLI

```bash
# List available workflows
gh workflow list

# Run a specific workflow
gh workflow run kmp-setup.yml

# Run orchestration (all agents)
gh workflow run agent-orchestration.yml
```

### Via GitHub Web UI

1. Navigate to **Actions** tab
2. Select workflow
3. Click **Run workflow**
4. Monitor execution in real-time

## Monitoring Workflow Progress

Each workflow generates:
- Console output in GitHub Actions
- Pull requests with implementation details
- Artifacts (build summaries, generated files)

## Troubleshooting

### Workflow Failures

1. Check GitHub Actions logs
2. Verify Java and Gradle installation
3. Check API credentials
4. Review build output artifacts

### Build Issues

```bash
# Clean build
./gradlew clean

# Build shared module
./gradlew :shared:build

# Build Android app
./gradlew :androidApp:build
```

### Common Issues

| Issue | Solution |
|-------|----------|
| Java version mismatch | Use JDK 17+ |
| Gradle sync failure | Run `./gradlew --refresh-dependencies` |
| API auth failure | Verify OAuth credentials |
| Compose build error | Update Kotlin version |

## Next Steps

After agents complete:

1. **Test**: Run unit and integration tests
2. **Customize**: Modify UI and business logic as needed
3. **API Integration**: Complete OAuth setup
4. **Deploy**: Build and deploy to App Stores
5. **Monitor**: Set up analytics and error tracking

## Development Workflow

### Adding Features

1. Create new feature workflow in `.github/workflows/`
2. Define corresponding agent in `.github/agents/`
3. Trigger workflow through GitHub Actions
4. Review generated code and PR

### Local Development

```bash
# Setup local environment
export JAVA_HOME=/path/to/jdk17

# Build all modules
./gradlew build

# Build for Android
./gradlew :androidApp:build

# Build shared module
./gradlew :shared:build

# Run tests
./gradlew test
```

## Documentation

- [Kotlin Multiplatform](https://kotlinlang.org/docs/multiplatform.html)
- [TradeMe API](https://developer.trademe.co.nz)
- [Jetpack Compose](https://developer.android.com/jetpack/compose)
- [SwiftUI](https://developer.apple.com/swiftui/)

## Support

For issues or questions:
1. Check workflow logs in GitHub Actions
2. Review generated code comments
3. Check GitHub Issues
4. Review documentation links above

## License

[Add your license here]

---

**Generated by Agent Workflows** - Automated development automation system

