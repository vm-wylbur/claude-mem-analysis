#!/bin/bash
# memory-pattern-analysis.sh - Main orchestrator script

set -e

echo "🧠 Starting memory pattern analysis..."

# Load config
source ./config.sh

# Setup working directory
WORK_DIR="/tmp/memory-analysis-$(date +%s)"
echo "📁 Working directory: $WORK_DIR"
mkdir -p "$WORK_DIR"

# Make all scripts executable
chmod +x *.sh

# Run analysis pipeline
./01-export-data.sh "$WORK_DIR"
./02-start-neo4j.sh "$WORK_DIR"
./03-analyze-patterns.sh "$WORK_DIR"
./04-run-queries.sh "$WORK_DIR"

# Cleanup
echo ""
echo "🧹 Cleaning up..."
docker stop neo4j-memory-analysis
rm -rf "$WORK_DIR"

echo "✅ Analysis complete!"
