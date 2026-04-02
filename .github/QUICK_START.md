# Agent Workflows Quick Start Guide

## 📍 Location

All workflows are in: `.github/workflows/`

## 🎯 Available Workflows

### 1️⃣ **KMP Project Setup**
**File**: `kmp-setup.yml`  
**Trigger**: Manually or on push to main  
**Time**: ~2 minutes

```
Creates: Kotlin Multiplatform project structure
├── shared/ (common code)
├── androidApp/ (Android UI)
└── iosApp/ (iOS UI)
```

---

### 2️⃣ **TradeMe API Client**
**File**: `trademe-api-client.yml`  
**Depends on**: KMP Setup  
**Time**: ~3 minutes

```
Implements: API client with OAuth2
├── Authentication (OAuth)
├── API Models (Listing, Response)
├── HTTP Client (Ktor)
└── Search Endpoints
```

---

### 3️⃣ **Data Models**
**File**: `data-models.yml`  
**Depends on**: KMP Setup  
**Time**: ~3 minutes

```
Defines: Core data structures
├── ListingModel
├── SearchFilter
├── SearchResultsModel
├── FavoriteListing
├── Repository Interface
└── Local Cache
```

---

### 4️⃣ **Image Loading**
**File**: `image-loading.yml`  
**Depends on**: Data Models & API Client  
**Time**: ~3 minutes

```
Implements: Image caching system
├── InMemoryImageCache (LRU)
├── AndroidDiskImageCache (persistent)
├── ImageLoader interface
└── Prefetching support
```

---

### 5️⃣ **Search UI**
**File**: `search-ui.yml`  
**Depends on**: Image Loading  
**Time**: ~4 minutes

```
Builds: Platform-specific UIs
├── Android (Compose)
│   ├── SearchScreen
│   ├── ListingCard
│   └── SearchFilterChips
└── iOS (SwiftUI)
    ├── SearchView
    └── ListingRowView
```

---

### 6️⃣ **Search Integration**
**File**: `search-integration.yml`  
**Depends on**: All above  
**Time**: ~3 minutes

```
Connects: UI to data layer
├── SearchViewModel
├── SearchRepositoryImpl
├── SearchUseCase
├── Pagination
└── Favorites management
```

---

### 7️⃣ **Orchestration (Run All)**
**File**: `agent-orchestration.yml`  
**Depends on**: Nothing (triggers others)  
**Time**: ~15-20 minutes total

```
Executes all workflows in order:
1. KMP Setup
   ├── 2. API Client
   ├── 3. Data Models
   │   └── 4. Image Loading
   │       └── 5. Search UI
   │           └── 6. Search Integration
   └── 7. Complete
```

---

## 🚀 How to Run

### Option A: Run All (Recommended for first time)

```bash
# Via GitHub CLI
gh workflow run agent-orchestration.yml

# Via GitHub Web
1. Go to Actions tab
2. Select "Agent Orchestration - Build Complete TradeMe App"
3. Click "Run workflow"
```

### Option B: Run Individual Workflows

```bash
# Setup KMP first
gh workflow run kmp-setup.yml

# Then others (they depend on KMP)
gh workflow run trademe-api-client.yml
gh workflow run data-models.yml
gh workflow run image-loading.yml
gh workflow run search-ui.yml
gh workflow run search-integration.yml
```

---

## 📊 What Gets Created

### Shared Module (Kotlin Multiplatform)
```kotlin
com/trademe/
├── api/
│   ├── auth/AuthManager.kt          // OAuth handling
│   ├── models/                      // ListingsResponse, Listing
│   └── client/TradeMeApiClient.kt   // API client
├── models/
│   ├── ListingModel.kt              // Core data model
│   ├── SearchFilter.kt              // Filter options
│   └── ...other models
├── database/
│   ├── LocalCache.kt                // Cache interface
│   └── InMemoryCache.kt             // Implementation
├── image/
│   ├── ImageLoader.kt               // Image loading
│   └── cache/InMemoryImageCache.kt  // Image cache
├── search/
│   ├── SearchRepositoryImpl.kt       // Repository pattern
│   └── SearchUseCase.kt             // Business logic
└── viewmodel/
    └── SearchViewModel.kt           // State management
```

### Android App (Jetpack Compose)
```kotlin
com/trademe/
├── ui/
│   ├── screens/SearchScreen.kt      // Main search screen
│   └── components/
│       ├── ListingCard.kt           // Listing display
│       └── SearchFilterChips.kt     // Filters
└── viewmodel/
    └── AndroidSearchViewModel.kt    // Android wrapper
```

### iOS App (SwiftUI)
```swift
TradeMe/
└── Views/
    └── SearchView.swift             // iOS search UI
```

---

## ✅ Verification

After workflows complete, check:

1. **GitHub Actions Tab**
   - ✅ All workflows show green checkmarks
   - ✅ No failures or errors
   - ✅ View logs for details

2. **Pull Requests**
   - ✅ 6 new PRs created (one per agent)
   - ✅ Code review the changes
   - ✅ Merge to apply code

3. **Project Structure**
   - ✅ `shared/` folder created with code
   - ✅ `androidApp/` has Compose UI
   - ✅ `iosApp/` has SwiftUI code
   - ✅ All gradle files configured

4. **Code Quality**
   - ✅ Proper package structure
   - ✅ Comprehensive comments
   - ✅ Design patterns used
   - ✅ Error handling included

---

## ⚙️ Requirements

Before running workflows:

### ✅ Git
```bash
git --version  # Should be installed
```

### ✅ Java
```bash
java -version  # JDK 17+
```

### ✅ Gradle
```bash
./gradlew --version  # Should work
```

### ✅ GitHub Token
- Workflows need write access
- Usually automatic with GitHub Actions

### ✅ Optional: OAuth Credentials
- For real API testing
- Not needed for initial setup
- Set later: `TRADEME_CLIENT_ID`, `TRADEME_CLIENT_SECRET`

---

## 🔧 Troubleshooting

### Workflow Won't Start
- ✅ Check GitHub token permissions
- ✅ Verify branch is `main`
- ✅ Check Actions tab is enabled

### Build Fails
- ✅ Check Java version (need 17+)
- ✅ Try `./gradlew clean`
- ✅ View detailed logs in Actions

### Code Generation Issues
- ✅ Check branch is up to date
- ✅ Verify file permissions
- ✅ Check available disk space

---

## 📚 Documentation

| File | Purpose |
|------|---------|
| `.github/workflows/README.md` | Detailed workflow docs |
| `.github/WORKFLOWS_SUMMARY.md` | This summary |
| Individual workflow files | Comments & step details |

---

## 🎓 Learning Path

1. **Start with**: `kmp-setup.yml` (understand project structure)
2. **Then**: `trademe-api-client.yml` (learn API integration)
3. **Next**: `data-models.yml` (see data structure design)
4. **Then**: `image-loading.yml` (understand caching)
5. **Next**: `search-ui.yml` (see UI implementation)
6. **Finally**: `search-integration.yml` (complete integration)

---

## 🎯 Next Steps

After workflows complete:

1. **Review Generated Code**
   - Read generated Kotlin files
   - Check Compose UI components
   - Review API client implementation

2. **Merge Pull Requests**
   - Each workflow creates a PR
   - Review changes
   - Merge to apply code

3. **Configure OAuth**
   - Register with TradeMe API
   - Set environment variables
   - Test API connectivity

4. **Customize**
   - Modify UI as needed
   - Add more features
   - Extend models

5. **Test & Deploy**
   - Run unit tests
   - Build APK/AAB
   - Deploy to stores

---

## 💡 Pro Tips

### 💻 Local Testing
```bash
# After workflows complete, test locally
./gradlew :shared:build        # Build shared module
./gradlew :androidApp:build    # Build Android app
```

### 📱 Android Studio
```bash
# Import project into Android Studio
# File → Open → Select project root
# Gradle will sync automatically
```

### 🔄 Re-run Workflows
```bash
# If something fails, re-run from GitHub Actions UI
# Workflows are idempotent (safe to re-run)
```

### 🐛 Debug
```bash
# Check workflow logs for detailed output
# Actions tab → Select workflow → See logs
```

---

## 📞 Support

For issues:
1. Check workflow logs (Actions tab)
2. Review README files
3. Check code comments
4. Review GitHub Issues

---

**You're all set!** 🚀  
Run the orchestration workflow or individual workflows to build your TradeMe app.

