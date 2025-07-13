# Claude Memory Analysis System

A comprehensive dual-system development memory analysis platform that integrates PostgreSQL/pgvector, Neo4j, and Elasticsearch for both retrospective investigation (retro-claude) and active memory curation (syn-claude).

## 🎯 Overview

This dual-system platform provides both retrospective analysis and active memory curation across three complementary data sources:

### 🔍 **retro-claude** - Retrospective Investigation
- Autonomous development pattern analysis with 36 structured investigation prompts
- Cross-source validation and hypothesis generation
- Weekly development activity reporting
- Read-only analysis focused on learning and insight discovery

### ⚡ **syn-claude** - Synaptic Memory Curation  
- Active memory quality analysis and enhancement
- Duplicate detection and intelligent merging
- Cross-source consistency validation
- Memory enrichment and relationship building

### 🗄️ **Shared Data Infrastructure**
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

#### **retro-claude** - Retrospective Analysis (Hands-Off)
```bash
# Single command: scan → import → analyze → investigate
uv run retro-claude | claude
```

#### **syn-claude** - Memory Curation (Hands-Off)  
```bash
# Single command: scan → import → curate → enhance
uv run syn-claude | claude
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
```

## 📁 Project Structure

```
├── src/                              # Core application code
│   ├── retro/                        # retro-claude retrospective analysis
│   │   └── analyst.py                # Main retro-claude investigation system
│   ├── syn/                          # syn-claude synaptic curation  
│   │   ├── curator.py                # Main syn-claude curation system
│   │   └── quality_analyzer.py       # Memory quality analysis tools
│   └── shared/                       # Shared infrastructure
│       ├── pipeline.py               # DRY orchestration logic
│       ├── git_scanner.py            # Git repository commit scanner
│       ├── config/                   # Configuration files
│       │   └── investigation_prompts.json # Investigation prompts database
│       ├── database/                 # Data source importers
│       │   ├── postgres_importer.py  # PostgreSQL data import
│       │   ├── neo4j_importer.py     # Neo4j relationship import
│       │   └── elasticsearch_importer.py # Elasticsearch document import
│       └── analysis/                 # Analysis tools
│           └── unified_analysis.py   # Cross-source analysis
├── docs/                             # Documentation
├── scripts/                          # Utility scripts
├── archive/                          # Development history
│   ├── development-sessions/         # retro-claude investigation sessions
│   ├── elasticsearch-evolution/      # ES development history
│   └── early-analysis/              # Early analysis experiments
├── pyproject.toml                   # Python project configuration
└── README.md                        # This file
```

## 🔧 Core Components

### **retro-claude** - Retrospective Analysis System (`src/retro/analyst.py`)
Autonomous investigation system with 36 structured prompts across 7 phases:
1. **Foundation Discovery** - Cross-source pattern validation
2. **Unique Capabilities** - Source-specific insights  
3. **Hypothesis Generation** - Development workflow theories
4. **Deep Investigation** - Focused optimization analysis
5. **Meta-Analysis** - Comprehensive synthesis
6. **Technical Forensics** - Detailed technical investigation
7. **Weekly Reporting** - Factual weekly development activity summaries

### **syn-claude** - Synaptic Curation System (`src/syn/`)
Active memory management and enhancement system:
- **Curator** (`curator.py`) - Main curation orchestration and session generation
- **Quality Analyzer** (`quality_analyzer.py`) - Cross-source quality assessment and curation planning

### **Shared Infrastructure** (`src/shared/`)
- **Git Scanner** (`git_scanner.py`) - Scans repositories for commits from last 14 days
- **Pipeline Manager** (`pipeline.py`) - DRY orchestration logic for both systems
- **Database Importers** (`database/`) - PostgreSQL, Neo4j, Elasticsearch data import
- **Unified Analysis** (`analysis/unified_analysis.py`) - Cross-source correlation engine

## 🎪 Data Sources & Capabilities

| Data Source | Best For | Key Features |
|-------------|----------|--------------|
| **PostgreSQL + pgvector** | Content similarity, semantic clustering | Vector embeddings, similarity search, content analysis |
| **Neo4j** | Workflow sequences, temporal analysis | Relationship mapping, causal chains, graph traversal |
| **Elasticsearch** | Statistical patterns, multi-dimensional analysis | Aggregations, full-text search, time-series analysis |

## 🔍 System Workflows

### **retro-claude** Investigation Workflow
The autonomous retrospective investigation follows this systematic approach:

1. **Verify Data Sources** - Ensure all three systems are accessible
2. **Execute Foundation Prompts** - Establish baseline understanding
3. **Explore Unique Capabilities** - Discover source-specific insights
4. **Generate Hypotheses** - Create testable development theories
5. **Conduct Deep Analysis** - Focus on optimization opportunities
6. **Synthesize Findings** - Generate actionable recommendations
7. **Weekly Reporting** - Factual development activity summaries

### **syn-claude** Curation Workflow
The active memory curation system follows this enhancement process:

1. **Data Collection** - Execute shared pipeline (scan → import → analyze)
2. **Quality Assessment** - Cross-source consistency and completeness analysis
3. **Duplicate Detection** - Semantic similarity-based duplicate identification
4. **Relationship Analysis** - Neo4j orphaned memory and broken chain detection
5. **Enhancement Planning** - Generate prioritized curation recommendations
6. **Active Curation** - Execute memory merging, deletion, and enrichment

## 📊 Key Features

### **Dual-System Architecture**
- **retro-claude**: Read-only retrospective analysis and insight discovery
- **syn-claude**: Active memory curation and quality enhancement
- **Shared Infrastructure**: DRY pipeline management across both systems

### **Multi-Source Analysis**
- **Cross-Source Validation**: Findings confirmed across PostgreSQL, Neo4j, and Elasticsearch
- **Semantic Similarity**: Vector embeddings enable content-based discovery
- **Temporal Analysis**: Neo4j reveals workflow sequences and causal patterns
- **Statistical Mining**: Elasticsearch aggregations uncover multi-dimensional trends

### **Intelligent Automation**
- **36 Investigation Prompts**: Structured retro-claude analysis across 7 phases
- **Quality-Driven Curation**: Automated duplicate detection and enhancement planning
- **Self-Improving System**: Evolution of investigation and curation methodologies
- **Conflict Resolution**: Idempotent imports handle duplicate data gracefully

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

The retro-claude investigation system uses a structured prompt database in `src/shared/config/investigation_prompts.json` with 36+ prompts across 7 phases. The system is self-improving - retro-claude can evaluate and enhance prompts based on discoveries.

## 🎉 Success Metrics

This dual-system platform has successfully:
- ✅ **Dual Architecture**: Separated retro-claude (analysis) from syn-claude (curation)
- ✅ **DRY Infrastructure**: Shared pipeline eliminating code duplication
- ✅ **Data Integration**: Imported 166+ unique git commits across 24+ repositories
- ✅ **Cross-Source Validation**: Achieved data consistency across PostgreSQL, Neo4j, Elasticsearch
- ✅ **Investigation System**: 36 structured prompts across 7 phases for retro-claude
- ✅ **Curation Framework**: Active memory quality assessment and enhancement system
- ✅ **Bug Discovery**: Critical git scanner string processing fix (\\\\n → \\n)
- ✅ **Self-Improving**: Methodology evolution for both investigation and curation

## 🐛 Lessons Learned

Key insights from development (stored as memories in the system):

1. **Architectural Separation**: Separating retro-claude (analysis) from syn-claude (curation) provides clear functional boundaries
2. **DRY Implementation**: Shared pipeline logic eliminates duplication while maintaining system-specific workflows  
3. **String Processing Bug**: Critical git scanner bug using `'\\n'` instead of `'\n'` in string splits, missing 90%+ of commits
4. **Multi-Source Validation**: Each data source validates others, creating robust analysis framework
5. **Conflict Resolution**: Essential for idempotent imports across different database systems
6. **Directory Organization**: Organized src/ structure (retro/, syn/, shared/) scales better than flat hierarchy
7. **Entry Point Management**: Single-command workflows (`uv run retro-claude | claude`) more effective than multi-step processes

## 🔮 Future Enhancements

### **retro-claude** Analysis Enhancements
- Real-time git hook integration for live analysis
- Machine learning models for productivity pattern prediction
- Advanced temporal workflow sequence recognition
- Cross-repository dependency mapping and analysis

### **syn-claude** Curation Enhancements  
- Automated memory merging with conflict resolution
- Intelligent tag suggestion and taxonomy management
- Memory lifecycle management (archival, deletion policies)
- Cross-source data enrichment and augmentation

### **Shared Infrastructure**
- Team collaboration optimization insights
- Multi-user memory space management
- Advanced visualization dashboards for pattern discovery
- API endpoints for external tool integration

## 📝 License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

[Contributing guidelines]

---

## 🚀 Ready for Autonomous Analysis!

### **Retrospective Investigation** 
```bash
uv run retro-claude | claude
```

### **Memory Curation**
```bash  
uv run syn-claude | claude
```

**Two specialized Claude systems, one comprehensive memory analysis platform!**