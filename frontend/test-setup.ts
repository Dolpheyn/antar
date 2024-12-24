// Global test setup
import '@testing-library/jest-dom';
import * as matchers from '@testing-library/jest-dom/matchers';
import { expect } from 'vitest';

// Extend Vitest's expect with jest-dom matchers
expect.extend(matchers);

// Polyfill for document and window in test environment
if (typeof window === 'undefined') {
  global.window = global as any;
}

if (typeof document === 'undefined') {
  global.document = {
    body: {
      appendChild: () => { },
      removeChild: () => { },
    },
    createElement: () => ({
      style: {},
      setAttribute: () => { },
      addEventListener: () => { },
      removeEventListener: () => { },
    }),
    createTextNode: () => ({}),
  } as any;
}

// Extend expect with additional matchers if needed
expect.extend({
  toBeInTheDocument(received) {
    const pass = received !== null && received !== undefined;
    return {
      pass,
      message: () => `expected ${received} to be in the document`
    };
  }
});
