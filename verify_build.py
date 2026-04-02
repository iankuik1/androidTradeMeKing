#!/usr/bin/env python3
"""
Build Verification Script
Checks if the local build agents have successfully created the project
"""

import os
import sys
from pathlib import Path

def check_build_status():
    """Check the current build status"""
    print("🔍 TradeMe Build Verification")
    print("=" * 50)

    project_root = Path(".")
    issues = []

    # Check if build directory exists
    if not (project_root / "build").exists():
        issues.append("❌ build/ directory missing")
    else:
        print("✅ build/ directory exists")

        # Check orchestrator
        if (project_root / "build/orchestrator.py").exists():
            print("✅ Orchestrator script exists")
        else:
            issues.append("❌ orchestrator.py missing")

        # Check agents directory
        agents_dir = project_root / "build/agents"
        if agents_dir.exists():
            print("✅ build/agents/ directory exists")

            # Check all agent scripts
            expected_agents = [
                "01_kmp_setup.py",
                "02_trademe_api_client.py",
                "03_data_models.py",
                "04_image_loading.py",
                "05_search_ui.py",
                "06_search_integration.py"
            ]

            missing_agents = []
            for agent in expected_agents:
                if not (agents_dir / agent).exists():
                    missing_agents.append(agent)

            if missing_agents:
                issues.append(f"❌ Missing agents: {missing_agents}")
            else:
                print("✅ All 6 agent scripts exist")
        else:
            issues.append("❌ build/agents/ directory missing")

    # Check if project structure was created
    print("\n📁 Checking Generated Project Structure:")

    # Shared module
    shared_paths = [
        "shared/src/commonMain/kotlin/com/trademe",
        "shared/src/androidMain/kotlin/com/trademe",
        "shared/src/iosMain/kotlin/com/trademe"
    ]

    shared_created = 0
    for path in shared_paths:
        if (project_root / path).exists():
            shared_created += 1
            print(f"✅ {path}")
        else:
            print(f"❌ {path}")

    # Android app
    android_paths = [
        "androidApp/src/main/kotlin/com/trademe/ui/screens",
        "androidApp/src/main/kotlin/com/trademe/ui/components",
        "androidApp/src/main/kotlin/com/trademe/viewmodel"
    ]

    android_created = 0
    for path in android_paths:
        if (project_root / path).exists():
            android_created += 1
        else:
            print(f"❌ {path}")

    if android_created > 0:
        print(f"✅ Android directories: {android_created}/3 created")

    # iOS app
    ios_path = "iosApp/TradeMe/Views"
    if (project_root / ios_path).exists():
        print(f"✅ {ios_path}")
    else:
        print(f"❌ {ios_path}")

    # Check generated files
    print("\n📄 Checking Generated Files:")

    kotlin_files = list(project_root.glob("**/*.kt"))
    swift_files = list(project_root.glob("**/*.swift"))

    print(f"📊 Kotlin files found: {len(kotlin_files)}")
    print(f"📊 Swift files found: {len(swift_files)}")

    if len(kotlin_files) > 0:
        print("✅ Kotlin files generated")
        # Show some examples
        for i, file in enumerate(kotlin_files[:3]):
            print(f"   • {file.relative_to(project_root)}")
        if len(kotlin_files) > 3:
            print(f"   ... and {len(kotlin_files) - 3} more")
    else:
        issues.append("❌ No Kotlin files generated")

    if len(swift_files) > 0:
        print("✅ Swift files generated")
        for file in swift_files:
            print(f"   • {file.relative_to(project_root)}")
    else:
        print("⚠️  No Swift files generated (may be normal)")

    # Check Gradle files
    gradle_files = ["build.gradle.kts", "settings.gradle.kts", "shared/build.gradle.kts"]
    gradle_created = 0
    for gradle_file in gradle_files:
        if (project_root / gradle_file).exists():
            gradle_created += 1

    if gradle_created > 0:
        print(f"✅ Gradle files: {gradle_created}/3 created")
    else:
        issues.append("❌ No Gradle files created")

    # Summary
    print("\n" + "=" * 50)
    if issues:
        print("❌ BUILD ISSUES FOUND:")
        for issue in issues:
            print(f"   {issue}")
        print("\n🔧 To fix: Run the build agents manually:")
        print("   python3 build/agents/01_kmp_setup.py")
        print("   python3 build/agents/02_trademe_api_client.py")
        print("   ... etc")
    else:
        print("✅ BUILD VERIFICATION PASSED!")
        print("🎉 Your TradeMe project is ready!")
        print("\n🚀 Next steps:")
        print("   1. Build with Gradle: ./gradlew build")
        print("   2. Start scraper: python .github/scraper/scraper.py --server")
        print("   3. Run app: ./gradlew :androidApp:run")
        print("   4. Search for listings!")

    return len(issues) == 0

if __name__ == "__main__":
    success = check_build_status()
    sys.exit(0 if success else 1)
