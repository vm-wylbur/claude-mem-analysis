#!/usr/bin/env python3
"""
25-unified-git-analysis.py - Unified cross-source git commit analysis
Correlates git commits across PostgreSQL, Neo4j, and Elasticsearch
"""

import json
import os
import psycopg2
from neo4j import GraphDatabase
from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
from typing import List, Dict, Any
import toml

class UnifiedGitAnalysis:
    def __init__(self):
        # Load database config
        config_file = os.path.expanduser("~/.config/claude-mem/claude-mem.toml")
        self.db_config = self.load_db_config(config_file)
        
        # Connection details
        self.neo4j_uri = "bolt://localhost:7687"
        self.neo4j_user = "neo4j"
        self.neo4j_password = "tempanalysis"
        self.es_host = "localhost:9200"
        self.index_name = "memory_analysis"
        
    def load_db_config(self, config_file: str) -> Dict:
        """Load PostgreSQL connection config from TOML file"""
        try:
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
            return {}
    
    def analyze_postgresql_patterns(self):
        """Analyze git commits in PostgreSQL with semantic similarity"""
        print("🔍 POSTGRESQL ANALYSIS")
        print("=" * 30)
        
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
            
            # Pattern 1: Repository productivity analysis
            productivity_query = """
            SELECT 
                repository_name,
                COUNT(*) as commit_count,
                SUM(lines_added) as total_added,
                SUM(lines_deleted) as total_deleted,
                AVG(files_changed) as avg_files_per_commit,
                string_agg(DISTINCT commit_type, ', ') as commit_types
            FROM git_commits
            GROUP BY repository_name
            ORDER BY total_added + total_deleted DESC;
            """
            
            cursor.execute(productivity_query)
            results = cursor.fetchall()
            
            print("📊 Repository Productivity (PostgreSQL):")
            for row in results:
                repo, commits, added, deleted, avg_files, types = row
                total_changes = added + deleted
                print(f"  🗂️  {repo}: {commits} commits, {total_changes} total changes")
                print(f"      📈 +{added}/-{deleted} lines, ~{avg_files:.1f} files/commit")
                print(f"      🏷️  Types: {types}")
                print()
            
            # Pattern 2: Author coding patterns
            author_query = """
            SELECT 
                author_name,
                COUNT(*) as commits,
                string_agg(DISTINCT primary_language, ', ') as languages,
                string_agg(DISTINCT repository_name, ', ') as repositories,
                AVG(lines_added::float / NULLIF(files_changed, 0)) as avg_lines_per_file
            FROM git_commits
            GROUP BY author_name
            ORDER BY commits DESC;
            """
            
            cursor.execute(author_query)
            results = cursor.fetchall()
            
            print("👨‍💻 Author Coding Patterns:")
            for row in results:
                author, commits, langs, repos, avg_lines = row
                avg_lines_str = f"{avg_lines:.1f}" if avg_lines else "N/A"
                print(f"  👤 {author}: {commits} commits")
                print(f"      💻 Languages: {langs}")
                print(f"      📁 Repositories: {repos}")
                print(f"      📝 Avg lines/file: {avg_lines_str}")
                print()
            
            # Pattern 3: Semantic similarity with memories (if any exist)
            similarity_query = """
            SELECT 
                gc.repository_name,
                gc.commit_type,
                LEFT(gc.content, 100) as git_content,
                m.memory_id,
                LEFT(m.content, 100) as memory_content,
                (gc.embedding <-> m.embedding) as similarity_distance
            FROM git_commits gc, memories m
            WHERE gc.embedding <-> m.embedding < 0.5
            ORDER BY similarity_distance ASC
            LIMIT 5;
            """
            
            cursor.execute(similarity_query)
            results = cursor.fetchall()
            
            if results:
                print("🔗 Git-Memory Semantic Similarities:")
                for row in results:
                    repo, commit_type, git_content, mem_id, mem_content, distance = row
                    similarity = 1 - distance
                    print(f"  🎯 Similarity: {similarity:.3f}")
                    print(f"      🔧 Git ({repo}): {git_content}...")
                    print(f"      📝 Memory ({mem_id}): {mem_content}...")
                    print()
            else:
                print("ℹ️ No high semantic similarities found between git commits and memories")
                print()
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            print(f"❌ PostgreSQL analysis failed: {e}")
            print()
    
    def analyze_neo4j_relationships(self):
        """Analyze git commit relationships in Neo4j"""
        print("🔍 NEO4J RELATIONSHIP ANALYSIS")
        print("=" * 30)
        
        try:
            driver = GraphDatabase.driver(
                self.neo4j_uri,
                auth=(self.neo4j_user, self.neo4j_password)
            )
            
            with driver.session() as session:
                # Pattern 1: Developer collaboration patterns
                collab_query = """
                MATCH (a1:Author)-[:AUTHORED]->(gc1:GitCommit)-[:COMMITTED_TO]->(r:Repository)<-[:COMMITTED_TO]-(gc2:GitCommit)<-[:AUTHORED]-(a2:Author)
                WHERE a1.name <> a2.name
                RETURN 
                    a1.name as author1,
                    a2.name as author2,
                    r.name as repository,
                    COUNT(*) as shared_repo_commits
                ORDER BY shared_repo_commits DESC
                """
                
                result = session.run(collab_query)
                records = list(result)
                
                if records:
                    print("🤝 Developer Collaboration Patterns:")
                    for record in records:
                        print(f"  👥 {record['author1']} & {record['author2']}")
                        print(f"      📁 Repository: {record['repository']}")
                        print(f"      🔢 Shared commits: {record['shared_repo_commits']}")
                        print()
                else:
                    print("ℹ️ No multi-developer repositories found")
                    print()
                
                # Pattern 2: Temporal commit chains
                temporal_query = """
                MATCH (gc1:GitCommit)-[:FOLLOWED_BY]->(gc2:GitCommit)
                RETURN 
                    gc1.repository as repo,
                    gc1.commit_type as first_type,
                    gc2.commit_type as second_type,
                    duration.between(gc1.timestamp, gc2.timestamp) as time_gap,
                    gc1.hash as first_hash,
                    gc2.hash as second_hash
                ORDER BY time_gap ASC
                LIMIT 5
                """
                
                result = session.run(temporal_query)
                records = list(result)
                
                if records:
                    print("⏰ Temporal Commit Chains:")
                    for record in records:
                        gap = record['time_gap']
                        print(f"  🔗 {record['repo']}: {record['first_type']} → {record['second_type']}")
                        print(f"      ⏱️  Gap: {gap}")
                        print(f"      🔧 {record['first_hash'][:8]} → {record['second_hash'][:8]}")
                        print()
                else:
                    print("ℹ️ No temporal relationships found")
                    print()
                
                # Pattern 3: Repository development patterns
                dev_pattern_query = """
                MATCH (gc:GitCommit)-[:COMMITTED_TO]->(r:Repository)
                RETURN 
                    r.name as repository,
                    collect(DISTINCT gc.commit_type) as commit_types,
                    collect(DISTINCT gc.primary_language) as languages,
                    COUNT(gc) as total_commits,
                    SUM(gc.lines_added) as total_added,
                    SUM(gc.lines_deleted) as total_deleted
                ORDER BY total_commits DESC
                """
                
                result = session.run(dev_pattern_query)
                records = list(result)
                
                print("🏗️ Repository Development Patterns:")
                for record in records:
                    repo = record['repository']
                    types = ", ".join(record['commit_types'])
                    langs = ", ".join(record['languages'])
                    commits = record['total_commits']
                    added = record['total_added']
                    deleted = record['total_deleted']
                    
                    print(f"  📁 {repo}: {commits} commits")
                    print(f"      🏷️  Types: {types}")
                    print(f"      💻 Languages: {langs}")
                    print(f"      📊 Changes: +{added}/-{deleted}")
                    print()
            
            driver.close()
            
        except Exception as e:
            print(f"❌ Neo4j analysis failed: {e}")
            print()
    
    def analyze_elasticsearch_aggregations(self):
        """Analyze git commits using Elasticsearch aggregations"""
        print("🔍 ELASTICSEARCH AGGREGATION ANALYSIS")
        print("=" * 30)
        
        try:
            es = Elasticsearch([f"http://{self.es_host}"])
            
            if not es.ping():
                print("❌ Cannot connect to Elasticsearch")
                return
            
            # Pattern 1: Time-based commit activity
            time_agg_query = {
                "size": 0,
                "query": {
                    "term": {"content_type": "git_commit"}
                },
                "aggs": {
                    "commits_over_time": {
                        "date_histogram": {
                            "field": "created_at",
                            "calendar_interval": "hour"
                        },
                        "aggs": {
                            "commit_types": {
                                "terms": {"field": "commit_type"}
                            }
                        }
                    }
                }
            }
            
            result = es.search(index=self.index_name, body=time_agg_query)
            
            print("📅 Time-based Commit Activity:")
            for bucket in result['aggregations']['commits_over_time']['buckets']:
                timestamp = bucket['key_as_string']
                count = bucket['doc_count']
                if count > 0:  # Only show periods with activity
                    print(f"  ⏰ {timestamp}: {count} commits")
                    for type_bucket in bucket['commit_types']['buckets']:
                        type_name = type_bucket['key']
                        type_count = type_bucket['doc_count']
                        print(f"      🏷️  {type_name}: {type_count}")
                    print()
            
            # Pattern 2: Language and repository correlation
            lang_repo_query = {
                "size": 0,
                "query": {
                    "term": {"content_type": "git_commit"}
                },
                "aggs": {
                    "languages": {
                        "terms": {"field": "primary_language"},
                        "aggs": {
                            "repositories": {
                                "terms": {"field": "repository_name"}
                            },
                            "avg_lines_added": {
                                "avg": {"field": "lines_added"}
                            }
                        }
                    }
                }
            }
            
            result = es.search(index=self.index_name, body=lang_repo_query)
            
            print("💻 Language-Repository Correlations:")
            for bucket in result['aggregations']['languages']['buckets']:
                lang = bucket['key']
                count = bucket['doc_count']
                avg_lines = bucket['avg_lines_added']['value']
                
                print(f"  📝 {lang}: {count} commits, avg {avg_lines:.1f} lines added")
                
                for repo_bucket in bucket['repositories']['buckets']:
                    repo = repo_bucket['key']
                    repo_count = repo_bucket['doc_count']
                    print(f"      📁 {repo}: {repo_count} commits")
                print()
            
            # Pattern 3: Text search patterns in commit messages
            search_terms = ["fix", "add", "update", "refactor", "bug"]
            
            print("🔍 Commit Message Text Analysis:")
            for term in search_terms:
                search_query = {
                    "query": {
                        "bool": {
                            "must": [
                                {"term": {"content_type": "git_commit"}},
                                {"match": {"commit_message": term}}
                            ]
                        }
                    },
                    "size": 0
                }
                
                result = es.search(index=self.index_name, body=search_query)
                count = result['hits']['total']['value']
                print(f"  🔍 '{term}': {count} commits")
            print()
            
        except Exception as e:
            print(f"❌ Elasticsearch analysis failed: {e}")
            print()
    
    def generate_cross_source_insights(self):
        """Generate insights by correlating data across all three sources"""
        print("🎯 CROSS-SOURCE CORRELATION INSIGHTS")
        print("=" * 40)
        
        insights = []
        
        # Collect basic statistics from each source
        pg_stats = self.get_postgresql_stats()
        neo4j_stats = self.get_neo4j_stats()
        es_stats = self.get_elasticsearch_stats()
        
        print("📊 Data Consistency Check:")
        print(f"  🔵 PostgreSQL: {pg_stats.get('total_commits', 0)} git commits")
        print(f"  🟠 Neo4j: {neo4j_stats.get('total_commits', 0)} GitCommit nodes")
        print(f"  🟢 Elasticsearch: {es_stats.get('total_commits', 0)} git_commit documents")
        print()
        
        # Generate insights
        if pg_stats.get('total_commits', 0) > 0:
            insights.append(f"✅ Git integration successful: {pg_stats['total_commits']} commits across {pg_stats.get('repositories', 0)} repositories")
            
            if pg_stats.get('most_productive_repo'):
                insights.append(f"🏆 Most productive repository: {pg_stats['most_productive_repo']} ({pg_stats.get('max_changes', 0)} total changes)")
            
            if pg_stats.get('primary_language'):
                insights.append(f"💻 Primary development language: {pg_stats['primary_language']} ({pg_stats.get('lang_commits', 0)} commits)")
        
        if neo4j_stats.get('has_temporal_relationships'):
            insights.append(f"⏰ Temporal development patterns identified with {neo4j_stats.get('temporal_count', 0)} commit sequences")
        
        if es_stats.get('searchable_content'):
            insights.append(f"🔍 Full-text search enabled across {es_stats.get('total_commits', 0)} commit messages and content")
        
        print("💡 Key Insights:")
        for i, insight in enumerate(insights, 1):
            print(f"  {i}. {insight}")
        print()
        
        print("🎯 Recommended Next Steps:")
        print("  1. Use enhanced Claude analysis with git correlation capabilities")
        print("  2. Explore semantic similarities between memories and recent code changes")
        print("  3. Identify development workflow optimization opportunities")
        print("  4. Monitor temporal patterns for productivity insights")
        print()
    
    def get_postgresql_stats(self) -> Dict[str, Any]:
        """Get summary statistics from PostgreSQL"""
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
            
            # Basic counts
            cursor.execute("SELECT COUNT(*), COUNT(DISTINCT repository_name) FROM git_commits")
            total_commits, repositories = cursor.fetchone()
            
            # Most productive repo
            cursor.execute("""
                SELECT repository_name, SUM(lines_added + lines_deleted) as total_changes
                FROM git_commits 
                GROUP BY repository_name 
                ORDER BY total_changes DESC 
                LIMIT 1
            """)
            result = cursor.fetchone()
            most_productive_repo, max_changes = result if result else (None, 0)
            
            # Primary language
            cursor.execute("""
                SELECT primary_language, COUNT(*) as commits
                FROM git_commits 
                GROUP BY primary_language 
                ORDER BY commits DESC 
                LIMIT 1
            """)
            result = cursor.fetchone()
            primary_language, lang_commits = result if result else (None, 0)
            
            cursor.close()
            conn.close()
            
            return {
                'total_commits': total_commits,
                'repositories': repositories,
                'most_productive_repo': most_productive_repo,
                'max_changes': max_changes,
                'primary_language': primary_language,
                'lang_commits': lang_commits
            }
            
        except Exception as e:
            print(f"⚠️ PostgreSQL stats error: {e}")
            return {}
    
    def get_neo4j_stats(self) -> Dict[str, Any]:
        """Get summary statistics from Neo4j"""
        try:
            driver = GraphDatabase.driver(
                self.neo4j_uri,
                auth=(self.neo4j_user, self.neo4j_password)
            )
            
            with driver.session() as session:
                # Basic counts
                result = session.run("MATCH (gc:GitCommit) RETURN COUNT(gc) as total")
                total_commits = result.single()['total']
                
                # Temporal relationships
                result = session.run("MATCH ()-[:FOLLOWED_BY]->() RETURN COUNT(*) as temporal_count")
                temporal_count = result.single()['temporal_count']
                
            driver.close()
            
            return {
                'total_commits': total_commits,
                'has_temporal_relationships': temporal_count > 0,
                'temporal_count': temporal_count
            }
            
        except Exception as e:
            print(f"⚠️ Neo4j stats error: {e}")
            return {}
    
    def get_elasticsearch_stats(self) -> Dict[str, Any]:
        """Get summary statistics from Elasticsearch"""
        try:
            es = Elasticsearch([f"http://{self.es_host}"])
            
            if not es.ping():
                return {}
            
            # Count git commits
            count_query = {
                "query": {
                    "term": {"content_type": "git_commit"}
                }
            }
            
            result = es.count(index=self.index_name, body=count_query)
            total_commits = result['count']
            
            return {
                'total_commits': total_commits,
                'searchable_content': total_commits > 0
            }
            
        except Exception as e:
            print(f"⚠️ Elasticsearch stats error: {e}")
            return {}

def main():
    """Main unified analysis function"""
    
    print("🔄 UNIFIED GIT COMMIT ANALYSIS")
    print("=" * 50)
    print("Analyzing git commits across PostgreSQL, Neo4j, and Elasticsearch")
    print()
    
    analyzer = UnifiedGitAnalysis()
    
    # Run analysis for each data source
    analyzer.analyze_postgresql_patterns()
    analyzer.analyze_neo4j_relationships()
    analyzer.analyze_elasticsearch_aggregations()
    
    # Generate cross-source insights
    analyzer.generate_cross_source_insights()
    
    print("🎉 Unified analysis complete!")
    print("💡 Ready for enhanced Claude investigation with git correlation capabilities")

if __name__ == "__main__":
    main()