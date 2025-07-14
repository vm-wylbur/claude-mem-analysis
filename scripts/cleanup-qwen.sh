#!/bin/bash
# cleanup-qwen.sh - Unload Qwen2.5-Coder from GPU to free resources for colleagues

echo "🧹 Unloading Qwen2.5-Coder:32B from GPU..."

# Stop the model to free GPU memory
ollama stop qwen2.5-coder:32b

# Brief pause to ensure cleanup completes
sleep 2

# Verify GPU freed
gpu_memory=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | head -1)
echo "🖥️  GPU Memory: ${gpu_memory}MB used (should be ~3MB baseline)"

# Verify model is unloaded
if ollama ps | grep -q "qwen2.5-coder:32b"; then
    echo "⚠️  Warning: Qwen2.5-Coder:32B still appears to be loaded"
else
    echo "✅ Qwen2.5-Coder:32B successfully unloaded"
fi

echo "🎉 GPU resources freed for colleagues"