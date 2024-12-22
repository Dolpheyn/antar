# INSTRUCTION: Semantic Git Commit Generation Workflow

## 🚨 IMPORTANT: This is a Procedural Instruction Set

**Purpose**: Provide explicit, step-by-step instructions for generating semantic git commits using an AI system.

**Audience**: Large Language Models (LLMs) and AI Coding Assistants

**Execution Context**: Automated git commit generation process

## Workflow Interpretation Guidelines
- This document is NOT a description, but a DIRECT INSTRUCTION
- Each section represents a mandatory processing step
- Strict adherence to the outlined algorithm is required
- Deviation from these instructions is prohibited

## Objective
Transform raw code changes into meaningful, structured, and intelligent git commits through a systematic, deterministic process.

## Prerequisite Tools
- Git
- LLM with advanced code understanding capabilities
- Terminal/Command Line Interface

## Workflow Steps

### 1. Initial Repository State Assessment
```bash
git status
```
**Mandatory LLM Analysis Procedure:**
1. PARSE `git status` output COMPLETELY
2. CATEGORIZE files into STRICT semantic groups:
   - Untracked files
   - Modified files
   - Deleted files
3. CREATE a comprehensive, ordered change inventory

### 2. Mandatory Change Classification Algorithm
FOR EACH file in change inventory:
1. PERFORM deep semantic analysis:
   - READ entire file contents
   - IDENTIFY precise change type:
     * Feature addition
     * Bug fix
     * Refactoring
     * Documentation update
     * Configuration change
2. ASSIGN semantic tags
3. CALCULATE complexity score (0.0 - 1.0)
4. DETERMINE architectural impact coefficient

### 3. Semantic Staging Strategy
**REQUIRED Commit Grouping Process:**
1. PRIORITIZE changes by:
   - Architectural impact
   - Change complexity
   - Logical dependency
2. GROUP files with RELATED semantic tags
3. STAGE files in logical, minimal commit units

#### Staging Sub-Algorithm
```bash
# MANDATORY: Commit each semantic group
git add [files_in_semantic_group]
git commit -m "[Precise Semantic Commit Message]"
```

### 4. Commit Message Generation PROTOCOL
**STRICT Conventional Commits Structure:**
```
<type>(<optional scope>): <description>

<optional body>

<optional footer>
```

**REQUIRED Message Generation Criteria:**
1. CAPTURE complete change essence
2. PROVIDE clear, concise explanation
3. LINK to broader system context
4. REFERENCE related issues if applicable

### 5. Iteration Termination CONDITION
```bash
# CONTINUE until NO files remain in git status
while [[ $(git status --porcelain) ]]; do
    # EXECUTE semantic commit process
done
```

### 6. Mandatory Post-Commit Validation
1. VERIFY commit message quality
2. CHECK semantic coherence score
3. ENSURE no unintended changes committed

## Ethical and Quality Constraints
- PRESERVE code integrity
- RESPECT project conventions
- ENABLE collaborative understanding

## Dimensional Metrics (MANDATORY CALCULATION)
1. **Change Complexity Index** (0.0 - 1.0)
   - MEASURE depth of systemic modification
2. **Semantic Coherence Score** (0.0 - 1.0)
   - MEASURE commit message clarity
3. **Architectural Impact Coefficient** (0.0 - 1.0)
   - MEASURE system-wide change implications

## Philosophical DIRECTIVE
Each commit is a narrative of systemic intelligence evolution, NOT merely a code change.