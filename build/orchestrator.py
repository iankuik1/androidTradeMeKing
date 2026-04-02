#!/usr/bin/env python3
"""
TradeMe Build Agent System
Local build orchestration - replaces GitHub Actions workflows
Run: python build/orchestrator.py [--step 1-6] [--verbose]
"""

import os
import sys
import subprocess
import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Tuple

# Colors for terminal output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def log_header(msg: str):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{msg:^70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")

def log_info(msg: str):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.ENDC}")

def log_success(msg: str):
    print(f"{Colors.GREEN}✓ {msg}{Colors.ENDC}")

def log_warning(msg: str):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.ENDC}")

def log_error(msg: str):
    print(f"{Colors.RED}✗ {msg}{Colors.ENDC}")

def run_agent(agent_name: str, agent_path: str, verbose: bool = False) -> Tuple[bool, str]:
    """Run a single build agent"""
    log_info(f"Running: {agent_name}")

    try:
        result = subprocess.run(
            [sys.executable, agent_path],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )

        if result.returncode == 0:
            log_success(f"{agent_name} completed")
            if verbose and result.stdout:
                print(result.stdout)
            return True, result.stdout
        else:
            log_error(f"{agent_name} failed")
            if result.stderr:
                print(f"{Colors.RED}{result.stderr}{Colors.ENDC}")
            return False, result.stderr

    except subprocess.TimeoutExpired:
        log_error(f"{agent_name} timed out (5 min)")
        return False, "Timeout"
    except Exception as e:
        log_error(f"{agent_name} error: {e}")
        return False, str(e)

def get_project_root() -> Path:
    """Get project root directory"""
    current = Path(__file__).parent.parent
    return current

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="TradeMe Build Agent System - Local Build Orchestration"
    )
    parser.add_argument(
        '--step',
        type=int,
        choices=range(1, 7),
        help='Run specific step (1-6)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose output'
    )
    parser.add_argument(
        '--skip-checks',
        action='store_true',
        help='Skip prerequisite checks'
    )

    args = parser.parse_args()

    project_root = get_project_root()
    build_dir = project_root / "build" / "agents"

    # Build agents configuration
    agents = [
        {
            "number": 1,
            "name": "KMP Project Setup",
            "script": "01_kmp_setup.py",
            "duration": "2-3 min",
            "description": "Creates project structure, Gradle config, modules"
        },
        {
            "number": 2,
            "name": "TradeMe Data Client",
            "script": "02_trademe_api_client.py",
            "duration": "2-3 min",
            "description": "Real-time scraper client with RealTimeScraperClient"
        },
        {
            "number": 3,
            "name": "Data Models",
            "script": "03_data_models.py",
            "duration": "2-3 min",
            "description": "Listing models, search filters, repository pattern"
        },
        {
            "number": 4,
            "name": "Image Loading",
            "script": "04_image_loading.py",
            "duration": "2-3 min",
            "description": "Image caching system, memory & disk cache"
        },
        {
            "number": 5,
            "name": "Search UI",
            "script": "05_search_ui.py",
            "duration": "3-4 min",
            "description": "Android Compose UI, iOS SwiftUI components"
        },
        {
            "number": 6,
            "name": "Search Integration",
            "script": "06_search_integration.py",
            "duration": "2-3 min",
            "description": "SearchViewModel, repository integration, use cases"
        }
    ]

    # Display header
    log_header("🚀 TradeMe Build Agent System")
    print(f"{Colors.CYAN}Local Build Orchestration - Replaces GitHub Actions{Colors.ENDC}")
    print(f"{Colors.CYAN}Project Root: {project_root}{Colors.ENDC}\n")

    # Show agents
    print(f"{Colors.BOLD}Available Agents:{Colors.ENDC}")
    for agent in agents:
        print(f"  {agent['number']}. {agent['name']} ({agent['duration']})")
        print(f"     {agent['description']}")

    print()

    # Run agents
    if args.step:
        # Run specific step
        agent = next((a for a in agents if a['number'] == args.step), None)
        if agent:
            agent_path = build_dir / agent['script']
            if agent_path.exists():
                success, output = run_agent(agent['name'], str(agent_path), args.verbose)
                sys.exit(0 if success else 1)
            else:
                log_error(f"Agent script not found: {agent_path}")
                sys.exit(1)
    else:
        # Run all agents sequentially
        log_header("🏗️  Building TradeMe Application")
        print(f"{Colors.CYAN}Running all agents in sequence...{Colors.ENDC}\n")

        start_time = time.time()
        results = []

        for agent in agents:
            agent_path = build_dir / agent['script']

            if not agent_path.exists():
                log_warning(f"Skipping {agent['name']} - script not found")
                results.append((agent['number'], agent['name'], False, "Script not found"))
                continue

            print(f"\n{Colors.BOLD}[{agent['number']}/6]{Colors.ENDC} {agent['name']}")
            success, output = run_agent(agent['name'], str(agent_path), args.verbose)
            results.append((agent['number'], agent['name'], success, output))

            if not success:
                log_error(f"Build failed at step {agent['number']}")
                break

            time.sleep(1)  # Small delay between agents

        # Summary
        elapsed = time.time() - start_time
        log_header("📊 Build Summary")

        passed = sum(1 for _, _, success, _ in results if success)
        total = len(results)

        for number, name, success, _ in results:
            status = f"{Colors.GREEN}✓{Colors.ENDC}" if success else f"{Colors.RED}✗{Colors.ENDC}"
            print(f"  {status} {number}. {name}")

        print(f"\n{Colors.BOLD}Results: {passed}/{total} agents completed{Colors.ENDC}")
        print(f"{Colors.CYAN}Elapsed Time: {elapsed:.1f}s{Colors.ENDC}\n")

        if passed == total:
            log_success("🎉 Build completed successfully!")
            print(f"\n{Colors.BOLD}Next steps:{Colors.ENDC}")
            print("  1. Review generated code in shared/, androidApp/, iosApp/")
            print("  2. Start scraper server: python .github/scraper/scraper.py --server")
            print("  3. Run app: ./gradlew :androidApp:run")
            print("  4. Search for listings!")
            sys.exit(0)
        else:
            log_error(f"Build failed - {total - passed} agents did not complete")
            sys.exit(1)

if __name__ == "__main__":
    main()

