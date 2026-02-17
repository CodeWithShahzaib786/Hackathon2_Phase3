#!/bin/bash
echo "=== Running Frontend Tests ==="
echo ""
echo "Installing test dependencies if needed..."
npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event jest jest-environment-jsdom

echo ""
echo "Running all component tests..."
npm test -- --coverage --watchAll=false

echo ""
echo "=== Test Summary ==="
echo "Coverage report generated in coverage/"
