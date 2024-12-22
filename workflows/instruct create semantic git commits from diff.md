# Semantic Git Commit Workflow

## Commit Types
- `feat`: New feature or enhancement
- `fix`: Bug fix
- `docs`: Documentation updates
- `style`: Code formatting, no logic change
- `refactor`: Code restructuring
- `test`: Test-related changes
- `chore`: Maintenance tasks

## Commit Message Template
```
<type>(<scope>): Short, descriptive summary

[Detailed explanation]
- Why this change is necessary
- What problem it solves
- Any potential side effects or considerations
```

## Workflow Steps

### 1. Pre-Commit Reflection
- Understand the change's purpose
- Identify the problem being solved
- Consider the broader project context

### 2. Staging Changes
- Use `git add -p` for granular staging
- Group logically related changes
- Ensure each commit is focused and atomic

### 3. Crafting the Commit Message
- Be concise but informative
- Use present tense
- Explain the "why", not just the "what"

### 4. Commit Message Checklist
✅ Clear type prefix
✅ Optional scope for context
✅ Concise summary (50 chars max)
✅ Detailed explanation
✅ Connects to project goals

## AI-Driven Semantic Commit Workflow

### Advanced Semantic Commit Strategy

#### Workflow Phases

##### 1. Comprehensive Change Analysis
```bash
# Initial repository state assessment
git status
git diff
```

##### 2. Semantic Diff Parsing
- Analyze changes across multiple dimensions:
  * Code structure modifications
  * Logical grouping of changes
  * Identification of related modifications
  * Extraction of semantic intent

##### 3. Change Categorization Strategy
- Develop a multi-dimensional change mapping:
  * Technical scope (language/framework)
  * Functional impact
  * Architectural significance
  * Dependency modifications

##### 4. Semantic Staging and Commit Workflow
```bash
# Iterative, semantically-driven staging
git add -p  # Interactive patch staging

# Semantic commit generation
git commit -m "<type>(<scope>): Concise semantic summary

[Detailed semantic analysis]
- Rationale for change
- Systemic implications
- Potential side effects
"
```

#### Semantic Commit Planning Algorithm

1. **Change Discovery**
   - Run `git status` and `git diff`
   - Parse entire changeset
   - Identify logical change clusters

2. **Semantic Clustering**
   - Group changes by:
     * Affected components
     * Type of modification
     * Potential system impact

3. **Commit Planning**
   - Create a staged commit plan
   - Prioritize changes by:
     * Dependency resolution
     * Minimal system disruption
     * Logical coherence

4. **Iterative Staging**
   - Use `git add -p` for granular control
   - Stage changes according to semantic plan
   - Validate each staging decision

5. **Semantic Commit Generation**
   - Craft commit messages that explain:
     * WHY the change was necessary
     * WHAT systemic improvements result
     * HOW the change integrates

#### Commit Message Semantic Enrichment
- Include machine-readable metadata
- Add context beyond traditional commit messages
- Facilitate automated changelog generation

##### Example Semantic Commit
```
feat(authentication): Enhance OAuth2 token management

[Semantic Analysis]
- Resolved potential token refresh race conditions
- Improved security by implementing adaptive token rotation
- Minimal performance overhead with efficient caching strategy

Systemic Impact:
- Reduces authentication failure scenarios
- Increases system resilience
- Prepares infrastructure for future auth complexity
```

#### Best Practices
- Maintain atomic, focused commits
- Preserve logical change relationships
- Balance technical detail with readability
- Continuously refine semantic understanding

#### Tooling Recommendations
- Use semantic-release for automated versioning
- Integrate with CI/CD change tracking
- Develop custom semantic analysis scripts

## Examples

### Feature Commit
```
feat(user-auth): Implement OAuth2 login

- Adds Google and GitHub OAuth2 providers
- Enhances user authentication security
- Reduces friction in user onboarding process
```

### Refactor Commit
```
refactor(api): Simplify error handling middleware

- Consolidates error handling logic
- Improves code readability
- Reduces potential for error propagation
```

### Chore Commit
```
chore(deps): Update React and TypeScript versions

- Upgrades to latest stable versions
- Ensures compatibility with modern ecosystem
- Potential performance and security improvements
```

## Best Practices
- Commit often
- Keep commits small and focused
- Write for future maintainers
- Treat commit messages as documentation

## Continuous Improvement
- Regularly review commit history
- Discuss and refine commit practices
- Learn from team's commit narratives

*Last Updated*: 2024-12-22
