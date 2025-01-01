# Project Setup Guide

## Bun Installation
```bash
# Install Bun (macOS, Linux, WSL)
curl -fsSL https://bun.sh/install | bash

# Verify installation
bun --version
```

## Create Next.js Project
```bash
bunx create-next-app@latest antar \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir
cd antar
```

## Development Workflow
```bash
# Start development server
bun dev

# Build for production
bun run build

# Run tests
bun test

# Lint the project
bun lint
```

*Last Updated*: 2024-12-22
