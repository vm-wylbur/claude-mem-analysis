# Git Commit Memory Integration - Design Proposal

## 🎯 **Concept Overview**
Automatically scan git repositories in `~/projects` to extract recent commit data and integrate it into the memory analysis system, providing richer context for development pattern discovery.

## 📊 **Potential Value**

### **Enhanced Pattern Discovery:**
- **Actual Development Activity**: Real commit patterns vs subjective memory entries
- **Code Change Velocity**: Frequency, size, and timing of actual changes
- **Project Context**: Multiple project comparison and cross-pollination patterns
- **Collaboration Patterns**: Multi-contributor workflows and interaction styles
- **Technology Adoption**: New tools/frameworks appearing in commits

### **Cross-Reference Opportunities:**
- **Memory → Commit Correlation**: Match memory entries to actual development work
- **Productivity Validation**: Verify self-reported productivity against actual output
- **Problem-Solution Tracking**: Connect reported issues to actual fixes in code
- **Learning Curve Analysis**: Track real skill development through commit evolution

## 🔍 **Data Collection Strategy**

### **Git Data to Extract:**
```bash
# Per repository in ~/projects:
- Repository name and path
- Commit hash, timestamp, author
- Commit message and description
- Files changed (paths, additions, deletions)
- Branch information
- Merge/PR patterns
- Tag/release information
```

### **Time Window:**
- **Default**: Last 7 days for initial implementation
- **Configurable**: Extend to 30 days or specific date ranges
- **Incremental**: Only new commits since last scan

### **Metadata Enrichment:**
- **Language Detection**: Primary programming languages per repo
- **Project Classification**: Web app, CLI tool, library, etc.
- **Commit Type Classification**: Feature, bugfix, refactor, docs, test
- **Complexity Estimation**: Lines changed, files affected, commit message analysis

## 🛠️ **Technical Implementation**

### **Git Scanning Script:**
```python
#!/usr/bin/env python3
"""
21-git-commit-scanner.py - Scan ~/projects for recent git commits
"""

import os
import subprocess
import json
from datetime import datetime, timedelta
from pathlib import Path

def scan_projects_directory():
    """Find all git repositories in ~/projects"""
    projects_dir = Path.home() / "projects"
    git_repos = []
    
    for item in projects_dir.iterdir():
        if item.is_dir() and (item / ".git").exists():
            git_repos.append(item)
    
    return git_repos

def extract_recent_commits(repo_path, days=7):
    """Extract commits from last N days"""
    since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    cmd = [
        "git", "log", 
        f"--since={since_date}",
        "--pretty=format:%H|%at|%an|%ae|%s|%b",
        "--stat=1000,1000"  # Include file change stats
    ]
    
    result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)
    return result.stdout

def classify_commit_type(message):
    """Classify commit based on message patterns"""
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['fix', 'bug', 'error', 'issue']):
        return 'bugfix'
    elif any(word in message_lower for word in ['add', 'new', 'feature', 'implement']):
        return 'feature'
    elif any(word in message_lower for word in ['refactor', 'cleanup', 'reorganize']):
        return 'refactor'
    elif any(word in message_lower for word in ['test', 'spec', 'coverage']):
        return 'test'
    elif any(word in message_lower for word in ['doc', 'readme', 'comment']):
        return 'documentation'
    else:
        return 'general'
```

### **Memory Integration:**
```python
def create_commit_memory_entry(commit_data, repo_name):
    """Convert git commit to memory entry"""
    
    content = f"""Git Commit Analysis - {repo_name}
    
Commit: {commit_data['hash'][:8]}
Message: {commit_data['message']}
Type: {commit_data['type']}
Files Changed: {len(commit_data['files'])}
Lines Added: {commit_data['additions']}
Lines Deleted: {commit_data['deletions']}

Technical Context:
{commit_data['files_summary']}

Development Activity: {commit_data['activity_classification']}
"""
    
    # Store using memory system
    mcp__claude_mem__store_dev_memory(
        content=content,
        type="code",
        tags=[
            "git-commit", 
            repo_name,
            commit_data['type'],
            f"language-{commit_data['primary_language']}"
        ],
        status="completed",
        code_changes=commit_data['files'],
        key_decisions=[f"Implemented {commit_data['type']} in {repo_name}"]
    )
```

## 🔒 **Privacy & Security Considerations**

### **Critical Security Questions:**
1. **Sensitive Information**: Git commits may contain API keys, passwords, personal data
2. **Proprietary Code**: Work repositories with confidential intellectual property  
3. **Private Repositories**: Personal projects not intended for analysis
4. **Commit Messages**: May contain private context or sensitive details

### **Proposed Safeguards:**
```python
# Security filters and controls
EXCLUDED_PATTERNS = [
    r'api[_-]?key',
    r'password',
    r'secret',
    r'token',
    r'credential',
    r'private[_-]?key'
]

EXCLUDED_REPOS = [
    'work-project',
    'client-code', 
    'confidential',
    '.secrets'
]

def sanitize_commit_data(commit):
    """Remove sensitive information from commit data"""
    # Filter out sensitive patterns
    # Exclude certain file types (.env, .key, etc.)
    # Anonymize email addresses
    # Truncate overly detailed commit messages
```

### **User Controls:**
- **Opt-in per repository**: Explicit consent for each repo
- **Exclusion patterns**: User-defined filters for sensitive content
- **Data retention**: Configurable cleanup of git-sourced memories
- **Local processing**: No external API calls for git data

## 📈 **Integration with Existing Analysis**

### **Enhanced Elasticsearch Fields:**
```json
{
  "memory_id": "git_commit_abc123",
  "content_type": "git_commit",
  "repository_name": "my-web-app",
  "commit_hash": "abc123def456",
  "commit_type": "feature",
  "programming_language": "typescript",
  "files_changed": 5,
  "lines_added": 127,
  "lines_deleted": 45,
  "commit_timestamp": "2025-01-13T14:30:00Z",
  "development_activity": "frontend_enhancement"
}
```

### **Neo4j Relationships:**
```cypher
// Link commits to memory entries
(commit:GitCommit)-[:IMPLEMENTS]->(memory:Memory)
(commit1:GitCommit)-[:FOLLOWS]->(commit2:GitCommit)
(commit:GitCommit)-[:BELONGS_TO]->(repo:Repository)
```

### **New Analysis Capabilities:**
- **Memory-Commit Correlation**: "Which commits correspond to documented memories?"
- **Multi-Project Patterns**: "How do development patterns vary across projects?"
- **Actual vs Perceived Productivity**: "Does reported productivity match commit activity?"
- **Technology Adoption Tracking**: "When and how are new technologies introduced?"

## 🚨 **Implementation Considerations**

### **Technical Challenges:**
1. **Scale**: Large repositories with thousands of commits
2. **Performance**: Git operations can be slow on large repos
3. **Data Volume**: Could significantly increase memory database size
4. **Parsing Complexity**: Diverse commit message formats and conventions

### **Recommended Approach:**
1. **Start Small**: Single repository proof of concept
2. **User Control**: Explicit opt-in and granular controls
3. **Incremental**: Only scan new commits after initial run
4. **Filtering**: Strong content filtering for security/privacy
5. **Analytics**: Measure value add before broader rollout

## 🎯 **Next Steps**

### **Phase 1: Proof of Concept**
- Build git scanner for single repository
- Create security filtering system
- Test memory integration workflow
- Validate analysis value with limited dataset

### **Phase 2: Multi-Repository Support**
- Expand to ~/projects directory scanning
- Add user configuration and controls
- Enhance commit classification system
- Integrate with existing analysis framework

### **Phase 3: Advanced Analytics**
- Cross-repository pattern analysis
- Memory-commit correlation algorithms
- Productivity validation models
- Technology adoption tracking

This enhancement could provide unprecedented insight into actual development patterns while requiring careful attention to privacy and security concerns.