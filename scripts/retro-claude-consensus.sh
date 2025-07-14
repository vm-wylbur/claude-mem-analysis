#!/bin/bash
# retro-claude-consensus.sh - Run retro-claude with three-way AI consensus validation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "🚀 Starting retro-claude three-way consensus analysis..."

# Load Qwen2.5-Coder to GPU
echo "1/4 Loading Qwen2.5-Coder to GPU..."
"$SCRIPT_DIR/warm-qwen.sh"

# Generate retro-claude session prompt
echo "2/4 Generating retro-claude investigation session..."
PROMPT_FILE="/tmp/retro-claude-session-$(date +%s).md"
cd "$PROJECT_DIR"
python -m src.retro.analyst > "$PROMPT_FILE"

echo "✅ Session prompt generated: $PROMPT_FILE"

# Run zen-mcp consensus with Claude + Gemini + Qwen
echo "3/4 Initiating three-way AI consensus (Claude + Gemini + Qwen)..."
echo "📝 Consensus models: Claude (primary), Gemini 2.5 Pro (strategic), Qwen2.5-Coder:32B (implementation)"

# Use zen-mcp consensus tool with the generated prompt
mcp__zen__consensus \
  --models "claude,gemini-2.5-pro,qwen2.5-coder:32b" \
  --prompt-file "$PROMPT_FILE" \
  --output-file "/tmp/retro-claude-consensus-$(date +%s).md" \
  --consensus-type "validation" \
  --thinking-mode "high"

# Cleanup GPU resources
echo "4/4 Freeing GPU resources for colleagues..."
"$SCRIPT_DIR/cleanup-qwen.sh"

echo "🎉 Three-way consensus analysis complete!"
echo "📊 Results saved to consensus output file"
echo "🤝 GPU resources freed for colleagues"