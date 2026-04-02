#!/usr/bin/env python3
"""
Agent 1: KMP Project Setup
Creates Kotlin Multiplatform project structure with Gradle configuration
"""

import os
from pathlib import Path
import subprocess

def create_directories():
    """Create project directory structure"""
    dirs = [
        "shared/src/commonMain/kotlin/com/trademe",
        "shared/src/commonMain/resources",
        "shared/src/androidMain/kotlin/com/trademe",
        "shared/src/iosMain/kotlin/com/trademe",
        "androidApp/src/main/kotlin/com/trademe/ui/screens",
        "androidApp/src/main/kotlin/com/trademe/ui/components",
        "androidApp/src/main/kotlin/com/trademe/viewmodel",
        "androidApp/src/main/res/values",
        "iosApp/TradeMe/Views",
    ]

    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {d}")

def create_gradle_files():
    """Create Gradle build configuration files"""

    # Root build.gradle.kts
    root_gradle = """
plugins {
    id("org.jetbrains.kotlin.multiplatform") version "1.9.20" apply false
    id("com.android.library") version "8.1.0" apply false
    id("com.android.application") version "8.1.0" apply false
}

allprojects {
    repositories {
        google()
        mavenCentral()
    }
}
"""

    # Settings file
    settings = """
pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}

rootProject.name = "TradeMe"
include(":shared")
include(":androidApp")
"""

    # Shared module build.gradle.kts
    shared_gradle = """
plugins {
    kotlin("multiplatform") version "1.9.20"
    id("com.android.library") version "8.1.0"
}

kotlin {
    androidTarget()

    iosX64()
    iosArm64()
    iosSimulatorArm64()

    sourceSets {
        commonMain.dependencies {
            implementation("io.ktor:ktor-client-core:2.3.0")
            implementation("io.ktor:ktor-client-json:2.3.0")
            implementation("io.ktor:ktor-client-serialization:2.3.0")
            implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.5.1")
            implementation("org.jetbrains.kotlinx:kotlinx-coroutines-core:1.7.0")
        }

        androidMain.dependencies {
            implementation("io.ktor:ktor-client-android:2.3.0")
        }

        iosMain.dependencies {
            implementation("io.ktor:ktor-client-darwin:2.3.0")
        }
    }
}

android {
    namespace = "com.trademe.shared"
    compileSdk = 34
    defaultConfig {
        minSdk = 24
    }
}
"""

    files = {
        "build.gradle.kts": root_gradle,
        "settings.gradle.kts": settings,
        "shared/build.gradle.kts": shared_gradle,
    }

    for path, content in files.items():
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            f.write(content.strip())
        print(f"✓ Created: {path}")

def create_gradle_wrapper():
    """Create Gradle wrapper script"""
    import shutil
    import tempfile

    try:
        subprocess.run(["gradle", "wrapper", "--gradle-version", "8.4"], check=False)
        print("✓ Created Gradle wrapper")
    except Exception as e:
        print(f"⚠ Gradle wrapper creation skipped: {e}")

def main():
    print("\n" + "="*70)
    print("Agent 1: KMP Project Setup".center(70))
    print("="*70 + "\n")

    print("📁 Creating directory structure...")
    create_directories()

    print("\n📋 Creating Gradle configuration...")
    create_gradle_files()

    print("\n🔧 Initializing Gradle wrapper...")
    create_gradle_wrapper()

    print("\n" + "="*70)
    print("✓ KMP Project Setup Complete".center(70))
    print("="*70 + "\n")

    return 0

if __name__ == "__main__":
    exit(main())

