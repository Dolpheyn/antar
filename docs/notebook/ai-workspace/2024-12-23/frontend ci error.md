# Frontend CI Error: Missing Jest DOM Testing Library

## Problem
- Failed to resolve `@testing-library/jest-dom` import
- Missing dependency in `package.json`
- Affects both `Button.test.tsx` and `utils.test.ts`

## Root Cause
The `@testing-library/jest-dom` package was not installed in the project's dev dependencies.

## Solution
1. Add `@testing-library/jest-dom` to `devDependencies` in `package.json`:
```json
"devDependencies": {
  "@testing-library/jest-dom": "^6.3.0"
}
```

## Verification Steps
- Install dependencies
- Run unit tests
- Ensure all imports work correctly

## Potential Impact
- Resolves import errors in test files
- Enables proper DOM-based testing
- Improves test reliability

## Recommended Actions
- Update `package.json`
- Reinstall dependencies
- Rerun frontend tests

## The error log is as follows:
```
$ vitest
The CJS build of Vite's Node API is deprecated. See https://vite.dev/guide/troubleshooting.html#vite-cjs-node-api-deprecated for more details.

 RUN  v2.1.8 /home/runner/work/antar/antar/frontend

 ❯ tests/components/Button.test.tsx (0 test)
 ❯ tests/unit/utils.test.ts (0 test)

⎯⎯⎯⎯⎯⎯ Failed Suites 2 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  tests/components/Button.test.tsx [ tests/components/Button.test.tsx ]
Error: Failed to resolve import "@testing-library/jest-dom" from "test-setup.ts". Does the file exist?
  Plugin: vite:import-analysis
  File: /home/runner/work/antar/antar/frontend/test-setup.ts:2:7
  1  |  import "@testing-library/jest-dom";
     |          ^
  2  |  import * as matchers from "@testing-library/jest-dom/matchers";
  3  |  import { expect } from "vitest";
 ❯ TransformPluginContext._formatError node_modules/vite/dist/node/chunks/dep-CB_7IfJ-.js:49255:41
 ❯ TransformPluginContext.error node_modules/vite/dist/node/chunks/dep-CB_7IfJ-.js:49250:16
 ❯ normalizeUrl node_modules/vite/dist/node/chunks/dep-CB_7IfJ-.js:64041:23
 ❯ node_modules/vite/dist/node/chunks/dep-CB_7IfJ-.js:64173:39
 ❯ TransformPluginContext.transform node_modules/vite/dist/node/chunks/dep-CB_7IfJ-.js:64100:7
 ❯ PluginContainer.transform node_modules/vite/dist/node/chunks/dep-CB_7IfJ-.js:49096:18
 ❯ loadAndTransform node_modules/vite/dist/node/chunks/dep-CB_7IfJ-.js:51929:27

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/2]⎯

 FAIL  tests/unit/utils.test.ts [ tests/unit/utils.test.ts ]
Error: Failed to resolve import "@testing-library/jest-dom" from "test-setup.ts". Does the file exist?
  Plugin: vite:import-analysis
  File: /home/runner/work/antar/antar/frontend/test-setup.ts:2:7
  1  |  import "@testing-library/jest-dom";
     |          ^
  2  |  import * as matchers from "@testing-library/jest-dom/matchers";
  3  |  import { expect } from "vitest";
 ❯ TransformPluginContext._formatError node_modules/vite/dist/node/chunks/dep-CB_7IfJ-.js:49255:41
 ❯ TransformPluginContext.error node_modules/vite/dist/node/chunks/dep-CB_7IfJ-.js:49250:16
 ❯ normalizeUrl node_modules/vite/dist/node/chunks/dep-CB_7IfJ-.js:64041:23
 ❯ node_modules/vite/dist/node/chunks/dep-CB_7IfJ-.js:64173:39
 ❯ TransformPluginContext.transform node_modules/vite/dist/node/chunks/dep-CB_7IfJ-.js:64100:7
 ❯ PluginContainer.transform node_modules/vite/dist/node/chunks/dep-CB_7IfJ-.js:49096:18
 ❯ loadAndTransform node_modules/vite/dist/node/chunks/dep-CB_7IfJ-.js:51929:27

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[2/2]⎯

 Test Files  2 failed (2)
      Tests  no tests
   Start at  02:34:46
   Duration  719ms (transform 14ms, setup 0ms, collect 0ms, tests 0ms, environment 828ms, prepare 199ms)

error: script "test:unit" exited with code 1
Error: Process completed with exit code 1.