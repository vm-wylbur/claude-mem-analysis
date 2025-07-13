#!/usr/bin/env python3
"""
postgres_importer.py - Import git commits to PostgreSQL with embeddings
"""

import json
import psycopg2
import requests
from datetime import datetime
from typing import List, Dict
import os

class GitCommitPostgresImporter:
    def __init__(self, config_file: str = None):
        if config_file is None:
            config_file = os.path.expanduser("~/.config/claude-mem/claude-mem.toml")
        self.db_config = self.load_db_config(config_file)
        self.embedding_model_url = "http://localhost:11434/api/embeddings"
        
    def load_db_config(self, config_file: str) -> Dict:
        """Load PostgreSQL connection config from TOML file"""
        try:
            import toml
            with open(config_file, 'r') as f:
                config = toml.load(f)
                
            pg_config = config['database']['postgresql']
            return {
                'host': pg_config['hosts'][0],
                'port': pg_config['port'], 
                'database': pg_config['database'],
                'user': pg_config['user'],
                'password': pg_config['password']
            }
        except Exception as e:
            print(f"❌ Error loading DB config: {e}")
            print("Please ensure ~/.config/claude-mem/claude-mem.toml exists with database configuration")
            return {}
    
    def get_embedding(self, text: str) -> List[float]:
        """Generate embedding for text using Ollama"""
        try:
            payload = {
                "model": "nomic-embed-text",
                "prompt": text
            }
            
            response = requests.post(self.embedding_model_url, json=payload, timeout=30)
            if response.status_code == 200:
                return response.json()['embedding']
            else:
                print(f"⚠️ Embedding request failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"⚠️ Error generating embedding: {e}")
            return None
    
    def create_table(self):
        """Create git_commits table if it doesn't exist"""
        try:
            conn = psycopg2.connect(
                host=self.db_config['host'],
                port=self.db_config['port'],
                database=self.db_config['database'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                sslmode='require'
            )
            
            cursor = conn.cursor()
            
            # Create table with vector column for embeddings
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS git_commits (
                memory_id VARCHAR(16) PRIMARY KEY,
                hash VARCHAR(40) NOT NULL,
                author_name VARCHAR(255),
                author_email VARCHAR(255),
                timestamp TIMESTAMPTZ,
                commit_message TEXT,
                repository_name VARCHAR(255),
                lines_added INTEGER DEFAULT 0,
                lines_deleted INTEGER DEFAULT 0,
                files_changed INTEGER DEFAULT 0,
                commit_type VARCHAR(50),
                primary_language VARCHAR(50),
                content TEXT,
                embedding VECTOR(768)
            );
            """
            
            cursor.execute(create_table_sql)
            
            # Create index on memory_id for uniqueness
            cursor.execute("""
                CREATE UNIQUE INDEX IF NOT EXISTS git_commits_memory_id_key 
                ON git_commits(memory_id);
            """)
            
            # Create index on timestamp for temporal queries
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS git_commits_timestamp_idx 
                ON git_commits(timestamp);
            """)
            
            # Create index on repository for filtering
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS git_commits_repository_idx 
                ON git_commits(repository_name);
            """)
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print("✅ git_commits table created successfully")
            
        except Exception as e:
            print(f"❌ Error creating table: {e}")
    
    def import_commits(self, json_file: str = "git_commits_for_import.json"):
        """Import git commits from JSON file to PostgreSQL"""
        
        if not self.db_config:
            print("❌ No database configuration available")
            return
            
        try:
            # Load commits from JSON
            with open(json_file, 'r') as f:
                commits = json.load(f)
            
            print(f"📊 Loaded {len(commits)} commits from {json_file}")
            
            # Connect to PostgreSQL
            conn = psycopg2.connect(
                host=self.db_config['host'],
                port=self.db_config['port'],
                database=self.db_config['database'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                sslmode='require'
            )
            
            cursor = conn.cursor()
            
            imported_count = 0
            skipped_count = 0
            
            for commit in commits:
                try:
                    # Generate content for embedding
                    content = f"{commit['commit_message']} {commit['repository']} {commit.get('primary_language', '')}"
                    
                    # Generate embedding
                    embedding = self.get_embedding(content)
                    if embedding is None:
                        print(f"⚠️ Skipping commit {commit['hash'][:8]} - no embedding")
                        skipped_count += 1
                        continue
                    
                    # Convert timestamp
                    timestamp = datetime.fromisoformat(commit['timestamp'].replace('Z', '+00:00'))
                    
                    # Insert commit with conflict handling
                    insert_sql = """
                    INSERT INTO git_commits (
                        memory_id, hash, author_name, author_email, timestamp,
                        commit_message, repository_name, lines_added, lines_deleted,
                        files_changed, commit_type, primary_language, content, embedding
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    ) ON CONFLICT (memory_id) DO NOTHING;
                    """
                    
                    cursor.execute(insert_sql, (
                        commit['memory_id'],
                        commit['hash'],
                        commit['author'],
                        commit.get('author_email', ''),
                        timestamp,
                        commit['commit_message'],
                        commit['repository'],
                        commit.get('lines_added', 0),
                        commit.get('lines_deleted', 0),
                        commit.get('files_changed', 0),
                        commit.get('commit_type', 'unknown'),
                        commit.get('primary_language', 'unknown'),
                        content,
                        embedding
                    ))
                    
                    imported_count += 1
                    
                    if imported_count % 10 == 0:
                        print(f"📈 Imported {imported_count} commits...")
                    
                except Exception as e:
                    print(f"⚠️ Error importing commit {commit.get('hash', 'unknown')[:8]}: {e}")
                    skipped_count += 1
                    continue
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"\n🎉 Import complete!")
            print(f"   📈 Imported: {imported_count} commits")
            print(f"   ⏭️  Skipped: {skipped_count} commits")
            print(f"   💾 Total in database: {imported_count} new commits")
            
        except Exception as e:
            print(f"❌ Import failed: {e}")

def main():
    """Main import function"""
    print("🔄 POSTGRESQL GIT COMMIT IMPORT")
    print("=" * 40)
    
    importer = GitCommitPostgresImporter()
    
    # Create table if needed
    importer.create_table()
    
    # Import commits
    importer.import_commits()

if __name__ == "__main__":
    main()