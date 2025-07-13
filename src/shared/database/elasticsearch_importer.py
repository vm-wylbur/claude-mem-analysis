#!/usr/bin/env python3
"""
24-git-commit-elasticsearch-import.py - Import git commits to Elasticsearch
"""

import json
import os
from elasticsearch import Elasticsearch
from datetime import datetime
from typing import List, Dict

class GitCommitElasticsearchImporter:
    def __init__(self):
        self.es_host = "localhost:9200"
        self.index_name = "memory_analysis"
        self.git_commit_type = "git_commit"
        
    def connect_to_elasticsearch(self):
        """Connect to Elasticsearch"""
        try:
            es = Elasticsearch([f"http://{self.es_host}"])
            
            # Test connection
            if es.ping():
                info = es.info()
                print(f"✅ Connected to Elasticsearch: {info['version']['number']}")
                return es
            else:
                print("❌ Elasticsearch connection failed")
                return None
                
        except Exception as e:
            print(f"❌ Elasticsearch connection failed: {e}")
            return None
    
    def create_git_commit_mapping(self, es):
        """Create mapping for git_commit type in existing index"""
        
        # Check if index exists
        if not es.indices.exists(index=self.index_name):
            print(f"❌ Index {self.index_name} does not exist")
            print("💡 Run 19-fixed-es-import.py first to create the index")
            return False
        
        # Update mapping to include git_commit fields
        git_commit_mapping = {
            "properties": {
                "content_type": {"type": "keyword"},
                "content": {"type": "text", "analyzer": "standard"},
                "memory_id": {"type": "keyword"},
                "created_at": {"type": "date"},
                "tags": {"type": "keyword"},
                "sentiment": {"type": "keyword"},
                "complexity": {"type": "keyword"},
                
                # Git-specific fields
                "commit_hash": {"type": "keyword"},
                "repository_name": {"type": "keyword"},
                "commit_type": {"type": "keyword"},
                "author_name": {"type": "keyword"},
                "files_changed": {"type": "integer"},
                "lines_added": {"type": "integer"},
                "lines_deleted": {"type": "integer"},
                "primary_language": {"type": "keyword"},
                "commit_message": {"type": "text", "analyzer": "standard"}
            }
        }
        
        try:
            # Update mapping (will merge with existing mapping) - ES 7.x format
            es.indices.put_mapping(
                index=self.index_name,
                body=git_commit_mapping
            )
            print(f"✅ Updated mapping for git_commit type in {self.index_name}")
            return True
            
        except Exception as e:
            print(f"⚠️ Mapping update warning: {e}")
            return True  # Continue anyway, mapping might already exist
    
    def clear_git_commits(self, es):
        """Clear existing git_commit documents"""
        try:
            delete_query = {
                "query": {
                    "term": {
                        "content_type": self.git_commit_type
                    }
                }
            }
            
            result = es.delete_by_query(
                index=self.index_name,
                body=delete_query
            )
            
            deleted_count = result.get('deleted', 0)
            print(f"🧹 Cleared {deleted_count} existing git_commit documents")
            
        except Exception as e:
            print(f"⚠️ Clear warning: {e}")
    
    def import_git_commits(self, git_commits_file: str):
        """Import git commits from JSON file to Elasticsearch"""
        
        # Load git commits data
        try:
            with open(git_commits_file, 'r') as f:
                git_commits = json.load(f)
        except Exception as e:
            print(f"❌ Error loading git commits file: {e}")
            return
        
        if not git_commits:
            print("❌ No git commits to import")
            return
        
        # Connect to Elasticsearch
        es = self.connect_to_elasticsearch()
        if not es:
            return
        
        try:
            # Create/update mapping
            if not self.create_git_commit_mapping(es):
                return
            
            # Clear existing git commits
            self.clear_git_commits(es)
            
            imported_count = 0
            
            for commit in git_commits:
                print(f"📝 Processing commit {commit['hash'][:8]}...")
                
                # Create memory_id for git commit (same as PostgreSQL/Neo4j)
                memory_id = f"git_{commit['hash'][:16]}"
                
                # Create comprehensive content for search
                commit_content = f"""Git Commit: {commit['repository']}

Type: {commit['commit_type']}
Message: {commit['message']}
Repository: {commit['repository']}
Language: {commit['primary_language']}

Changes:
- Files: {commit['files_changed']}
- Added: {commit['lines_added']} lines
- Deleted: {commit['lines_deleted']} lines

Author: {commit['author']}
Timestamp: {commit['timestamp']}

Context: Development activity captured from git commit history for pattern analysis."""
                
                # Prepare tags
                tags = [
                    "git-commit",
                    commit['repository'],
                    commit['commit_type'],
                    f"language-{commit['primary_language']}"
                ]
                
                # Create document
                doc = {
                    "content_type": self.git_commit_type,
                    "content": commit_content,
                    "memory_id": memory_id,
                    "created_at": commit['timestamp'],
                    "tags": tags,
                    "sentiment": "neutral",
                    "complexity": "medium" if commit['commit_type'] == 'feature' else "low",
                    
                    # Git-specific fields
                    "commit_hash": commit['hash'],
                    "repository_name": commit['repository'],
                    "commit_type": commit['commit_type'],
                    "author_name": commit['author'],
                    "files_changed": commit['files_changed'],
                    "lines_added": commit['lines_added'],
                    "lines_deleted": commit['lines_deleted'],
                    "primary_language": commit['primary_language'],
                    "commit_message": commit['message']
                }
                
                # Index document
                es.index(
                    index=self.index_name,
                    id=memory_id,
                    body=doc
                )
                
                imported_count += 1
                print(f"✅ Imported git_commit document {commit['hash'][:8]}")
            
            # Refresh index to make documents searchable
            es.indices.refresh(index=self.index_name)
            
            print(f"\n🎉 SUCCESS: Imported {imported_count} git_commit documents to Elasticsearch!")
            print(f"🔍 Use queries like: GET {self.index_name}/_search?q=content_type:git_commit")
            
        except Exception as e:
            print(f"❌ Import failed: {e}")
            import traceback
            traceback.print_exc()
    
    def test_git_commit_queries(self):
        """Test git_commit document queries"""
        es = self.connect_to_elasticsearch()
        if not es:
            return
        
        try:
            print("\n🔍 TESTING GIT COMMIT QUERIES:")
            print("=" * 50)
            
            # Test 1: Count documents by type
            count_query = {
                "query": {
                    "term": {
                        "content_type": self.git_commit_type
                    }
                }
            }
            
            result = es.count(index=self.index_name, body=count_query)
            total_commits = result['count']
            print(f"📊 Total git_commit documents: {total_commits}")
            
            # Test 2: Repository aggregation
            repo_agg_query = {
                "size": 0,
                "query": {
                    "term": {
                        "content_type": self.git_commit_type
                    }
                },
                "aggs": {
                    "repositories": {
                        "terms": {
                            "field": "repository_name",
                            "size": 10
                        },
                        "aggs": {
                            "total_lines_added": {
                                "sum": {"field": "lines_added"}
                            },
                            "total_lines_deleted": {
                                "sum": {"field": "lines_deleted"}
                            }
                        }
                    }
                }
            }
            
            result = es.search(index=self.index_name, body=repo_agg_query)
            
            print("\n📈 Repository Activity (Elasticsearch):")
            for bucket in result['aggregations']['repositories']['buckets']:
                repo = bucket['key']
                count = bucket['doc_count']
                added = int(bucket['total_lines_added']['value'])
                deleted = int(bucket['total_lines_deleted']['value'])
                print(f"  🗂️  {repo}: {count} commits, +{added}/-{deleted} lines")
            
            # Test 3: Text search across commit messages
            search_query = {
                "query": {
                    "bool": {
                        "must": [
                            {"term": {"content_type": self.git_commit_type}},
                            {"match": {"commit_message": "fix"}}
                        ]
                    }
                },
                "_source": ["commit_hash", "repository_name", "commit_message"],
                "size": 5
            }
            
            result = es.search(index=self.index_name, body=search_query)
            
            if result['hits']['total']['value'] > 0:
                print(f"\n🔍 Commits containing 'fix':")
                for hit in result['hits']['hits']:
                    source = hit['_source']
                    print(f"  🔧 {source['commit_hash'][:8]} ({source['repository_name']}): {source['commit_message'][:50]}...")
            else:
                print("\n🔍 No commits found containing 'fix'")
            
            # Test 4: Language distribution
            lang_agg_query = {
                "size": 0,
                "query": {
                    "term": {
                        "content_type": self.git_commit_type
                    }
                },
                "aggs": {
                    "languages": {
                        "terms": {
                            "field": "primary_language",
                            "size": 10
                        }
                    }
                }
            }
            
            result = es.search(index=self.index_name, body=lang_agg_query)
            
            print("\n💻 Language Distribution:")
            for bucket in result['aggregations']['languages']['buckets']:
                lang = bucket['key']
                count = bucket['doc_count']
                print(f"  📝 {lang}: {count} commits")
            
        except Exception as e:
            print(f"❌ Query test failed: {e}")

def main():
    """Main git commit Elasticsearch import function"""
    
    print("🔄 GIT COMMIT ELASTICSEARCH IMPORT")
    print("=" * 40)
    
    importer = GitCommitElasticsearchImporter()
    
    # Import git commits
    git_commits_file = "git_commits_for_import.json"
    if not os.path.exists(git_commits_file):
        print(f"❌ Git commits file not found: {git_commits_file}")
        print("💡 Run 21-git-commit-scanner.py first to generate commit data")
        return
    
    importer.import_git_commits(git_commits_file)
    
    # Test queries
    importer.test_git_commit_queries()
    
    print("\n🎯 NEXT STEPS:")
    print("1. Run 25-unified-git-analysis.py for cross-source correlation")
    print("2. Use enhanced Claude analysis with git correlation capabilities")

if __name__ == "__main__":
    main()