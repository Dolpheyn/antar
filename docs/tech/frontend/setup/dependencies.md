# Project Dependencies

## Core Dependencies
```bash
# Core dependencies
bun add @headlessui/react @heroicons/react
bun add @tanstack/react-query
bun add zustand immer

# Development dependencies
bun add -D @typescript-eslint/parser
bun add -D @typescript-eslint/eslint-plugin
bun add -D prettier prettier-plugin-tailwindcss
```

## shadcn/ui Setup
```bash
# Uses npx as it's a one-time setup
npx shadcn-ui@latest init
```

## Dependency Configuration Options
When running the init command, use these recommended options:
```plaintext
Would you like to use TypeScript (recommended)? yes
Which style would you like to use? › Default
Which color would you like to use as base color? › Indigo
Where is your global CSS file? › src/styles/globals.css
Do you want to use CSS variables for colors? › yes
Where is your tailwind.config.js located? › tailwind.config.js
Configure the import alias for components: › @/components
Configure the import alias for utils: › @/lib/utils
Are you using React Server Components? › yes
```

*Last Updated*: 2024-12-22
