# How to Create Meaningful Git Commits: A Step-by-Step Guide

## Your Mission
You're going to transform your code changes into clear, meaningful git commits that tell a story about what you've done.

## Before You Start: Understanding Commit Types
Think of commits like chapters in a book. Each type describes a different kind of change:
- `feat`: You've added something new (like a cool feature)
- `fix`: You've repaired a bug
- `docs`: You've updated documentation
- `style`: You've made formatting changes
- `refactor`: You've restructured code without changing its behavior
- `test`: You've modified or added tests
- `chore`: You've done maintenance work

## The Commit Message Formula
Your commit message should look like this:
```
<type>(<optional area>): Short, clear description

(Optional longer explanation if needed)
```

## The Workflow: From Changes to Commits

### Step 1: Check What's Changed
- Look at your git status
- Identify different types of changes:
  * Staged changes (ready to commit)
  * Unstaged changes (modified but not added)
  * Untracked files (brand new files)

### Step 2: Examine the Entire Difference
- Generate a comprehensive diff
- If you have staged changes, look at staged diff
- If you have unstaged changes, look at unstaged diff
- Handle mixed changes carefully

### Step 3: Understand the Changes Deeply
- Group your changes logically
- Ask yourself:
  * What type of change is this?
  * Are these changes related?
  * Do they belong in the same commit?

### Step 4: Stage and Commit
- Stage the first logical group of changes
- Write a commit message that explains:
  * What changed
  * Why it changed
  * Any important details

### Step 5: Repeat
- Keep doing this until ALL changes are committed
- Stop when `git status` shows nothing left to commit

## Pro Tips
- Keep commits small and focused
- Tell a clear story with your commits
- Think about how another developer would understand your changes

## The Big Picture
Each commit is more than code - it's a communication about your project's evolution. Make it count!
