# Testing Examples

## Unit Test (Vitest)
```typescript
import { describe, it, expect } from 'vitest';
import { formatDeliveryStatus } from '@/lib/utils';

describe('Delivery Utility Functions', () => {
  it('formats delivery status correctly', () => {
    expect(formatDeliveryStatus('pending')).toBe('Pending');
    expect(formatDeliveryStatus('completed')).toBe('Completed');
  });
});
```

## Component Test (Playwright)
```typescript
import { test, expect } from '@playwright/experimental-ct-react';
import DeliveryCard from '@/components/DeliveryCard';

test('renders delivery card with interaction', async ({ mount }) => {
  const onDetailClick = vi.fn();
  const component = await mount(
    <DeliveryCard 
      delivery={mockDelivery} 
      onDetailClick={onDetailClick} 
    />
  );
  
  await component.getByText('View Details').click();
  expect(onDetailClick).toHaveBeenCalledTimes(1);
});
```

## E2E Test (Playwright)
```typescript
import { test, expect } from '@playwright/test';

test('complete delivery creation workflow', async ({ page }) => {
  await page.goto('/dashboard');
  
  await page.click('button:has-text("New Delivery")');
  await page.fill('input[name="customer"]', 'Test Customer');
  await page.click('button[type="submit"]');
  
  await expect(page.locator('text=Test Customer')).toBeVisible();
  await expect(page.locator('text=Pending')).toBeVisible();
});
```

*Last Updated*: 2024-12-22
