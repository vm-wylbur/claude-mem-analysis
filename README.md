# retro-claude Memory Analysis System

A comprehensive multi-source development memory analysis system that integrates PostgreSQL/pgvector, Neo4j, and Elasticsearch to discover patterns in development workflows and enable retro-claude retrospective investigation.

## 🎯 Overview

This system captures development memories and git commits across three complementary data sources:

- **PostgreSQL + pgvector**: Semantic similarity and content clustering using vector embeddings
- **Neo4j**: Temporal workflow sequences, causal chains, and relationship mapping  
- **Elasticsearch**: Statistical aggregations, multi-dimensional analysis, and full-text search

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ with `uv` package manager
- PostgreSQL with pgvector extension
- Neo4j database
- Elasticsearch cluster
- Docker (optional, for containerized services)

### Installation

```bash
# Clone and setup
git clone <repository-url>
cd claude-mem-analysis
uv sync

# Configure database connections
cp config/claude-mem.toml.example ~/.config/claude-mem/claude-mem.toml
# Edit with your database credentials
```

### Basic Usage

#### Complete Pipeline (Hands-Off)
```bash
# Single command: scan → import → analyze → investigate
uv run retro-claude-all | claude
```

#### Individual Steps
```bash
# Scan git repositories for commits
uv run git-scanner

# Import to all data sources
uv run postgres-importer
uv run neo4j-importer  
uv run elasticsearch-importer

# Run unified analysis
uv run unified-analysis

# Launch retro-claude investigation
uv run retro-claude | claude
```

## 📁 Project Structure

```
├── src/                          # Core application code
│   ├── retro_claude.py           # retro-claude investigation system
│   ├── git_scanner.py            # Git repository commit scanner
│   ├── postgres_importer.py      # PostgreSQL data import
│   ├── neo4j_importer.py         # Neo4j relationship import
│   ├── elasticsearch_importer.py # Elasticsearch document import
│   └── unified_analysis.py       # Cross-source analysis
├── config/                       # Configuration files
│   └── investigation_prompts.json # retro-claude investigation prompts database
├── docs/                         # Documentation
├── scripts/                      # Utility scripts
├── archive/                      # Development history
│   ├── development-sessions/     # retro-claude investigation sessions
│   ├── elasticsearch-evolution/  # ES development history
│   └── early-analysis/          # Early analysis experiments
├── pyproject.toml               # Python project configuration
└── README.md                    # This file
```

## 🔧 Core Components

### Git Scanner (`src/git_scanner.py`)
Scans all repositories in `~/projects` for commits from the last 14 days, extracting:
- Commit metadata (hash, author, timestamp, message)
- File changes (added/deleted lines, changed files)
- Primary programming language
- Commit type classification

### Multi-Source Importers
- **PostgreSQL**: Stores commits with vector embeddings for semantic similarity
- **Neo4j**: Creates relationship graphs between commits, authors, and repositories
- **Elasticsearch**: Enables full-text search and statistical aggregations

### retro-claude (`src/retro_claude.py`)
Retrospective investigation system with 36 structured prompts across 7 phases:
1. **Foundation Discovery** - Cross-source pattern validation
2. **Unique Capabilities** - Source-specific insights
3. **Hypothesis Generation** - Development workflow theories
4. **Deep Investigation** - Focused optimization analysis
5. **Meta-Analysis** - Comprehensive synthesis
6. **Technical Forensics** - Detailed technical investigation
7. **Weekly Reporting** - Factual weekly development activity summaries

### Unified Analysis (`src/unified_analysis.py`)
Cross-source correlation engine that validates findings across all three data sources and generates actionable insights.

## 🎪 Data Sources & Capabilities

| Data Source | Best For | Key Features |
|-------------|----------|--------------|
| **PostgreSQL + pgvector** | Content similarity, semantic clustering | Vector embeddings, similarity search, content analysis |
| **Neo4j** | Workflow sequences, temporal analysis | Relationship mapping, causal chains, graph traversal |
| **Elasticsearch** | Statistical patterns, multi-dimensional analysis | Aggregations, full-text search, time-series analysis |

## 🔍 Investigation Workflow

The autonomous Claude investigation follows this systematic approach:

1. **Verify Data Sources** - Ensure all three systems are accessible
2. **Execute Foundation Prompts** - Establish baseline understanding
3. **Explore Unique Capabilities** - Discover source-specific insights
4. **Generate Hypotheses** - Create testable development theories
5. **Conduct Deep Analysis** - Focus on optimization opportunities
6. **Synthesize Findings** - Generate actionable recommendations
7. **Evolve System** - Improve investigation methodology

## 📊 Key Features

- **Cross-Source Validation**: Findings confirmed across multiple data sources
- **Semantic Similarity**: Vector embeddings enable content-based discovery
- **Temporal Analysis**: Neo4j reveals workflow sequences and patterns
- **Statistical Mining**: Elasticsearch aggregations uncover trends
- **Retrospective Investigation**: Self-improving retro-claude analysis system
- **Conflict Resolution**: Idempotent imports handle duplicate data
- **Git Integration**: Real-time development activity correlation

## 🛠️ Configuration

### Database Connections

Configure database connections in `~/.config/claude-mem/claude-mem.toml`:

```toml
[database.postgresql]
hosts = ["localhost"]
port = 5432
database = "claude_mem"
user = "your_user"
password = "your_password"

[database.neo4j]
uri = "bolt://localhost:7687"
user = "neo4j"
password = "your_password"

[database.elasticsearch]
hosts = ["localhost:9200"]
index = "memory_analysis"
```

### Investigation Prompts

The investigation system uses a structured prompt database in `config/investigation_prompts.json` with 36+ prompts across 7 phases. The system is self-improving - retro-claude can evaluate and enhance prompts based on discoveries.

## 🎉 Success Metrics

This system has successfully:
- ✅ Imported 166 unique git commits across 24 repositories
- ✅ Achieved cross-source data consistency validation
- ✅ Generated 36 structured investigation prompts
- ✅ Created retro-claude investigation workflow
- ✅ Discovered critical bugs through cross-validation
- ✅ Established self-improving investigation methodology

## 🐛 Lessons Learned

Key insights from development (stored as memories in the system):

1. **String Processing Bug**: Critical git scanner bug using `'\\n'` instead of `'\n'` in string splits, missing 90%+ of commits
2. **Multi-Source Architecture**: Each data source validates others, creating robust analysis framework
3. **Conflict Resolution**: Essential for idempotent imports across different database systems
4. **Repository Organization**: Archive development history, use descriptive names, separate concerns
5. **retro-claude Integration**: Single stdout pipeline more effective than multiple timestamped files

## 🔮 Future Enhancements

- Real-time git hook integration for live analysis
- Machine learning models for productivity prediction
- Advanced temporal pattern recognition
- Cross-repository dependency analysis
- Team collaboration optimization insights

## 📝 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

[Contributing guidelines]

---

**Ready for hands-off retrospective investigation!** Launch with: `uv run retro-claude-all | claude`