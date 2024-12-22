# Semantic Git Commit Workflow

## 🎯 Core Objective
Systematically transform git changes into meaningful, conventional commits by:
1. Detecting all pending changes
2. Analyzing complete diff context
3. Semantically clustering changes
4. Creating precise, conventional commits

## Conventional Commits Primer
### Commit Message Structure
```
<type>(<optional scope>): <description>

<optional body>

<optional footer>
```

### Commit Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting, missing semicolons
- `refactor`: Code restructuring
- `test`: Adding/modifying tests
- `chore`: Maintenance tasks

## Workflow Algorithm
```bash
while [[ -n "$(git status --porcelain)" ]]; do
    # 1. Detect Change Types
    detect_change_types() {
        # Categorize changes:
        # - Staged changes
        # - Unstaged changes
        # - Untracked files
    }

    # 2. Generate Comprehensive Diff
    generate_diff() {
        # Intelligently select diff source:
        # - If staged changes: git diff --staged
        # - If unstaged changes: git diff
        # - If mixed: handle each category
    }

    # 3. Semantic Change Analysis
    analyze_changes() {
        # Deep semantic clustering:
        # - Group by change type (feat/fix/docs)
        # - Consider logical dependencies
        # - Assess architectural impact
    }

    # 4. Staging and Committing
    stage_and_commit() {
        # Stage first semantic cluster
        # Generate conventional commit message
        # Commit with precise description
    }

    # Execute workflow steps
    detect_change_types
    generate_diff
    analyze_changes
    stage_and_commit
done
```

## Semantic Clustering Principles
1. **Logical Coherence**
   - Group changes that belong together
   - Maintain minimal, focused commits
   - Preserve code narrative

2. **Conventional Commit Alignment**
   - Match changes to appropriate commit types
   - Provide clear, concise descriptions
   - Include optional detailed explanations

## Workflow Termination
Workflow completes when:
- `git status --porcelain` returns empty
- All changes processed semantically
- No pending modifications in repository

## Quality Constraints
- Preserve code integrity
- Respect project conventions
- Enable collaborative understanding

## Philosophical Directive
Each commit is a precise communication of systemic change, 
not just a technical modification.
