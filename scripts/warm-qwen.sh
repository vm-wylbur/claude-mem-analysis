#!/bin/bash
# warm-qwen.sh - Load Qwen2.5-Coder to GPU for consensus analysis

echo "🔥 Loading Qwen2.5-Coder:32B to GPU..."
start_time=$(date +%s)

# Pre-load model to GPU with minimal output (32B model takes longer to load)
ollama run qwen2.5-coder:32b "Ready for three-way AI consensus analysis." >/dev/null 2>&1

end_time=$(date +%s)
load_time=$((end_time - start_time))
echo "✅ Qwen2.5-Coder:32B loaded in ${load_time}s, ready for consensus"

# Verify GPU allocation
gpu_memory=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | head -1)
echo "🖥️  GPU Memory: ${gpu_memory}MB used (~21.8GB expected for 32B model)"

# Verify model is loaded in Ollama
if ollama ps | grep -q "qwen2.5-coder:32b"; then
    echo "🤖 Qwen2.5-Coder:32B confirmed loaded and ready"
else
    echo "⚠️  Warning: Qwen2.5-Coder:32B may not be fully loaded"
fi