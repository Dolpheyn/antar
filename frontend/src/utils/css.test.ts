import { test, expect } from 'bun:test';
import { cn } from './css';

test('merges class names correctly', () => {
  const result = cn('test-class', 'another-class', { 'conditional-class': true });
  expect(result).toContain('test-class');
  expect(result).toContain('another-class');
  expect(result).toContain('conditional-class');
});

test('handles falsy values', () => {
  const result = cn('test-class', null, undefined, false, { 'conditional-class': false });
  expect(result).toBe('test-class');
});
