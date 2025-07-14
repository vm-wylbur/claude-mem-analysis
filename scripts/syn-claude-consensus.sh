#!/bin/bash
# syn-claude-consensus.sh - Run syn-claude with three-way AI consensus validation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "🚀 Starting syn-claude three-way consensus curation..."

# Load Qwen2.5-Coder to GPU
echo "1/4 Loading Qwen2.5-Coder to GPU..."
"$SCRIPT_DIR/warm-qwen.sh"

# Generate syn-claude curation session prompt
echo "2/4 Generating syn-claude curation session..."
PROMPT_FILE="/tmp/syn-claude-session-$(date +%s).md"
cd "$PROJECT_DIR"
python -m src.syn.curator > "$PROMPT_FILE"

echo "✅ Curation session prompt generated: $PROMPT_FILE"

# Run zen-mcp consensus with Claude + Gemini + Qwen
echo "3/4 Initiating three-way AI consensus (Claude + Gemini + Qwen)..."
echo "📝 Consensus models: Claude (primary), Gemini 2.5 Pro (quality), Qwen2.5-Coder:32B (technical)"

# Use zen-mcp consensus tool with the generated prompt
mcp__zen__consensus \
  --models "claude,gemini-2.5-pro,qwen2.5-coder:32b" \
  --prompt-file "$PROMPT_FILE" \
  --output-file "/tmp/syn-claude-consensus-$(date +%s).md" \
  --consensus-type "curation" \
  --thinking-mode "high"

# Cleanup GPU resources
echo "4/4 Freeing GPU resources for colleagues..."
"$SCRIPT_DIR/cleanup-qwen.sh"

echo "🎉 Three-way consensus curation complete!"
echo "📊 Results saved to consensus output file"
echo "🤝 GPU resources freed for colleagues"