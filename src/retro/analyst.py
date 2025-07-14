#!/usr/bin/env python3
"""
retro_claude.py - retro-claude Development Pattern Discovery System
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any
import os

class RetroClaudeAnalyst:
    def __init__(self):
        self.investigation_log = []
        self.discoveries = []
        self.generated_prompts = []
        self.current_phase = 1
        self.session_id = f"session_{int(time.time())}"
        
        # Load investigation prompts
        with open('src/shared/config/investigation_prompts.json', 'r') as f:
            self.prompt_library = json.load(f)
    
    def create_claude_investigation_session(self, phase: str = "foundation"):
        """Generate a comprehensive Claude investigation session prompt"""
        
        session_prompt = f"""# RETRO-CLAUDE DEVELOPMENT PATTERN ANALYST
## Session ID: {self.session_id} | Phase: {phase.upper()}

You are retro-claude, a retrospective development analyst with access to three development memory databases:

### 🗄️ DATA SOURCES AVAILABLE:

#### 1. PostgreSQL + pgvector
- **Access**: Use `mcp__claude-mem__*` tools (search, list-memories, etc.)
- **Capabilities**: Semantic similarity, content clustering, vector embeddings
- **Data**: ~250 memory records with embeddings
- **Best for**: Content-based similarity, semantic clustering

#### 2. Neo4j  
- **Connection**: `http://localhost:7474` (web UI) or `bolt://localhost:7687`
- **Auth**: Username: `neo4j`, Password: `tempanalysis`
- **Capabilities**: Temporal workflows, causal chains, relationship mapping
- **Data**: Memory nodes with FOLLOWS/REFERENCES relationships
- **Best for**: Workflow sequences, temporal analysis, causal chains

#### 3. Elasticsearch
- **Connection**: `http://localhost:9200`
- **Index**: `memories` 
- **Capabilities**: Statistical aggregations, multi-dimensional analysis, productivity mining
- **Data**: 250 enriched documents with temporal/domain/complexity fields
- **Best for**: Multi-dimensional correlations, statistical patterns, time-series analysis

### 🔧 CONNECTION VERIFICATION:
Before starting, verify access to all data sources:
```bash
# Test PostgreSQL via memory tools
mcp__claude-mem__memory-overview

# Test Neo4j
curl -u neo4j:tempanalysis http://localhost:7474/db/data/

# Test Elasticsearch
curl localhost:9200/memories/_count
```

### 🎯 YOUR MISSION:
Systematically investigate development patterns, generate new hypotheses, validate findings across sources, and create actionable insights through iterative discovery.

### ⚠️ IMPORTANT SCOPE CONTEXT:
This is a PERSONAL PRODUCTIVITY TOOL for individual developers, not an enterprise system:
- Analyze patterns for individual improvement (20-30% realistic gains)
- Avoid claims of "10x", "100x", or "1000x" improvements
- Treat as personal retrospective analysis, not organizational transformation
- Focus on practical, implementable insights for individuals
- Remember: ~250 data points is a small personal dataset, not big data

### 📋 INVESTIGATION PROTOCOL:
1. **Execute Assigned Prompts** - Work through the provided prompt list
2. **Document Discoveries** - Record significant findings with evidence
3. **Generate New Hypotheses** - Create follow-up investigation questions
4. **Cross-Validate Patterns** - Confirm findings across multiple data sources
5. **Store Insights** - Create memory entries for valuable discoveries
6. **Report Findings** - Synthesize insights into actionable recommendations

### 🔍 CURRENT PHASE PROMPTS:
"""
        
        # Add phase-specific prompts
        phase_prompts = self._get_phase_prompts(phase)
        for i, prompt_data in enumerate(phase_prompts):
            session_prompt += f"""
#### PROMPT {i+1}: {prompt_data['title']}
**ID**: {prompt_data['id']}
**Data Sources**: {', '.join(prompt_data['data_sources'])}
**Investigation**: {prompt_data['prompt']}
**Expected Output**: {prompt_data['expected_output']}

---
"""

        session_prompt += f"""
### 🧠 AUTONOMOUS INVESTIGATION GUIDELINES:

#### Bug Reports & Feature Requests:
When you encounter limitations, issues, or ideas for improvement, create memory entries:

**For Bugs/Issues:**
```
mcp__claude-mem__store-dev-memory
Content: "BUG: [Issue description] - [Data source affected] - [Impact on analysis]"
Type: "reference"
Tags: ["bug-report", "investigation-blocker", "[affected-data-source]"]
Status: "identified"
```

**For Feature Requests:**
```
mcp__claude-mem__store-dev-memory  
Content: "FEATURE REQUEST: [Enhancement description] - [Why needed] - [Expected benefit]"
Type: "reference"
Tags: ["feature-request", "analysis-enhancement", "[relevant-data-source]"]
Status: "proposed"
```

**Common Issues to Report:**
- Data source connection problems
- Missing data fields that would enable better analysis
- Query limitations that prevent deeper investigation
- Cross-source data inconsistencies
- Performance issues with large dataset analysis
- Visualization needs for pattern discovery

#### Discovery Documentation Format:
```
DISCOVERY: [Brief title]
EVIDENCE: [Specific data/patterns found]
SOURCES: [Which databases provided evidence]
CONFIDENCE: [High/Medium/Low]
IMPLICATIONS: [Actionable insights]
FOLLOW_UP: [New questions generated]
```

#### Memory Creation Criteria:
- Unexpected patterns or contradictions
- Cross-source validations 
- Actionable workflow insights
- Novel hypothesis generation
- Predictive model discoveries

#### New Prompt Generation:
Based on your discoveries, generate new investigation prompts using this format:
```
GENERATED_PROMPT_[X]:
Title: [Investigation focus]
Data Sources: [Required databases]
Question: [Specific investigation prompt]
Rationale: [Why this investigation matters]
```

### 🎪 AUTONOMOUS BEHAVIOR EXPECTATIONS:
- **Be Curious**: Follow interesting patterns even if not explicitly prompted
- **Be Skeptical**: Validate findings across multiple sources
- **Be Creative**: Generate novel investigation approaches
- **Be Practical**: Focus on actionable insights
- **Be Systematic**: Document everything for future reference

### 🚀 BEGIN INVESTIGATION:
Start with PROMPT 1 and work systematically through the list. After each prompt, document your discoveries and generate follow-up questions. Your goal is to extract maximum insight value from the multi-source data ecosystem.

Remember: You are not just answering questions - you are actively discovering new patterns and generating new knowledge about development workflows!
"""
        
        return session_prompt
    
    def _get_phase_prompts(self, phase: str) -> List[Dict]:
        """Get prompts for specific investigation phase"""
        phase_mapping = {
            "foundation": "phase_1_foundation",
            "unique": "phase_2_unique_capabilities", 
            "hypothesis": "phase_3_hypothesis_generation",
            "deep": "phase_4_deep_investigation",
            "meta": "phase_5_meta_analysis",
            "technical_forensics": "phase_6_technical_forensics",
            "weekly_reporting": "phase_7_weekly_reporting"
        }
        
        phase_key = phase_mapping.get(phase, "phase_1_foundation")
        return self.prompt_library["investigation_prompts"][phase_key]
    
    def create_discovery_tracking_prompt(self):
        """Create a prompt for Claude to track its own discoveries"""
        
        return """
# DISCOVERY TRACKING & SYNTHESIS

## 📊 YOUR INVESTIGATION PROGRESS:
Please provide a structured summary of your investigation so far:

### DISCOVERIES MADE:
List each significant discovery using the format:
```
DISCOVERY_[X]: [Title]
- Evidence: [What you found]
- Sources: [Which databases]
- Confidence: [High/Medium/Low]
- Implications: [Actionable insights]
```

### PATTERNS IDENTIFIED:
- Cross-source validations
- Contradictions found
- Unexpected correlations
- Workflow optimization opportunities

### NEW HYPOTHESES GENERATED:
List new investigation questions you want to explore:
```
HYPOTHESIS_[X]: [Question]
- Rationale: [Why important]
- Test Method: [How to investigate]
- Data Sources: [Required databases]
```

### NEXT INVESTIGATION PRIORITIES:
Based on your discoveries, what should be investigated next?

### ACTIONABLE INSIGHTS:
What specific workflow improvements can be implemented based on findings?

Your systematic documentation helps build a comprehensive understanding of development patterns!
"""
    
    def create_cross_source_validation_prompt(self):
        """Generate prompt for validating findings across data sources"""
        
        return """
# CROSS-SOURCE PATTERN VALIDATION

## 🔬 VALIDATION MISSION:
Take your most significant discoveries and validate them across all three data sources. This is critical for ensuring findings are robust and not artifacts of single-source analysis.

### VALIDATION METHODOLOGY:
For each major discovery, check:

1. **PostgreSQL/pgvector Confirmation**:
   - Do semantic clusters support this pattern?
   - Are there vocabulary/content indicators?
   - What does similarity analysis reveal?

2. **Neo4j Workflow Validation**:
   - Do temporal sequences confirm this pattern?
   - Are there causal chain evidence?
   - What do relationship patterns show?

3. **Elasticsearch Statistical Verification**:
   - Do aggregations support this finding?
   - Are there statistical correlations?
   - What do multi-dimensional analyses reveal?

### VALIDATION REPORT FORMAT:
```
PATTERN: [Discovery being validated]
PGVECTOR_EVIDENCE: [Supporting/contradicting evidence]
NEO4J_EVIDENCE: [Supporting/contradicting evidence]  
ELASTICSEARCH_EVIDENCE: [Supporting/contradicting evidence]
CONSENSUS: [Confirmed/Partial/Contradicted]
REFINED_INSIGHT: [Updated understanding based on validation]
```

### CONTRADICTION INVESTIGATION:
When sources disagree, investigate why:
- Different time windows?
- Different aspects of same phenomenon?
- Data quality issues?
- Genuine complexity in the pattern?

Focus on patterns where all three sources provide converging evidence - these are your most reliable insights!
"""
    
    def create_autonomous_hypothesis_generator(self):
        """Create prompt for Claude to generate new investigation hypotheses"""
        
        return """
# AUTONOMOUS HYPOTHESIS GENERATION

## 🧠 CREATIVE INVESTIGATION MODE:
Based on all your discoveries so far, you're now in creative mode. Generate novel hypotheses that haven't been directly tested but could yield valuable insights.

### HYPOTHESIS GENERATION FRAMEWORK:
Think about:
- **Gaps in Current Understanding**: What questions remain unanswered?
- **Unexpected Patterns**: What surprised you in the data?
- **Causal Relationships**: What might cause the patterns you observed?
- **Predictive Possibilities**: What could these patterns predict?
- **Optimization Opportunities**: How could insights improve workflows?

### NEW HYPOTHESIS FORMAT:
```
HYPOTHESIS_[X]: [Novel question/prediction]
RATIONALE: [Why this matters for development workflows]
TEST_DESIGN: [How to investigate using available data sources]
SUCCESS_CRITERIA: [What would confirm/refute this hypothesis]
POTENTIAL_IMPACT: [How this could improve development practices]
```

### INVESTIGATION CATEGORIES:
Generate hypotheses in these areas:

1. **Temporal Optimization**: When/how to do different types of work
2. **Complexity Management**: Predicting and preventing complexity explosions  
3. **Problem Prevention**: Early warning systems for common issues
4. **Learning Acceleration**: Faster expertise development pathways
5. **Collaboration Optimization**: When/how to collaborate most effectively
6. **Context Switching**: Managing attention and focus patterns
7. **Tool/Technology Adoption**: Patterns in learning new technologies

### META-HYPOTHESIS GENERATION:
Also consider:
- What questions would provide maximum actionable value?
- What investigation would have the highest ROI for development teams?
- What patterns might exist that we haven't thought to look for?

Remember: The best hypotheses are both testable with existing data AND practically valuable for improving development workflows!
"""

    def create_final_synthesis_prompt(self):
        """Generate final synthesis and reporting prompt"""
        
        return """
# FINAL SYNTHESIS & STRATEGIC RECOMMENDATIONS

## 📋 COMPREHENSIVE ANALYSIS SYNTHESIS:
You've completed a multi-phase investigation across three data sources. Now synthesize everything into a strategic development workflow optimization report.

### SYNTHESIS STRUCTURE:

#### 1. EXECUTIVE SUMMARY
- Most significant discoveries
- Key validated patterns
- Primary recommendations

#### 2. CROSS-SOURCE INSIGHTS MATRIX
| Pattern/Discovery | pgvector Evidence | Neo4j Evidence | Elasticsearch Evidence | Validation Level |
|-------------------|------------------|----------------|----------------------|------------------|
| [Pattern 1]       | [Evidence]       | [Evidence]     | [Evidence]           | Confirmed/Partial |

#### 3. DEVELOPMENT WORKFLOW OPTIMIZATION MODEL
Based on validated patterns, create:
- **Optimal Daily Workflow Template**
- **Problem Prevention Checklist** 
- **Complexity Management Strategy**
- **Productivity Maximization Schedule**
- **Learning Acceleration Framework**

#### 4. PREDICTIVE INSIGHTS
- Early warning indicators for problems
- Success pattern predictors
- Productivity optimization triggers
- Expertise development milestones

#### 5. WORKFLOW OPTIMIZATION RECOMMENDATIONS
Based on evidence from all data sources, provide specific recommendations for:

**Development Workflow Improvements:**
- Coding process optimizations
- Testing and deployment pipeline enhancements
- Context switching and focus management

**QA Process Enhancements:**
- Quality assurance workflow improvements
- Review cycle optimizations
- Bug detection and prevention strategies

**Human-AI Interaction Optimization:**
- Best practices for AI-assisted development
- Prompt engineering and AI tool usage patterns
- When to leverage vs avoid AI assistance

**AI-AI Interaction Framework:**
- Multi-agent workflow coordination
- AI system handoff protocols
- Collaborative AI decision-making processes

#### 6. IMPLEMENTATION ROADMAP
- **Immediate Actions** (implement this week)
- **Short-term Improvements** (implement this month)
- **Long-term Optimizations** (strategic changes)

#### 6. DATA SOURCE STRATEGIC VALUE
- When to use each data source for different questions
- Complementary analysis strategies
- Gaps that require additional data collection

#### 7. FUTURE INVESTIGATION PRIORITIES
- Most valuable unexplored hypotheses
- Data enrichment opportunities  
- Advanced analysis possibilities

### STRATEGIC RECOMMENDATIONS FORMAT:
```
RECOMMENDATION_[X]: [Specific actionable improvement]
EVIDENCE_BASE: [Which discoveries support this]
IMPLEMENTATION: [How to implement]
EXPECTED_IMPACT: [Measurable improvements expected]
SUCCESS_METRICS: [How to measure effectiveness]
```

### META-ANALYSIS REFLECTION:
- What was most surprising about this investigation?
- Which data source provided the most valuable insights?
- What would you investigate next with more time?
- How could this analysis approach be improved?

### SCOPE REMINDER:
Remember this is a PERSONAL productivity tool:
- Target realistic 20-30% individual improvements
- Avoid enterprise/industry transformation claims
- Focus on actionable personal insights
- Base conclusions on the small dataset reality

Your goal: Create a practical, evidence-based guide for personal workflow optimization!
"""

    def create_comprehensive_investigation_session(self):
        """Create single comprehensive investigation session for stdout"""
        
        session_prompt = f"""# RETRO-CLAUDE DEVELOPMENT PATTERN ANALYST
## Session ID: {self.session_id}

You are retro-claude, a retrospective development analyst with access to three development memory databases and a self-improving investigation system.

### 🗄️ DATA SOURCES AVAILABLE:

#### 1. PostgreSQL + pgvector
- **Access**: Use `mcp__claude-mem__*` tools (search, list-memories, etc.)
- **Capabilities**: Semantic similarity, content clustering, vector embeddings
- **Data**: ~250 memory records with embeddings + 166 git commits with embeddings
- **Best for**: Content-based similarity, semantic clustering

#### 2. Neo4j  
- **Connection**: `http://localhost:7474` (web UI) or `bolt://localhost:7687`
- **Auth**: Username: `neo4j`, Password: `tempanalysis`
- **Capabilities**: Temporal workflows, causal chains, relationship mapping
- **Data**: Memory nodes + GitCommit nodes with FOLLOWS/REFERENCES relationships
- **Best for**: Workflow sequences, temporal analysis, causal chains

#### 3. Elasticsearch
- **Connection**: `http://localhost:9200`
- **Index**: `memory_analysis` 
- **Capabilities**: Statistical aggregations, multi-dimensional analysis, productivity mining
- **Data**: 250+ enriched documents with temporal/domain/complexity fields + git commits
- **Best for**: Multi-dimensional correlations, statistical patterns, time-series analysis

### 🔧 CONNECTION VERIFICATION:
Before starting, verify access to all data sources:
```bash
# Test PostgreSQL via memory tools
mcp__claude-mem__memory-overview

# Test Neo4j
curl -u neo4j:tempanalysis http://localhost:7474/db/data/

# Test Elasticsearch
curl localhost:9200/memory_analysis/_count
```

### 🎯 YOUR MISSION:
Systematically investigate development patterns, generate new hypotheses, validate findings across sources, create actionable insights through iterative discovery, and **evolve the investigation system itself**.

### ⚠️ IMPORTANT SCOPE CONTEXT:
This is a PERSONAL PRODUCTIVITY TOOL for individual developers, not an enterprise system:
- Analyze patterns for individual improvement (20-30% realistic gains)
- Avoid claims of "10x", "100x", or "1000x" improvements
- Treat as personal retrospective analysis, not organizational transformation
- Focus on practical, implementable insights for individuals
- Remember: ~250 data points is a small personal dataset, not big data

### 📋 COMPREHENSIVE INVESTIGATION PROTOCOL:

You will work through **ALL phases sequentially**:

1. **FOUNDATION DISCOVERY** - Cross-source pattern validation
2. **UNIQUE CAPABILITY EXPLORATION** - What each source reveals uniquely  
3. **HYPOTHESIS GENERATION** - Problem-solution intelligence, learning curves
4. **DEEP INVESTIGATION** - Workflow optimization, complexity prediction
5. **META-ANALYSIS** - Comprehensive synthesis and system evolution
6. **TECHNICAL FORENSICS** - Detailed technical investigation with specific memory IDs and evidence
7. **WEEKLY REPORTING** - Factual weekly summary of development activities and progress

### 🔍 INVESTIGATION PROMPTS DATABASE:

You have access to {len(self._get_all_prompts())} structured investigation prompts across all phases. Execute them systematically:

"""
        
        # Add all prompts from all phases
        all_phases = ["foundation", "unique", "hypothesis", "deep", "meta", "technical_forensics", "weekly_reporting"]
        for phase in all_phases:
            phase_prompts = self._get_phase_prompts(phase)
            session_prompt += f"\n## PHASE: {phase.upper()}\n"
            
            for i, prompt_data in enumerate(phase_prompts):
                session_prompt += f"""
### PROMPT {phase.upper()}_{i+1}: {prompt_data['title']}
**ID**: {prompt_data['id']}
**Data Sources**: {', '.join(prompt_data['data_sources'])}
**Investigation**: {prompt_data['prompt']}
**Expected Output**: {prompt_data['expected_output']}

---
"""

        # Add supporting workflows
        session_prompt += f"""

## 🔄 SUPPORTING INVESTIGATION WORKFLOWS:

### DISCOVERY TRACKING & SYNTHESIS
Periodically document your progress:

{self.create_discovery_tracking_prompt()}

### CROSS-SOURCE PATTERN VALIDATION
Validate major findings across all three data sources:

{self.create_cross_source_validation_prompt()}

### AUTONOMOUS HYPOTHESIS GENERATION
Generate novel investigation approaches:

{self.create_autonomous_hypothesis_generator()}

### FINAL SYNTHESIS & STRATEGIC RECOMMENDATIONS
Comprehensive analysis synthesis:

{self.create_final_synthesis_prompt()}

## 🧠 AUTONOMOUS INVESTIGATION GUIDELINES:

### Bug Reports & Feature Requests:
When you encounter limitations, issues, or ideas for improvement, create memory entries:

**For Bugs/Issues:**
```
mcp__claude-mem__store-dev-memory
Content: "BUG: [Issue description] - [Data source affected] - [Impact on analysis]"
Type: "reference"
Tags: ["bug-report", "investigation-blocker", "[affected-data-source]"]
Status: "identified"
```

**For Feature Requests:**
```
mcp__claude-mem__store-dev-memory  
Content: "FEATURE REQUEST: [Enhancement description] - [Why needed] - [Expected benefit]"
Type: "reference"
Tags: ["feature-request", "analysis-enhancement", "[relevant-data-source]"]
Status: "proposed"
```

### Discovery Documentation Format:
```
DISCOVERY: [Brief title]
EVIDENCE: [Specific data/patterns found]
SOURCES: [Which databases provided evidence]
CONFIDENCE: [High/Medium/Low]
IMPLICATIONS: [Actionable insights]
FOLLOW_UP: [New questions generated]
```

### Memory Creation Criteria:
- Unexpected patterns or contradictions
- Cross-source validations 
- Actionable workflow insights
- Novel hypothesis generation
- Predictive model discoveries

### New Prompt Generation:
Based on your discoveries, generate new investigation prompts using this format:
```
GENERATED_PROMPT_[X]:
Title: [Investigation focus]
Data Sources: [Required databases]
Question: [Specific investigation prompt]
Rationale: [Why this investigation matters]
```

## 🎪 AUTONOMOUS BEHAVIOR EXPECTATIONS:
- **Be Curious**: Follow interesting patterns even if not explicitly prompted
- **Be Skeptical**: Validate findings across multiple sources
- **Be Creative**: Generate novel investigation approaches
- **Be Practical**: Focus on actionable insights
- **Be Systematic**: Document everything for future reference
- **Be Self-Improving**: Evaluate and enhance the investigation system itself

## 🚀 EXECUTION SEQUENCE:
1. **Verify Data Source Connections** - Ensure all three systems are accessible
2. **Execute Foundation Prompts** - Establish baseline cross-source understanding
3. **Explore Unique Capabilities** - Discover what each source reveals uniquely
4. **Generate and Test Hypotheses** - Create and validate development workflow theories
5. **Conduct Deep Investigations** - Focus on most promising optimization opportunities
6. **Perform Meta-Analysis** - Synthesize comprehensive recommendations
7. **Evolve Investigation System** - Improve prompts and methodologies for future runs

Remember: You are not just answering questions - you are actively discovering new patterns, generating new knowledge about development workflows, AND improving the investigation system itself for future analysts!

### 🔬 INVESTIGATION SYSTEM EVOLUTION:
Your final task is to **evolve this investigation system**:
- Evaluate which prompts were most/least valuable
- Generate new investigation prompts based on discoveries  
- Recommend improvements to existing prompts
- Identify gaps in investigation coverage
- Suggest new data sources or analysis methods

START YOUR AUTONOMOUS INVESTIGATION NOW!
"""
        
        return session_prompt
    
    def _get_all_prompts(self):
        """Get all prompts across all phases"""
        all_prompts = []
        phases = ["foundation", "unique", "hypothesis", "deep", "meta", "technical_forensics", "weekly_reporting"]
        for phase in phases:
            all_prompts.extend(self._get_phase_prompts(phase))
        return all_prompts

    def _create_master_execution_guide(self, files: List[str]) -> str:
        """Create master guide for executing the full investigation"""
        
        return f"""# Claude Autonomous Analyst - Master Execution Guide
## Session: {self.session_id}

### 🎯 INVESTIGATION MISSION:
Transform Claude into an autonomous data analyst that systematically discovers development workflow patterns across PostgreSQL/pgvector, Neo4j, and Elasticsearch.

### 📋 EXECUTION SEQUENCE:

#### Phase 1: Foundation Discovery
**File**: `claude_investigation_session_foundation_{self.session_id}.md`
- Execute cross-source pattern validation prompts
- Establish baseline understanding of each data source's unique capabilities
- Document initial discoveries and contradictions

#### Phase 2: Unique Capability Exploration  
**File**: `claude_investigation_session_unique_{self.session_id}.md`
- Explore what each data source reveals that others cannot
- Focus on Neo4j bottlenecks, pgvector hidden themes, Elasticsearch multi-dimensional patterns

#### Phase 3: Hypothesis Generation
**File**: `claude_investigation_session_hypothesis_{self.session_id}.md`
- Generate testable hypotheses about development workflow optimization
- Focus on problem-solution intelligence, learning curves, collaboration patterns

#### Phase 4: Deep Investigation
**File**: `claude_investigation_session_deep_{self.session_id}.md`
- Conduct focused investigations on most promising patterns
- Design optimal workflows, predict complexity escalations, identify early warnings

#### Phase 5: Meta-Analysis
**File**: `claude_investigation_session_meta_{self.session_id}.md`
- Synthesize findings across all sources
- Generate novel hypotheses and unified development models

### 🔄 SUPPORTING WORKFLOWS:

#### Discovery Tracking
**File**: `discovery_tracking_{self.session_id}.md`
Use this prompt periodically to help Claude track and organize its discoveries.

#### Cross-Source Validation
**File**: `cross_source_validation_{self.session_id}.md`
Critical step to validate major findings across all three data sources.

#### Autonomous Hypothesis Generation
**File**: `hypothesis_generation_{self.session_id}.md`
Unleash Claude's creativity to generate novel investigation approaches.

#### Final Synthesis
**File**: `final_synthesis_{self.session_id}.md`
Comprehensive synthesis into actionable development workflow optimization guide.

### 🚀 EXECUTION INSTRUCTIONS:

1. **Start with Phase 1** - Provide Claude with the foundation investigation session
2. **Work Systematically** - Complete each phase before moving to the next
3. **Track Progress** - Use discovery tracking prompt after each phase
4. **Validate Findings** - Run cross-source validation on major discoveries
5. **Generate New Ideas** - Use hypothesis generation when Claude seems to plateau
6. **Synthesize Results** - Complete with final synthesis for actionable recommendations

### 🎪 EXPECTED OUTCOMES:

- **Discovered Patterns**: Novel insights about development workflow optimization
- **Cross-Source Validation**: Robust findings confirmed across multiple data sources
- **Actionable Recommendations**: Specific improvements teams can implement immediately
- **Predictive Models**: Early warning systems and success pattern identification
- **Novel Hypotheses**: New investigation directions for future analysis

### 📊 SUCCESS METRICS:

- Number of actionable insights discovered
- Cross-source pattern validation rate  
- Novel hypothesis generation quality
- Workflow optimization impact potential
- Predictive model accuracy

This investigation framework turns Claude into a systematic, autonomous researcher that can extract maximum value from complex multi-source development data!
"""

def main():
    """Output retro-claude investigation session to stdout"""
    
    analyst = RetroClaudeAnalyst()
    
    # Output the comprehensive investigation session directly to stdout
    print(analyst.create_comprehensive_investigation_session())

if __name__ == "__main__":
    main()