#!/usr/bin/env python3
"""
23-git-commit-neo4j-import.py - Import git commits to Neo4j as GitCommit nodes
"""

import json
import os
from neo4j import GraphDatabase
from datetime import datetime
from typing import List, Dict

class GitCommitNeo4jImporter:
    def __init__(self):
        self.neo4j_uri = "bolt://localhost:7687"
        self.neo4j_user = "neo4j"
        self.neo4j_password = "tempanalysis"  # From 02-start-neo4j.sh
        
    def connect_to_neo4j(self):
        """Connect to Neo4j database"""
        try:
            driver = GraphDatabase.driver(
                self.neo4j_uri,
                auth=(self.neo4j_user, self.neo4j_password)
            )
            
            # Test connection
            with driver.session() as session:
                result = session.run("RETURN 'connected' as status")
                status = result.single()["status"]
                print(f"✅ Connected to Neo4j: {status}")
                
            return driver
            
        except Exception as e:
            print(f"❌ Neo4j connection failed: {e}")
            return None
    
    def clear_git_commits(self, driver):
        """Clear existing GitCommit nodes"""
        with driver.session() as session:
            result = session.run("MATCH (gc:GitCommit) DETACH DELETE gc RETURN COUNT(*) as deleted")
            deleted_count = result.single()["deleted"]
            print(f"🧹 Cleared {deleted_count} existing GitCommit nodes")
    
    def create_git_commit_constraints(self, driver):
        """Create constraints for GitCommit nodes"""
        constraints = [
            "CREATE CONSTRAINT git_commit_hash IF NOT EXISTS FOR (gc:GitCommit) REQUIRE gc.hash IS UNIQUE",
            "CREATE CONSTRAINT git_commit_memory_id IF NOT EXISTS FOR (gc:GitCommit) REQUIRE gc.memory_id IS UNIQUE"
        ]
        
        with driver.session() as session:
            for constraint in constraints:
                try:
                    session.run(constraint)
                    print(f"✅ Created constraint: {constraint.split()[-5]}")
                except Exception as e:
                    print(f"ℹ️ Constraint already exists or failed: {e}")
    
    def import_git_commits(self, git_commits_file: str):
        """Import git commits from JSON file to Neo4j"""
        
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
        
        # Connect to Neo4j
        driver = self.connect_to_neo4j()
        if not driver:
            return
        
        try:
            # Create constraints
            self.create_git_commit_constraints(driver)
            
            # Clear existing git commits
            self.clear_git_commits(driver)
            
            imported_count = 0
            
            with driver.session() as session:
                for commit in git_commits:
                    print(f"📝 Processing commit {commit['hash'][:8]}...")
                    
                    # Create memory_id for git commit (same as PostgreSQL)
                    memory_id = f"git_{commit['hash'][:16]}"
                    
                    # Create GitCommit node with conflict handling
                    create_commit_query = """
                    MERGE (gc:GitCommit {memory_id: $memory_id})
                    ON CREATE SET 
                        gc.hash = $hash,
                        gc.repository = $repository,
                        gc.commit_type = $commit_type,
                        gc.author = $author,
                        gc.message = $message,
                        gc.timestamp = datetime($timestamp),
                        gc.files_changed = $files_changed,
                        gc.lines_added = $lines_added,
                        gc.lines_deleted = $lines_deleted,
                        gc.primary_language = $primary_language,
                        gc.created_at = datetime()
                    """
                    
                    session.run(create_commit_query, {
                        'memory_id': memory_id,
                        'hash': commit['hash'],
                        'repository': commit['repository'],
                        'commit_type': commit['commit_type'],
                        'author': commit['author'],
                        'message': commit['message'],
                        'timestamp': commit['timestamp'],
                        'files_changed': commit['files_changed'],
                        'lines_added': commit['lines_added'],
                        'lines_deleted': commit['lines_deleted'],
                        'primary_language': commit['primary_language']
                    })
                    
                    imported_count += 1
                    print(f"✅ Imported GitCommit node {commit['hash'][:8]}")
                
                # Create relationships between GitCommits and repositories
                print("🔗 Creating repository relationships...")
                repo_relationship_query = """
                MATCH (gc:GitCommit)
                MERGE (r:Repository {name: gc.repository})
                MERGE (gc)-[:COMMITTED_TO]->(r)
                """
                session.run(repo_relationship_query)
                
                # Create relationships between commits by author
                print("🔗 Creating author relationships...")
                author_relationship_query = """
                MATCH (gc:GitCommit)
                MERGE (a:Author {name: gc.author})
                MERGE (a)-[:AUTHORED]->(gc)
                """
                session.run(author_relationship_query)
                
                # Create temporal relationships (commits within 1 day)
                print("🔗 Creating temporal relationships...")
                temporal_relationship_query = """
                MATCH (gc1:GitCommit), (gc2:GitCommit)
                WHERE gc1.hash <> gc2.hash
                AND duration.between(gc1.timestamp, gc2.timestamp).days <= 1
                AND gc1.timestamp < gc2.timestamp
                MERGE (gc1)-[:FOLLOWED_BY]->(gc2)
                """
                session.run(temporal_relationship_query)
                
                print(f"\n🎉 SUCCESS: Imported {imported_count} GitCommit nodes to Neo4j!")
                print(f"🔍 Use queries like: MATCH (gc:GitCommit)-[:COMMITTED_TO]->(r:Repository) RETURN gc, r")
                
        except Exception as e:
            print(f"❌ Import failed: {e}")
            import traceback
            traceback.print_exc()
            
        finally:
            driver.close()
    
    def test_git_commit_queries(self):
        """Test GitCommit node queries"""
        driver = self.connect_to_neo4j()
        if not driver:
            return
        
        try:
            with driver.session() as session:
                print("\n🔍 TESTING GIT COMMIT QUERIES:")
                print("=" * 50)
                
                # Test 1: Count nodes by type
                count_query = """
                MATCH (gc:GitCommit)
                RETURN 
                    COUNT(gc) as total_commits,
                    COUNT(DISTINCT gc.repository) as repositories,
                    COUNT(DISTINCT gc.author) as authors
                """
                
                result = session.run(count_query)
                record = result.single()
                print(f"📊 Total GitCommits: {record['total_commits']}")
                print(f"📊 Repositories: {record['repositories']}")
                print(f"📊 Authors: {record['authors']}")
                
                # Test 2: Repository activity
                repo_activity_query = """
                MATCH (gc:GitCommit)-[:COMMITTED_TO]->(r:Repository)
                RETURN 
                    r.name as repository,
                    COUNT(gc) as commits,
                    SUM(gc.lines_added) as total_added,
                    SUM(gc.lines_deleted) as total_deleted
                ORDER BY commits DESC
                """
                
                result = session.run(repo_activity_query)
                print("\n📈 Repository Activity:")
                for record in result:
                    print(f"  🗂️  {record['repository']}: {record['commits']} commits, +{record['total_added']}/-{record['total_deleted']} lines")
                
                # Test 3: Temporal relationships
                temporal_query = """
                MATCH (gc1:GitCommit)-[:FOLLOWED_BY]->(gc2:GitCommit)
                RETURN 
                    gc1.hash as first_commit,
                    gc2.hash as second_commit,
                    duration.between(gc1.timestamp, gc2.timestamp) as time_gap
                LIMIT 5
                """
                
                result = session.run(temporal_query)
                print("\n⏰ Temporal Relationships:")
                for record in result:
                    print(f"  🔗 {record['first_commit'][:8]} → {record['second_commit'][:8]} (gap: {record['time_gap']})")
                
        except Exception as e:
            print(f"❌ Query test failed: {e}")
            
        finally:
            driver.close()

def main():
    """Main git commit Neo4j import function"""
    
    print("🔄 GIT COMMIT NEO4J IMPORT")
    print("=" * 40)
    
    importer = GitCommitNeo4jImporter()
    
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
    print("1. Run 24-git-commit-elasticsearch-import.py to add to ES index")
    print("2. Use enhanced Claude analysis with git correlation capabilities")

if __name__ == "__main__":
    main()