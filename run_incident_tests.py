#!/usr/bin/env python3
"""
Test runner for comprehensive incident API tests.
Based on Postman collection with POM architecture.
"""

import sys
import os
import subprocess
from pathlib import Path
from typing import List, Dict, Any


def run_tests(
    test_path: str = "tests/tests_microservices/tests_incidents/test_incidents/",
    markers: List[str] = None,
    verbose: bool = True,
    parallel: bool = False,
    html_report: bool = False,
    allure_report: bool = False
) -> int:
    """Run incident API tests with specified parameters."""
    
    # Build pytest command
    cmd = ["python3", "-m", "pytest"]
    
    # Add test path
    cmd.append(test_path)
    
    # Add markers if specified
    if markers:
        marker_expr = " or ".join(markers)
        cmd.extend(["-m", marker_expr])
    
    # Add verbosity
    if verbose:
        cmd.append("-v")
    
    # Add parallel execution
    if parallel:
        cmd.extend(["-n", "auto"])
    
    # Add HTML report
    if html_report:
        cmd.extend(["--html=reports/incident_tests_report.html", "--self-contained-html"])
    
    # Add Allure report
    if allure_report:
        cmd.extend(["--alluredir=reports/allure-results"])
    
    # Add additional options
    cmd.extend([
        "--tb=short",  # Short traceback format
        "--strict-markers",  # Strict marker checking
        "--disable-warnings",  # Disable warnings
        "--color=yes"  # Colored output
    ])
    
    print(f"Running command: {' '.join(cmd)}")
    print("=" * 60)
    
    # Run the tests
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1


def run_basic_tests() -> int:
    """Run basic/smoke tests only."""
    print("🚀 Running Basic/Smoke Tests")
    print("=" * 60)
    return run_tests(markers=["basic", "smoke"])


def run_crud_tests() -> int:
    """Run CRUD tests only."""
    print("🔧 Running CRUD Tests")
    print("=" * 60)
    return run_tests(markers=["basic"])


def run_search_tests() -> int:
    """Run search and filtering tests."""
    print("🔍 Running Search Tests")
    print("=" * 60)
    return run_tests(markers=["basic"])


def run_negative_tests() -> int:
    """Run negative test scenarios."""
    print("❌ Running Negative Tests")
    print("=" * 60)
    return run_tests(markers=["negative"])


def run_performance_tests() -> int:
    """Run performance tests."""
    print("⚡ Running Performance Tests")
    print("=" * 60)
    return run_tests(markers=["performance"])


def run_all_tests() -> int:
    """Run all incident tests."""
    print("🎯 Running All Incident Tests")
    print("=" * 60)
    return run_tests()


def run_regression_tests() -> int:
    """Run regression tests."""
    print("🔄 Running Regression Tests")
    print("=" * 60)
    return run_tests(markers=["regression"])


def run_with_reports() -> int:
    """Run tests with HTML and Allure reports."""
    print("📊 Running Tests with Reports")
    print("=" * 60)
    
    # Create reports directory
    os.makedirs("reports", exist_ok=True)
    
    return run_tests(
        html_report=True,
        allure_report=True,
        parallel=True
    )


def check_environment() -> bool:
    """Check if test environment is properly configured."""
    print("🔍 Checking Test Environment")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("tests/tests_microservices/tests_incidents").exists():
        print("❌ Test directory not found. Please run from project root.")
        return False
    
    # Check if config files exist
    if not Path("config/auth.py").exists():
        print("❌ Auth config not found. Please ensure config/auth.py exists.")
        return False
    
    # Check if API client exists
    if not Path("tests/tests_microservices/utils/incidents/incidents_api.py").exists():
        print("❌ IncidentsAPI client not found.")
        return False
    
    # Check environment variables
    token = os.getenv("EPUTS_TOKEN")
    if not token:
        print("⚠️  EPUTS_TOKEN not set. Tests will use default token.")
    else:
        print("✅ EPUTS_TOKEN is set.")
    
    print("✅ Environment check passed.")
    return True


def show_test_structure():
    """Show the test structure and available tests."""
    print("📁 Incident API Test Structure")
    print("=" * 60)
    
    test_dir = Path("tests/tests_microservices/tests_incidents/test_incidents")
    if not test_dir.exists():
        print("❌ Test directory not found.")
        return
    
    print("Test Files:")
    for test_file in test_dir.glob("test_*.py"):
        print(f"  📄 {test_file.name}")
    
    print("\nAvailable Test Categories:")
    print("  🟢 basic     - Basic functionality tests")
    print("  🔥 smoke     - Smoke tests for critical functionality")
    print("  ❌ negative  - Negative test scenarios")
    print("  ⚡ performance - Performance and load tests")
    print("  🔄 regression - Regression tests")
    
    print("\nAvailable Commands:")
    print("  python run_incident_tests.py basic      - Run basic tests")
    print("  python run_incident_tests.py crud       - Run CRUD tests")
    print("  python run_incident_tests.py search     - Run search tests")
    print("  python run_incident_tests.py negative   - Run negative tests")
    print("  python run_incident_tests.py performance - Run performance tests")
    print("  python run_incident_tests.py all        - Run all tests")
    print("  python run_incident_tests.py reports    - Run with reports")


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("🎯 Incident API Test Runner")
        print("=" * 60)
        print("Usage: python run_incident_tests.py <command>")
        print("\nCommands:")
        print("  basic       - Run basic/smoke tests")
        print("  crud        - Run CRUD tests")
        print("  search      - Run search tests")
        print("  negative    - Run negative tests")
        print("  performance - Run performance tests")
        print("  all         - Run all tests")
        print("  regression  - Run regression tests")
        print("  reports     - Run with HTML/Allure reports")
        print("  check       - Check environment")
        print("  structure   - Show test structure")
        return 0
    
    command = sys.argv[1].lower()
    
    # Check environment first
    if not check_environment():
        return 1
    
    # Route to appropriate function
    if command == "basic":
        return run_basic_tests()
    elif command == "crud":
        return run_crud_tests()
    elif command == "search":
        return run_search_tests()
    elif command == "negative":
        return run_negative_tests()
    elif command == "performance":
        return run_performance_tests()
    elif command == "all":
        return run_all_tests()
    elif command == "regression":
        return run_regression_tests()
    elif command == "reports":
        return run_with_reports()
    elif command == "check":
        return 0  # Already checked above
    elif command == "structure":
        show_test_structure()
        return 0
    else:
        print(f"❌ Unknown command: {command}")
        print("Use 'python run_incident_tests.py' to see available commands.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
