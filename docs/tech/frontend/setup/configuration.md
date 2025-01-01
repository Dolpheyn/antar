# Project Configuration

## Bun Configuration
Create a `bunfig.toml` in the project root:
```toml
[install]
# Prefer workspace dependencies
prefer-workspace-packages = true

[test]
# Default test runner configuration
runner = "vitest"

[lint]
# ESLint configuration
enabled = true
```

## TypeScript Configuration
`tsconfig.json`:
```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "node",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx"],
  "exclude": ["node_modules"]
}
```

## Project Structure
```plaintext
antar/
├── src/
│   ├── app/
│   ├── components/
│   ├── hooks/
│   ├── lib/
│   ├── styles/
│   └── types/
├── public/
├── components.json
├── bunfig.toml
└── tests/
```

*Last Updated*: 2024-12-22
