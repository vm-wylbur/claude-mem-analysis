#!/bin/bash
# memory-pattern-analysis.sh
# One-shot Neo4j analysis of your memory database

set -e

# Read configuration from claude-mem.toml
CONFIG_FILE="$HOME/.config/claude-mem/claude-mem.toml"

echo "📖 Reading config from $CONFIG_FILE"

if [[ ! -f "$CONFIG_FILE" ]]; then
    echo "❌ Config file not found: $CONFIG_FILE"
    exit 1
fi

# Parse TOML config - extract postgresql section
POSTGRES_SECTION=$(awk '/^\[database\.postgresql\]$/,/^\[ollama\]$/ {if (/^\[ollama\]$/) exit; print}' "$CONFIG_FILE")

# Extract individual fields
POSTGRES_HOST=$(echo "$POSTGRES_SECTION" | grep '^hosts' | sed 's/hosts = \["\(.*\)"\]/\1/')
POSTGRES_PORT=$(echo "$POSTGRES_SECTION" | grep '^port' | sed 's/port = \([0-9]*\)/\1/')
POSTGRES_DB=$(echo "$POSTGRES_SECTION" | grep '^database' | sed 's/database = "\(.*\)"/\1/')
POSTGRES_USER=$(echo "$POSTGRES_SECTION" | grep '^user' | sed 's/user = "\(.*\)"/\1/')
POSTGRES_PASSWORD=$(echo "$POSTGRES_SECTION" | grep '^password' | sed 's/password = "\(.*\)"/\1/')

# Validate we got the config
if [[ -z "$POSTGRES_HOST" || -z "$POSTGRES_PORT" || -z "$POSTGRES_DB" || -z "$POSTGRES_USER" || -z "$POSTGRES_PASSWORD" ]]; then
    echo "❌ Failed to parse database config from TOML file"
    echo "   Host: '$POSTGRES_HOST'"
    echo "   Port: '$POSTGRES_PORT'"
    echo "   DB: '$POSTGRES_DB'"
    echo "   User: '$POSTGRES_USER'"
    echo "   Password: $(if [[ -n "$POSTGRES_PASSWORD" ]]; then echo "[SET]"; else echo "[MISSING]"; fi)"
    exit 1
fi

echo "✅ Database config loaded:"
echo "   Host: $POSTGRES_HOST:$POSTGRES_PORT"
echo "   Database: $POSTGRES_DB"
echo "   User: $POSTGRES_USER"

NEO4J_PASSWORD="tempanalysis"
WORK_DIR="/tmp/memory-analysis-$(date +%s)"

echo "🧠 Starting memory pattern analysis..."
echo "📁 Working directory: $WORK_DIR"

# Create working directory
mkdir -p "$WORK_DIR"
cd "$WORK_DIR"

# 1. Export memories from PostgreSQL
echo "📊 Exporting memories from PostgreSQL..."
# Create SQL export file
cat > export_memories.sql << 'SQLEOF'
\copy (
    SELECT 
        memory_id,
        content,
        content_type,
        created_at,
        updated_at,
        metadata,
        -- Extract technologies mentioned
        CASE 
            WHEN content ~* 'docker' THEN 'docker'
            WHEN content ~* 'truenas|truenas scale' THEN 'truenas'
            WHEN content ~* 'zfs|syncoid' THEN 'zfs'
            WHEN content ~* 'postgres|postgresql' THEN 'postgres'
            WHEN content ~* 'ups|netdata' THEN 'monitoring'
            WHEN content ~* 'nginx|apache|web' THEN 'web'
            ELSE 'general'
        END as primary_tech,
        -- Detect sentiment/difficulty
        CASE 
            WHEN content ~* 'frustrat|annoying|difficult|problem|error|fail|broke' THEN 'negative'
            WHEN content ~* 'success|work|good|easy|simple|fixed|solved' THEN 'positive'
            ELSE 'neutral'
        END as sentiment,
        -- Estimate complexity by content length and keywords
        CASE 
            WHEN length(content) > 1000 AND content ~* 'config|setup|install|deploy' THEN 'high'
            WHEN length(content) > 500 OR content ~* 'issue|debug|troubleshoot' THEN 'medium'
            ELSE 'low'
        END as complexity
    FROM memories 
    ORDER BY created_at
) TO STDOUT WITH CSV HEADER
SQLEOF

# Export data (with SSL required for Aiven)
PGPASSWORD="$POSTGRES_PASSWORD" psql \
    -h "$POSTGRES_HOST" \
    -p "$POSTGRES_PORT" \
    -U "$POSTGRES_USER" \
    -d "$POSTGRES_DB" \
    --set=sslmode=require \
    -f export_memories.sql >memories.csv

echo "✅ Exported $(wc -l <memories.csv) memory records"
