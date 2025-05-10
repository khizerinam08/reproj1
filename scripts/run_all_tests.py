"""
Run all test scripts for the crime prediction RAG system.

This script executes all test components to verify the entire system.
"""
import os
import sys
import subprocess
import time

def print_section(title):
    """Print a section title for better test readability."""
    line = "=" * 80
    print(f"\n{line}")
    print(f" {title} ".center(80, "="))
    print(f"{line}\n")

def run_test(script_name, description):
    """Run a test script and return the result."""
    print_section(description)
    
    script_path = os.path.join("scripts", script_name)
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            check=True
        )
        print(result.stdout)
        if result.stderr:
            print("ERRORS:")
            print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Test failed with exit code {e.returncode}")
        print(e.stdout)
        print("ERRORS:")
        print(e.stderr)
        return False

def main():
    """Run all test scripts in sequence."""
    print_section("CRIME PREDICTION RAG SYSTEM TEST SUITE")
    print("Starting test suite...")
    start_time = time.time()
    
    all_tests = [
        ("test_query_processor.py", "Testing Query Processor"),
        ("test_crime_model_rag.py", "Testing Crime Model RAG"),
        # Add other test scripts here as they are created
    ]
    
    # Track test results
    results = {}
    
    # Run all tests
    for script_name, description in all_tests:
        results[script_name] = run_test(script_name, description)
    
    # Print summary
    print_section("TEST SUMMARY")
    all_passed = True
    for script_name, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        print(f"{script_name}: {status}")
        if not passed:
            all_passed = False
    
    # Calculate elapsed time
    elapsed_time = time.time() - start_time
    print(f"\nTotal test time: {elapsed_time:.2f} seconds")
    
    # Set exit code based on test results
    if all_passed:
        print("\nAll tests passed!")
        sys.exit(0)
    else:
        print("\nSome tests failed. See details above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 