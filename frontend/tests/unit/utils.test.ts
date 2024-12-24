import { describe, it, expect } from 'vitest';
import { cn } from '../../src/utils/css';

describe('Utility Functions', () => {
  it('merges class names correctly', () => {
    const result = cn('test-class', 'another-class', { 'conditional-class': true });
    expect(result).toContain('test-class');
    expect(result).toContain('another-class');
    expect(result).toContain('conditional-class');
  });

  it('handles falsy values', () => {
    const result = cn('base-class', null, undefined, false, { 'conditional': false });
    expect(result).toBe('base-class');
  });
});
