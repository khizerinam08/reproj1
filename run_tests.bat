@echo off
:: Script to run all crime prediction model tests

echo ===================================================
echo Running Crime Prediction Model Tests
echo ===================================================

:: Create scripts directory if it doesn't exist
if not exist scripts mkdir scripts

:: Run individual tests
echo.
echo 1. Testing Crime Model Directly...
python scripts/test_crime_model.py

echo.
echo 2. Testing RAG Implementation...
python scripts/test_rag_implementation.py

echo.
echo ===================================================
echo All tests completed!
echo ===================================================

pause 