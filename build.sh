#!/bin/bash
# Simple build script to run all agents sequentially

echo "🚀 Starting TradeMe Local Build Process"
echo "========================================"

cd "$(dirname "$0")"

# Function to run an agent
run_agent() {
    local agent_name="$1"
    local agent_script="$2"
    local description="$3"

    echo ""
    echo "▶️  Running: $agent_name"
    echo "   $description"
    echo "   Script: $agent_script"

    if [ -f "build/agents/$agent_script" ]; then
        python3 "build/agents/$agent_script"
        if [ $? -eq 0 ]; then
            echo "✅ $agent_name completed successfully"
        else
            echo "❌ $agent_name failed"
            exit 1
        fi
    else
        echo "❌ Agent script not found: build/agents/$agent_script"
        exit 1
    fi
}

# Run all agents in sequence
echo "📋 Build Plan:"
echo "1. KMP Project Setup"
echo "2. TradeMe API Client"
echo "3. Data Models"
echo "4. Image Loading"
echo "5. Search UI"
echo "6. Search Integration"
echo ""

run_agent "Agent 1: KMP Project Setup" "01_kmp_setup.py" "Creates project structure and Gradle files"
run_agent "Agent 2: TradeMe API Client" "02_trademe_api_client.py" "Real-time scraper client implementation"
run_agent "Agent 3: Data Models" "03_data_models.py" "Core data structures and repository pattern"
run_agent "Agent 4: Image Loading" "04_image_loading.py" "Image caching and loading system"
run_agent "Agent 5: Search UI" "05_search_ui.py" "Android Compose and iOS SwiftUI UI components"
run_agent "Agent 6: Search Integration" "06_search_integration.py" "ViewModel and repository integration"

echo ""
echo "🎉 BUILD COMPLETE!"
echo "=================="
echo ""
echo "Generated files:"
echo "- $(find shared androidApp iosApp -name "*.kt" -o -name "*.swift" 2>/dev/null | wc -l) Kotlin/Swift files"
echo ""
echo "Next steps:"
echo "1. Build with Gradle: ./gradlew build"
echo "2. Start scraper: python .github/scraper/scraper.py --server"
echo "3. Run app: ./gradlew :androidApp:run"
echo ""
echo "✅ Ready to test your TradeMe app!"
