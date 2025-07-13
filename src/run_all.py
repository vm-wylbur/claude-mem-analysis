#!/usr/bin/env python3
"""
run_all.py - Complete retro-claude analysis pipeline
Single command to scan, import, analyze, and generate investigation session
"""

import subprocess
import sys
import time
from pathlib import Path

def run_command(cmd: str, description: str) -> bool:
    """Run a command and return success status"""
    print(f"🔄 {description}...")
    
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            check=True, 
            capture_output=True, 
            text=True
        )
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Command: {cmd}")
        print(f"   Error: {e.stderr}")
        return False

def main():
    """Run complete retro-claude analysis pipeline"""
    
    print("🚀 RETRO-CLAUDE COMPLETE ANALYSIS PIPELINE")
    print("=" * 50)
    print("Running full hands-off analysis: scan → import → investigate")
    print()
    
    start_time = time.time()
    
    # Pipeline steps
    steps = [
        ("uv run git-scanner", "Git repository scanning (last 14 days)"),
        ("uv run postgres-importer", "PostgreSQL import with vector embeddings"),
        ("uv run neo4j-importer", "Neo4j relationship mapping"),
        ("uv run elasticsearch-importer", "Elasticsearch document indexing"),
        ("uv run unified-analysis", "Cross-source data validation"),
    ]
    
    # Execute pipeline
    for cmd, desc in steps:
        if not run_command(cmd, desc):
            print(f"\n💥 Pipeline failed at: {desc}")
            print("🛑 Stopping execution")
            sys.exit(1)
        print()
    
    # Generate retro-claude investigation session
    print("🧠 Generating retro-claude investigation session...")
    print("📄 Ready for: uv run retro-claude | claude")
    print()
    
    # Output retro-claude session directly
    try:
        result = subprocess.run(
            "uv run retro-claude", 
            shell=True, 
            check=True, 
            text=True
        )
        # The output goes to stdout automatically
        
    except subprocess.CalledProcessError as e:
        print(f"❌ retro-claude session generation failed: {e}")
        sys.exit(1)
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n🎉 Complete pipeline finished in {duration:.1f} seconds", file=sys.stderr)
    print("💡 Ready for Claude investigation!", file=sys.stderr)

if __name__ == "__main__":
    main()