#!/usr/bin/env python3
"""
pipeline.py - Shared orchestration logic for claude-mem-analysis
"""

import subprocess
import sys
import time
from typing import List, Tuple

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

def run_pipeline(steps: List[Tuple[str, str]], pipeline_name: str, final_command: str = None) -> bool:
    """Run a complete pipeline with error handling"""
    
    print(f"🚀 {pipeline_name.upper()}")
    print("=" * 50)
    print(f"Running pipeline: {' → '.join([desc.split(' (')[0] for _, desc in steps])}")
    print()
    
    start_time = time.time()
    
    # Execute pipeline steps
    for cmd, desc in steps:
        if not run_command(cmd, desc):
            print(f"\n💥 Pipeline failed at: {desc}")
            print("🛑 Stopping execution")
            return False
        print()
    
    # Execute final command if provided
    if final_command:
        print(f"🧠 Executing final step...")
        print(f"📄 Command: {final_command}")
        print()
        
        try:
            result = subprocess.run(
                final_command, 
                shell=True, 
                check=True, 
                text=True
            )
            # The output goes to stdout automatically
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Final step failed: {e}")
            return False
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n🎉 {pipeline_name} finished in {duration:.1f} seconds", file=sys.stderr)
    print("💡 Pipeline complete!", file=sys.stderr)
    
    return True

def get_data_pipeline_steps() -> List[Tuple[str, str]]:
    """Get the standard data collection and import pipeline steps"""
    return [
        ("uv run git-scanner", "Git repository scanning (last 14 days)"),
        ("uv run postgres-importer", "PostgreSQL import with vector embeddings"),
        ("uv run neo4j-importer", "Neo4j relationship mapping"),
        ("uv run elasticsearch-importer", "Elasticsearch document indexing"),
        ("uv run unified-analysis", "Cross-source data validation"),
    ]