# Data Source Connection Guide for Claude Autonomous Analyst

## 🔌 CONNECTION DETAILS

### 1. PostgreSQL + pgvector
- **Host**: `pg-2c908149-claude-mem.e.aivencloud.com`
- **Port**: `24030`
- **Database**: `defaultdb`
- **Authentication**: Available in `.pgpass` file
- **SSL**: Required
- **Connection Method**: Use standard PostgreSQL tools or `mcp__claude-mem__*` memory tools

**Sample Query Approach**:
```sql
-- Find semantic similarities
SELECT memory_id, content, 
       embedding <-> (SELECT embedding FROM memories WHERE memory_id = 'target_id') as similarity
FROM memories 
ORDER BY similarity ASC 
LIMIT 10;
```

### 2. Neo4j
- **HTTP Interface**: `http://localhost:7474`
- **Bolt Interface**: `bolt://localhost:7687`
- **Username**: `neo4j`
- **Password**: `tempanalysis`
- **Database**: `neo4j`
- **Connection Method**: Use Neo4j Browser at http://localhost:7474 or Cypher queries

**Sample Cypher Query**:
```cypher
// Find workflow sequences
MATCH (m1:Memory)-[:FOLLOWS]->(m2:Memory)
WHERE m1.development_phase = 'planning' AND m2.development_phase = 'implementation'
RETURN m1.memory_id, m2.memory_id, m1.created_at, m2.created_at
ORDER BY m1.created_at
```

### 3. Elasticsearch
- **HTTP Interface**: `http://localhost:9200`
- **Index**: `memories`
- **Authentication**: None (disabled for local development)
- **Connection Method**: Direct HTTP requests or curl

**Sample Aggregation Query**:
```json
{
  "size": 0,
  "aggs": {
    "productivity_by_hour": {
      "terms": {
        "field": "hour_of_day",
        "size": 24
      },
      "aggs": {
        "sentiment_breakdown": {
          "terms": {"field": "sentiment"}
        },
        "avg_complexity": {
          "terms": {"field": "complexity"}
        }
      }
    }
  }
}
```

## 🛠️ CLAUDE TOOLS & ACCESS METHODS

### Recommended Access Approach:
1. **For PostgreSQL**: Use `mcp__claude-mem__*` tools for memory operations
2. **For Neo4j**: Use direct Cypher queries via web interface or Bash tool
3. **For Elasticsearch**: Use curl commands via Bash tool

### Sample Investigation Commands:

#### PostgreSQL/pgvector Investigation:
```bash
# Use memory tools to search semantically
mcp__claude-mem__search "problem resolution patterns"
mcp__claude-mem__search-enhanced "complexity management" --min-similarity 0.7
```

#### Neo4j Investigation:
```bash
# Execute Cypher queries
curl -X POST http://localhost:7474/db/data/cypher \
  -H "Content-Type: application/json" \
  -u neo4j:tempanalysis \
  -d '{"query": "MATCH (m:Memory) RETURN count(m) as total_memories"}'
```

#### Elasticsearch Investigation:
```bash
# Execute aggregation queries
curl -X POST "localhost:9200/memories/_search" \
  -H "Content-Type: application/json" \
  -d '{
    "size": 0,
    "aggs": {
      "development_phases": {
        "terms": {"field": "development_phase"}
      }
    }
  }'
```

## 🧪 PRE-INVESTIGATION VERIFICATION

Before starting analysis, verify all connections:

### Connection Test Commands:
```bash
# Test PostgreSQL (via memory tools)
mcp__claude-mem__memory-overview

# Test Neo4j
curl -u neo4j:tempanalysis http://localhost:7474/db/data/

# Test Elasticsearch  
curl localhost:9200/_cluster/health
curl localhost:9200/memories/_count
```

## 📊 DATA STRUCTURE REFERENCE

### Memory Data Schema (Common across all sources):
- **memory_id**: Unique identifier
- **content**: The actual memory content
- **content_type**: Type classification (code, decision, conversation, reference)
- **created_at**: Timestamp
- **sentiment**: positive/negative/neutral
- **complexity**: low/medium/high
- **tags**: Associated tags
- **development_phase**: planning/implementation/testing_debugging/general
- **technical_domains**: testing/frontend/backend/database/etc

### Neo4j Specific:
- **Relationships**: FOLLOWS, REFERENCES, RELATES_TO
- **Temporal sequences**: Memory chains over time
- **Causal paths**: Problem → Solution relationships

### Elasticsearch Specific:
- **Enriched fields**: hour_of_day, day_of_week, is_weekend
- **Problem indicators**: error_occurrence, performance_issue, etc
- **Solution indicators**: problem_resolution, optimization, etc

## 🚨 TROUBLESHOOTING

### If connections fail:
1. **Neo4j**: Check `docker ps` and restart with `./02-start-neo4j.sh /tmp`
2. **Elasticsearch**: Restart with `./18-lightweight-es-test.sh`
3. **PostgreSQL**: Verify `.pgpass` file and network connectivity

### Data verification:
- **PostgreSQL**: Should have ~250 memory records
- **Neo4j**: Should have Memory nodes with relationships
- **Elasticsearch**: Should have 250 documents in `memories` index

Use this guide to establish connections before beginning systematic pattern discovery!

## 🐛 BUG REPORTS & FEATURE REQUESTS

### When to File Bug Reports:
- Connection failures or timeouts
- Data inconsistencies between sources
- Query limitations that prevent analysis
- Performance issues with large datasets
- Missing data fields needed for investigation

### When to File Feature Requests:
- Additional data enrichment needs
- New analysis capabilities
- Visualization requirements
- Cross-source integration improvements
- Automation opportunities

### How to File via Memory System:
```bash
# Bug Report Example
mcp__claude-mem__store-dev-memory \
  --content "BUG: Neo4j relationship queries timeout for large temporal ranges. Affects workflow sequence analysis. Need query optimization or pagination." \
  --type "reference" \
  --tags '["bug-report", "neo4j", "performance", "investigation-blocker"]' \
  --status "identified"

# Feature Request Example  
mcp__claude-mem__store-dev-memory \
  --content "FEATURE REQUEST: Add sentiment change tracking over time in Elasticsearch. Would enable mood/productivity correlation analysis. Expected benefit: Better understanding of emotional patterns in development work." \
  --type "reference" \
  --tags '["feature-request", "elasticsearch", "sentiment-analysis", "enhancement"]' \
  --status "proposed"
```

### Investigation Impact Tracking:
When bugs/limitations block investigation:
1. **Document the blocked analysis** 
2. **File detailed bug report**
3. **Propose workaround if possible**
4. **Continue with alternative investigation paths**
5. **Track impact on overall pattern discovery**

This ensures continuous improvement of the analysis ecosystem!