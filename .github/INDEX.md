# 🤖 TradeMe Agent Workflows - Complete Guide

Welcome! This directory contains automated agent workflows that build a complete Kotlin Multiplatform TradeMe application.

## 📖 Documentation Map

### 🚀 **Start Here**
- **[QUICK_START.md](QUICK_START.md)** - Quick visual guide to all workflows
  - How to run workflows
  - What each workflow creates
  - Requirements and troubleshooting

### 📋 **Detailed Information**
- **[WORKFLOWS_SUMMARY.md](WORKFLOWS_SUMMARY.md)** - Complete summary of all workflows
  - Feature breakdown
  - Code structure details
  - Configuration requirements

### 🔧 **Technical Reference**
- **[workflows/README.md](workflows/README.md)** - In-depth workflow documentation
  - Detailed workflow descriptions
  - Project structure explained
  - Development workflow guide

### 📁 **Agent Definitions**
- **[agents/](agents/)** - Agent specifications (read-only)
  - `kmp_setup_agent.json`
  - `trademe_api_agent.json`
  - `data_models_agent.json`
  - `image_loading_agent.json`
  - `search_ui_agent.json`
  - `search_integration_agent.json`

---

## 🎯 Quick Navigation

### I want to...

#### ▶️ **Run all workflows at once**
→ Go to [QUICK_START.md](QUICK_START.md) → "Run All (Recommended for first time)"

#### ▶️ **Run individual workflows**
→ Go to [QUICK_START.md](QUICK_START.md) → "Run Individual Workflows"

#### ▶️ **Understand what workflows create**
→ Go to [QUICK_START.md](QUICK_START.md) → "What Gets Created"

#### ▶️ **Get detailed technical info**
→ Go to [workflows/README.md](workflows/README.md) → "Workflow Execution"

#### ▶️ **See all features implemented**
→ Go to [WORKFLOWS_SUMMARY.md](WORKFLOWS_SUMMARY.md) → "Key Features Implemented"

#### ▶️ **Troubleshoot issues**
→ Go to [QUICK_START.md](QUICK_START.md) → "Troubleshooting"

---

## 📦 What You Get

### 7 Complete Workflows

| # | Workflow | Purpose | Time |
|---|----------|---------|------|
| 1️⃣ | KMP Setup | Initialize project | ~2 min |
| 2️⃣ | API Client | OAuth & API integration | ~3 min |
| 3️⃣ | Data Models | Core data structures | ~3 min |
| 4️⃣ | Image Loading | Caching system | ~3 min |
| 5️⃣ | Search UI | Android & iOS UI | ~4 min |
| 6️⃣ | Search Integration | Connect layers | ~3 min |
| 7️⃣ | Orchestration | Run all together | ~15-20 min |

### 📱 Platform Support
- ✅ **Android** - Jetpack Compose UI
- ✅ **iOS** - SwiftUI UI
- ✅ **Shared** - Kotlin Multiplatform common code

### 🎁 Included Features
- ✅ OAuth2 Authentication
- ✅ Full-text Search
- ✅ Image Caching (Memory & Disk)
- ✅ Data Models & Repository Pattern
- ✅ State Management (ViewModel, StateFlow)
- ✅ Error Handling
- ✅ Pagination Support
- ✅ Favorites Management

---

## 🚀 Getting Started (60 seconds)

### Step 1: View Available Workflows
```bash
# See all workflows
gh workflow list
```

### Step 2: Run Orchestration (Recommended)
```bash
# Run all workflows in order
gh workflow run agent-orchestration.yml
```

### Step 3: Monitor Progress
- Go to GitHub Actions tab
- Watch workflows execute
- See generated PRs with code

### Step 4: Review & Merge
- Check generated pull requests
- Review automated code
- Merge to your repository

**Done!** Your TradeMe app is built! 🎉

---

## 📂 Project Structure (After Running)

```
androidTradeMeKing/
├── .github/
│   ├── agents/                  # Agent definitions (read-only)
│   ├── workflows/               # Workflow automations (this folder)
│   ├── QUICK_START.md          # ← Start here
│   ├── WORKFLOWS_SUMMARY.md     # Detailed summary
│   └── INDEX.md                 # ← You are here
├── shared/                      # Kotlin Multiplatform shared code
│   └── src/commonMain/kotlin/com/trademe/
│       ├── api/                 # API client
│       ├── models/              # Data models
│       ├── database/            # Cache & repository
│       ├── image/               # Image loading
│       ├── search/              # Search logic
│       └── viewmodel/           # State management
├── androidApp/                  # Android application
│   └── src/main/kotlin/com/trademe/
│       ├── ui/                  # Compose UI
│       └── viewmodel/           # Android ViewModels
└── iosApp/                      # iOS application
    └── TradeMe/Views/           # SwiftUI code
```

---

## 🎓 Learning by Example

Each workflow demonstrates important concepts:

1. **KMP Setup** - Project structure & Gradle configuration
2. **API Client** - OAuth2 authentication & HTTP clients
3. **Data Models** - Kotlin data classes & serialization
4. **Image Loading** - Caching strategies & memory management
5. **Search UI** - Compose and SwiftUI best practices
6. **Search Integration** - Repository pattern & state management
7. **Orchestration** - CI/CD workflow automation

---

## ⚙️ Requirements

Before running workflows, you need:
- ✅ Git
- ✅ Java 17+ (JDK)
- ✅ Gradle (included in project)
- ✅ GitHub Actions enabled
- ⚡ Optional: OAuth credentials (for real API testing)

See [QUICK_START.md](QUICK_START.md) → "Requirements" for details.

---

## 🔗 Quick Links

| Document | Purpose |
|----------|---------|
| [QUICK_START.md](QUICK_START.md) | 📍 Start here - visual guide |
| [WORKFLOWS_SUMMARY.md](WORKFLOWS_SUMMARY.md) | 📋 Detailed feature summary |
| [workflows/README.md](workflows/README.md) | 📖 Technical reference |
| [workflows/kmp-setup.yml](workflows/kmp-setup.yml) | Project initialization |
| [workflows/trademe-api-client.yml](workflows/trademe-api-client.yml) | API client setup |
| [workflows/data-models.yml](workflows/data-models.yml) | Data structures |
| [workflows/image-loading.yml](workflows/image-loading.yml) | Image caching |
| [workflows/search-ui.yml](workflows/search-ui.yml) | UI implementation |
| [workflows/search-integration.yml](workflows/search-integration.yml) | Integration layer |
| [workflows/agent-orchestration.yml](workflows/agent-orchestration.yml) | Run all workflows |

---

## 💡 Pro Tips

- **First time?** → Read [QUICK_START.md](QUICK_START.md)
- **Need details?** → Read [WORKFLOWS_SUMMARY.md](WORKFLOWS_SUMMARY.md)
- **Deep dive?** → Read [workflows/README.md](workflows/README.md)
- **Need help?** → Check troubleshooting sections
- **Want to learn?** → Follow the learning path in QUICK_START.md

---

## 🎯 Common Tasks

### Run all workflows
[→ See QUICK_START.md](QUICK_START.md#-how-to-run)

### Understand what each workflow does
[→ See WORKFLOWS_SUMMARY.md](WORKFLOWS_SUMMARY.md#-what-each-workflow-does)

### See the project structure
[→ See QUICK_START.md](QUICK_START.md#-what-gets-created)

### Troubleshoot issues
[→ See QUICK_START.md](QUICK_START.md#-troubleshooting)

### Learn Kotlin Multiplatform
[→ See workflows/README.md](workflows/README.md#documentation)

---

## ✨ Status

- ✅ All 7 workflows created
- ✅ Complete documentation written
- ✅ Ready to run immediately
- ✅ No additional setup needed
- ⏭️ Next: Run orchestration workflow!

---

## 📞 Need Help?

1. **Quick questions?** → [QUICK_START.md](QUICK_START.md#-troubleshooting)
2. **Feature details?** → [WORKFLOWS_SUMMARY.md](WORKFLOWS_SUMMARY.md)
3. **Technical info?** → [workflows/README.md](workflows/README.md)
4. **Code structure?** → Check generated files in pull requests

---

## 🎉 Ready?

### Start Here:
1. Open [QUICK_START.md](QUICK_START.md)
2. Follow "How to Run" section
3. Choose "Run All (Recommended)"
4. Watch workflows execute
5. Review generated code

**Your TradeMe app builds itself!** 🤖

---

## 🤖 Web Scraper Implementation

**NEW**: Instead of using the TradeMe API with OAuth, we now have a **web scraper approach**!

### What Changed

- ❌ **Removed**: OAuth2 authentication requirement
- ❌ **Removed**: API key management
- ✅ **Added**: Playwright web scraper (Workflow-based)
- ✅ **Added**: Automatic data collection every 6 hours
- ✅ **Added**: Works completely offline with bundled data

### Files Added

- **`.github/scraper/scraper.py`** - Main scraper code (Playwright + BeautifulSoup)
- **`.github/scraper/requirements.txt`** - Python dependencies
- **`.github/workflows/web-scraper.yml`** - Scraper workflow (runs every 6 hours)
- **`.github/WEBSCRAPER_GUIDE.md`** - Complete web scraper documentation

### Quick Start

1. Read: [WEBSCRAPER_GUIDE.md](WEBSCRAPER_GUIDE.md)
2. Run: `gh workflow run web-scraper.yml`
3. Wait: ~5 minutes for initial scrape
4. Check: `listings.json` in repo root
5. Integrate: Use in SearchRepositoryImpl

### Key Features

✅ **No OAuth/API Keys** - Zero authentication needed  
✅ **Automated Updates** - Runs every 6 hours via GitHub Actions  
✅ **Works Offline** - Bundle with app for offline search  
✅ **Legal Friendly** - Includes proper delays and user-agent  
✅ **Easy Integration** - ScraperDataClient for Kotlin code  
✅ **Scalable** - Store in GitHub releases or artifacts  

### Data Flow

```
Web Scraper Workflow → listings.json → GitHub Releases
                          ↓
                    Mobile App
                    (fetches & caches)
                          ↓
                    User sees listings
```

---

*Generated by Agent Workflows*  
*Last updated: April 2026*
