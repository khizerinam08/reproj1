#!/bin/sh
# Script to run all crime prediction model tests

echo "==================================================="
echo "Running Crime Prediction Model Tests"
echo "==================================================="

# Create scripts directory if it doesn't exist
mkdir -p scripts

# Run individual tests
echo "\n\n1. Testing Crime Model Directly..."
python scripts/test_crime_model.py

echo "\n\n2. Testing RAG Implementation..."
python scripts/test_rag_implementation.py

echo "\n\n==================================================="
echo "All tests completed!"
echo "===================================================" 