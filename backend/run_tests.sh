#!/bin/bash
echo "=== Running Backend Tests ==="
echo ""
echo "1. Unit Tests..."
uv run pytest tests/unit/ -v --tb=short

echo ""
echo "2. Integration Tests..."
uv run pytest tests/integration/ -v --tb=short

echo ""
echo "3. Full Test Suite with Coverage..."
uv run pytest --cov=src --cov-report=term-missing --cov-report=html

echo ""
echo "=== Test Summary ==="
echo "Coverage report generated in htmlcov/index.html"
