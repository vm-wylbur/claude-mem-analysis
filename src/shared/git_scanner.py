#!/usr/bin/env python3
"""
21-git-commit-scanner.py - Proof of concept: Scan git commits and integrate with memory system
"""

import os
import subprocess
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

class GitCommitScanner:
    def __init__(self, projects_dir: str = None):
        self.projects_dir = Path(projects_dir or Path.home() / "projects")
        
        # Security filters
        self.sensitive_patterns = [
            r'api[_-]?key',
            r'password', 
            r'secret',
            r'token',
            r'credential',
            r'private[_-]?key',
            r'auth[_-]?token'
        ]
        
        # No repositories excluded - this is personal data for personal use  
        # Scanning all 22+ repositories for comprehensive analysis
        self.excluded_repos = set()
    
    def find_git_repositories(self) -> List[Path]:
        """Find all git repositories in projects directory"""
        git_repos = []
        
        if not self.projects_dir.exists():
            print(f"❌ Projects directory not found: {self.projects_dir}")
            return git_repos
        
        for item in self.projects_dir.iterdir():
            if item.is_dir() and (item / ".git").exists():
                # Check if repo is excluded
                if item.name not in self.excluded_repos:
                    git_repos.append(item)
                else:
                    print(f"⏭️  Skipping excluded repository: {item.name}")
        
        return git_repos
    
    def extract_recent_commits(self, repo_path: Path, days: int = 14) -> List[Dict]:
        """Extract commits from last N days"""
        since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        try:
            # Get commit metadata
            cmd = [
                "git", "log", 
                f"--since={since_date}",
                "--pretty=format:%H|%at|%an|%ae|%s",
                "--no-merges"  # Skip merge commits for cleaner data
            ]
            
            result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"⚠️  Git log failed for {repo_path.name}: {result.stderr}")
                return []
            
            commits = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    parts = line.split('|')
                    if len(parts) >= 5:
                        commit_hash, timestamp, author, email, message = parts[:5]
                        
                        # Get file stats for this commit
                        stats = self.get_commit_stats(repo_path, commit_hash)
                        
                        commit_data = {
                            'hash': commit_hash,
                            'timestamp': datetime.fromtimestamp(int(timestamp)).isoformat(),
                            'author': author,
                            'email': self.anonymize_email(email),
                            'message': self.sanitize_message(message),
                            'repository': repo_path.name,
                            'commit_type': self.classify_commit_type(message),
                            'files_changed': stats['files_changed'],
                            'lines_added': stats['lines_added'],
                            'lines_deleted': stats['lines_deleted'],
                            'primary_language': self.detect_language(repo_path)
                        }
                        
                        commits.append(commit_data)
            
            return commits
            
        except Exception as e:
            print(f"❌ Error processing {repo_path.name}: {e}")
            return []
    
    def get_commit_stats(self, repo_path: Path, commit_hash: str) -> Dict:
        """Get file change statistics for a commit"""
        try:
            cmd = ["git", "show", "--stat", "--format=", commit_hash]
            result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)
            
            if result.returncode != 0:
                return {'files_changed': 0, 'lines_added': 0, 'lines_deleted': 0}
            
            # Parse git stat output
            lines = result.stdout.strip().split('\n')
            files_changed = 0
            lines_added = 0
            lines_deleted = 0
            
            for line in lines:
                if '|' in line and ('+' in line or '-' in line):
                    files_changed += 1
                    # Extract +/- counts
                    plus_count = line.count('+')
                    minus_count = line.count('-')
                    lines_added += plus_count
                    lines_deleted += minus_count
            
            return {
                'files_changed': files_changed,
                'lines_added': lines_added, 
                'lines_deleted': lines_deleted
            }
            
        except Exception:
            return {'files_changed': 0, 'lines_added': 0, 'lines_deleted': 0}
    
    def detect_language(self, repo_path: Path) -> str:
        """Detect primary programming language in repository"""
        try:
            # Simple heuristic based on file extensions
            language_files = {
                'python': 0,
                'javascript': 0,
                'typescript': 0,
                'java': 0,
                'go': 0,
                'rust': 0,
                'cpp': 0,
                'shell': 0
            }
            
            for ext_pattern, lang in [
                ('*.py', 'python'),
                ('*.js', 'javascript'), 
                ('*.ts', 'typescript'),
                ('*.java', 'java'),
                ('*.go', 'go'),
                ('*.rs', 'rust'),
                ('*.cpp', 'cpp'),
                ('*.sh', 'shell')
            ]:
                count = len(list(repo_path.glob(f"**/{ext_pattern}")))
                language_files[lang] += count
            
            # Return most common language
            primary_lang = max(language_files, key=language_files.get)
            return primary_lang if language_files[primary_lang] > 0 else 'unknown'
            
        except Exception:
            return 'unknown'
    
    def classify_commit_type(self, message: str) -> str:
        """Classify commit based on message patterns"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['fix', 'bug', 'error', 'issue', 'patch']):
            return 'bugfix'
        elif any(word in message_lower for word in ['add', 'new', 'feature', 'implement', 'create']):
            return 'feature'
        elif any(word in message_lower for word in ['refactor', 'cleanup', 'reorganize', 'restructure']):
            return 'refactor'
        elif any(word in message_lower for word in ['test', 'spec', 'coverage', 'unit', 'integration']):
            return 'test'
        elif any(word in message_lower for word in ['doc', 'readme', 'comment', 'documentation']):
            return 'documentation'
        elif any(word in message_lower for word in ['update', 'upgrade', 'bump', 'version']):
            return 'update'
        else:
            return 'general'
    
    def sanitize_message(self, message: str) -> str:
        """Remove sensitive information from commit messages"""
        sanitized = message
        
        # Remove potential sensitive patterns
        for pattern in self.sensitive_patterns:
            sanitized = re.sub(pattern, '[REDACTED]', sanitized, flags=re.IGNORECASE)
        
        # Truncate very long messages
        if len(sanitized) > 200:
            sanitized = sanitized[:197] + "..."
        
        return sanitized
    
    def anonymize_email(self, email: str) -> str:
        """Anonymize email addresses for privacy"""
        if '@' in email:
            local, domain = email.split('@', 1)
            # Keep first letter and domain for pattern analysis
            return f"{local[0]}***@{domain}"
        return email
    
    def create_memory_entries(self, commits: List[Dict], dry_run: bool = False) -> int:
        """Convert git commits to memory entries"""
        entries_created = 0
        
        for commit in commits:
            # Create comprehensive memory content
            content = f"""Git Commit Analysis - {commit['repository']}

Commit: {commit['hash'][:8]}
Type: {commit['commit_type']}
Author: {commit['author']}
Timestamp: {commit['timestamp']}

Message: {commit['message']}

Development Activity:
- Files Changed: {commit['files_changed']}
- Lines Added: {commit['lines_added']}
- Lines Deleted: {commit['lines_deleted']}
- Primary Language: {commit['primary_language']}

Context: Automated import from git commit history for development pattern analysis.
"""
            
            if dry_run:
                print(f"📝 Would create memory entry:")
                print(f"   Repository: {commit['repository']}")
                print(f"   Type: {commit['commit_type']}")
                print(f"   Message: {commit['message'][:50]}...")
                print(f"   Changes: {commit['files_changed']} files, +{commit['lines_added']}/-{commit['lines_deleted']} lines")
                print()
            else:
                # Store for batch creation with MCP tools later
                print(f"📝 Prepared memory entry for commit {commit['hash'][:8]}")
                entries_created += 1
        
        return entries_created

def main():
    """Main git commit scanning function"""
    scanner = GitCommitScanner()
    
    print("🔍 GIT COMMIT MEMORY INTEGRATION - PROOF OF CONCEPT")
    print("=" * 60)
    
    # Find repositories
    repos = scanner.find_git_repositories()
    print(f"📁 Found {len(repos)} git repositories in {scanner.projects_dir}")
    
    if not repos:
        print("❌ No git repositories found to scan")
        return
    
    # Scan for recent commits
    all_commits = []
    for repo in repos:  # Scan all repositories
        print(f"\\n🔍 Scanning {repo.name}...")
        commits = scanner.extract_recent_commits(repo, days=14)
        all_commits.extend(commits)
        print(f"   Found {len(commits)} recent commits")
    
    print(f"\\n📊 TOTAL COMMITS FOUND: {len(all_commits)}")
    
    if all_commits:
        # Show summary statistics
        commit_types = {}
        languages = {}
        total_files = 0
        total_additions = 0
        total_deletions = 0
        
        for commit in all_commits:
            commit_types[commit['commit_type']] = commit_types.get(commit['commit_type'], 0) + 1
            languages[commit['primary_language']] = languages.get(commit['primary_language'], 0) + 1
            total_files += commit['files_changed']
            total_additions += commit['lines_added']
            total_deletions += commit['lines_deleted']
        
        print(f"\\n📈 COMMIT ANALYSIS SUMMARY:")
        print(f"   Commit Types: {dict(sorted(commit_types.items(), key=lambda x: x[1], reverse=True))}")
        print(f"   Languages: {dict(sorted(languages.items(), key=lambda x: x[1], reverse=True))}")
        print(f"   Total Changes: {total_files} files, +{total_additions}/-{total_deletions} lines")
        
        # Create memory entries (actual creation)
        print(f"\\n🧠 MEMORY INTEGRATION:")
        entries_count = scanner.create_memory_entries(all_commits, dry_run=False)
        
        # Save commit data for manual import
        if all_commits:
            import json
            with open('git_commits_for_import.json', 'w') as f:
                json.dump(all_commits, f, indent=2)
            print(f"💾 Saved commit data to git_commits_for_import.json")
        
        print(f"\\n✅ PROOF OF CONCEPT COMPLETE!")
        print(f"📝 Would create {len(all_commits)} memory entries from git commit data")
        print(f"🔍 This would enhance pattern analysis with actual development activity")
        
        # Show potential analysis enhancements
        print(f"\\n🎯 ENHANCED ANALYSIS CAPABILITIES:")
        print(f"   - Memory-to-commit correlation analysis")
        print(f"   - Actual vs reported productivity patterns") 
        print(f"   - Multi-project development workflow analysis")
        print(f"   - Technology adoption and evolution tracking")
        print(f"   - Collaborative development pattern discovery")
    
    else:
        print("📭 No recent commits found in scanned repositories")

if __name__ == "__main__":
    main()