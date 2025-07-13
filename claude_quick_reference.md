# Claude Autonomous Analyst - Quick Reference Card

## 🚀 **GETTING STARTED**
**Starting Document**: `claude_investigation_session_foundation_session_1752416604.md`

## 🎯 **SPECIAL FOCUS AREAS**
Your investigation should prioritize recommendations for:
- **Development Workflows**: Coding, testing, deployment optimizations
- **QA Processes**: Quality assurance, review cycles, bug prevention
- **Human-AI Interaction**: AI-assisted development best practices
- **AI-AI Interaction**: Multi-agent workflows and system coordination

## 🔌 **CONNECTION COMMANDS**
```bash
# Test PostgreSQL
mcp__claude-mem__memory-overview

# Test Neo4j  
curl -u neo4j:tempanalysis http://localhost:7474/db/data/

# Test Elasticsearch
curl localhost:9200/memories/_count
```

## 📊 **DATA SOURCE ACCESS**

### PostgreSQL/pgvector (Semantic Analysis)
```bash
# Search semantically
mcp__claude-mem__search "productivity patterns"
mcp__claude-mem__search-enhanced "problem resolution" --min-similarity 0.7

# Get recent context
mcp__claude-mem__get-recent-context --limit 10

# List memories by tag
mcp__claude-mem__list-memories-by-tag "testing"
```

### Neo4j (Workflow Sequences)
```bash
# Basic Cypher query
curl -X POST http://localhost:7474/db/data/cypher \
  -H "Content-Type: application/json" \
  -u neo4j:tempanalysis \
  -d '{"query": "MATCH (m:Memory) RETURN count(m)"}'

# Find workflow sequences
curl -X POST http://localhost:7474/db/data/cypher \
  -H "Content-Type: application/json" \
  -u neo4j:tempanalysis \
  -d '{"query": "MATCH (m1:Memory)-[:FOLLOWS]->(m2:Memory) RETURN m1.memory_id, m2.memory_id LIMIT 10"}'
```

### Elasticsearch (Statistical Patterns)
```bash
# Basic count
curl localhost:9200/memories/_count

# Productivity aggregation
curl -X POST "localhost:9200/memories/_search" \
  -H "Content-Type: application/json" \
  -d '{
    "size": 0,
    "aggs": {
      "hourly_productivity": {
        "terms": {"field": "hour_of_day", "size": 24}
      }
    }
  }'
```

## 🐛 **BUG REPORTING**
```bash
# File a bug report
mcp__claude-mem__store-dev-memory \
  --content "BUG: [Description] - [Data source] - [Impact]" \
  --type "reference" \
  --tags '["bug-report", "[data-source]", "investigation-blocker"]' \
  --status "identified"

# File feature request
mcp__claude-mem__store-dev-memory \
  --content "FEATURE REQUEST: [Enhancement] - [Why needed] - [Expected benefit]" \
  --type "reference" \
  --tags '["feature-request", "[data-source]", "enhancement"]' \
  --status "proposed"
```

## 📝 **DISCOVERY DOCUMENTATION**
```
DISCOVERY: [Brief title]
EVIDENCE: [Specific data/patterns found]
SOURCES: [Which databases provided evidence]
CONFIDENCE: [High/Medium/Low]
IMPLICATIONS: [Actionable insights]
FOLLOW_UP: [New questions generated]
```

## 🔄 **INVESTIGATION PHASES**
1. **Foundation** - Cross-source pattern validation
2. **Unique** - Explore source-specific capabilities  
3. **Hypothesis** - Generate testable theories
4. **Deep** - Focused investigation of promising patterns
5. **Meta** - Synthesize findings and create unified models

## 🎯 **SUCCESS CRITERIA**
- Document all significant discoveries
- Cross-validate patterns across sources
- Generate novel hypotheses for future investigation
- Create actionable workflow optimization recommendations
- File bugs/feature requests when blocked

## 📊 **DATA SCHEMA REFERENCE**
- **memory_id**: Unique identifier
- **content**: Memory content text
- **content_type**: code/decision/conversation/reference
- **created_at**: Timestamp
- **sentiment**: positive/negative/neutral
- **complexity**: low/medium/high
- **development_phase**: planning/implementation/testing_debugging/general
- **technical_domains**: testing/frontend/backend/database/etc

## 🚨 **TROUBLESHOOTING**
- **Neo4j down**: `./02-start-neo4j.sh /tmp`
- **Elasticsearch down**: `./18-lightweight-es-test.sh`
- **Connection issues**: Check localhost binding (127.0.0.1)
- **Data missing**: Verify import completed successfully

**Remember**: You're not just answering questions - you're autonomously discovering new patterns and generating new knowledge about development workflows!