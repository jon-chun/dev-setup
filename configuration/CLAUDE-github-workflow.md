* [Claude Code + GitHub WORKFLOW for Complex Apps (18:40) (25 Jun 2025)](https://www.youtube.com/watch?v=FjHtZnjNEBU&t=71s)
- [https://docs.github.com/en/get-started/using-github/github-flow](https://docs.github.com/en/get-started/using-github/github-flow)
- [gh install](https://cli.github.com/)
- [https://www.anthropic.com/engineering/claude-code-best-practices](https://www.anthropic.com/engineering/claude-code-best-practices)
- [https://fly.io/blog/youre-all-nuts/](https://fly.io/blog/youre-all-nuts/)

# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a simple static landing page repository for "The Human-AI Algorithm" YouTube video. The project consists of a single HTML file with embedded CSS and is designed for demonstration purposes.

## File Structure

- `index.html` - Self-contained landing page with embedded CSS styling
  - Features responsive design with gradient backgrounds
  - Includes video embed placeholder section
  - Contains call-to-action and footer sections

## Development Workflow

Since this is a static HTML page, no build process is required. To work with this project:

1. Open `index.html` directly in a web browser to preview changes
2. Edit the HTML file to make modifications
3. To embed a YouTube video, uncomment line 109 and replace `VIDEO_ID` with the actual YouTube video ID

## Project Context

The repository is initialized as a git repository but contains minimal configuration. There is a Python virtual environment (`.venv`) present, though no Python code currently exists in the project.






# "Merge to Main" Workflow

When the user says "merge to main", follow this complete workflow:

## Pre-Merge Preparation
1. **Pull latest main** - Fetch and merge the latest changes from remote main
2. **Validate branch naming** - Create a conventional commits conform branch using kebab-case:
   - `feat/feature-name` for new features
   - `fix/bug-name` for bug fixes
   - `docs/update-name` for documentation
   - `refactor/change-name` for code refactoring
   - `test/test-name` for test additions
   - `chore/task-name` for maintenance tasks
  
## Commit and Push
3. **Run pre-commit checks** - Execute tests and linters if applicable; report any failures
4. **Commit changes** - Use detailed conventional commits messages:
   - Format: `type(scope): description`
   - Examples: `feat(auth): add user authentication`, `fix(dashboard): resolve memory leak`
   - Include body with details if changes are complex
5. **Check for conflicts** - Ensure branch can merge cleanly with main
6. **Push branch** - Push the branch to remote
  
## Pull Request Creation
1. **Create Pull Request** - Generate PR to main with:
   - Descriptive title matching commit message format
   - Body containing: changes summary, testing done, breaking changes (if any)
   - Link related issues if applicable
   - 
## Confirmation and Merge
1. **Wait for CI/CD** - Allow automated checks to complete; report status
2. **Present summary** - Show user:
   - All commits to be merged
   - Files changed
   - CI/CD status
   - Any warnings or conflicts
3.  **Request confirmation** - Ask: "Ready to merge to main? (yes/no)"
4.  **Merge PR** - After confirmation, merge using squash or merge commit (ask user preference)
5.  **Verify merge** - Confirm merge was successful
   
## Cleanup
1.  **Delete remote branch** - Remove the feature branch from remote
2.  **Update local main** - Pull the updated main branch locally
3.  **Confirm completion** - Report successful merge with commit SHA
   
## Error Handling
- **If tests fail**: Report failures and ask whether to fix or abort
- **If merge conflicts exist**: Report conflicts and ask user to resolve manually
- **If PR creation fails**: Report error and suggest manual creation
- **If CI/CD fails**: Report failures and ask whether to fix or abort