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
