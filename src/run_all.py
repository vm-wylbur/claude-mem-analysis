#!/usr/bin/env python3
"""
run_all.py - Complete retro-claude analysis pipeline
Single command to scan, import, analyze, and generate investigation session
"""

import sys
from src.shared.pipeline import run_pipeline, get_data_pipeline_steps

def main():
    """Run complete retro-claude analysis pipeline"""
    
    steps = get_data_pipeline_steps()
    final_command = "uv run retro-claude"
    
    success = run_pipeline(
        steps=steps,
        pipeline_name="retro-claude complete analysis pipeline", 
        final_command=final_command
    )
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()