import { test, expect } from 'bun:test';
import { render, fireEvent } from '@testing-library/react';
import { Button } from '@/components/ui/button';

test('renders with default variant and size', () => {
  const { container } = render(<Button>Click me</Button>);
  const button = container.querySelector('button');
  
  expect(button?.textContent).toBe('Click me');
  expect(button?.classList.contains('bg-primary')).toBe(true);
  expect(button?.classList.contains('h-10')).toBe(true);
  expect(button?.classList.contains('px-4')).toBe(true);
});

test('renders with different variants', () => {
  const { container: destructiveContainer } = render(<Button variant="destructive">Delete</Button>);
  const { container: outlineContainer } = render(<Button variant="outline">Outline</Button>);
  const { container: secondaryContainer } = render(<Button variant="secondary">Secondary</Button>);

  const destructiveButton = destructiveContainer.querySelector('button');
  const outlineButton = outlineContainer.querySelector('button');
  const secondaryButton = secondaryContainer.querySelector('button');

  expect(destructiveButton?.classList.contains('bg-destructive')).toBe(true);
  expect(outlineButton?.classList.contains('border')).toBe(true);
  expect(secondaryButton?.classList.contains('bg-secondary')).toBe(true);
});

test('renders with different sizes', () => {
  const { container: smallContainer } = render(<Button size="sm">Small</Button>);
  const { container: largeContainer } = render(<Button size="lg">Large</Button>);
  const { container: iconContainer } = render(<Button size="icon">Icon</Button>);

  const smallButton = smallContainer.querySelector('button');
  const largeButton = largeContainer.querySelector('button');
  const iconButton = iconContainer.querySelector('button');

  expect(smallButton?.classList.contains('h-9')).toBe(true);
  expect(largeButton?.classList.contains('h-11')).toBe(true);
  expect(iconButton?.classList.contains('h-10')).toBe(true);
  expect(iconButton?.classList.contains('w-10')).toBe(true);
});

test('handles click events', () => {
  let clicked = false;
  const handleClick = () => { clicked = true; };
  const { container } = render(<Button onClick={handleClick}>Click me</Button>);
  const button = container.querySelector('button');
  
  if (button) {
    fireEvent.click(button);
    expect(clicked).toBe(true);
  } else {
    throw new Error('Button not found');
  }
});

test('renders as a child component when asChild is true', () => {
  const { getByText } = render(
    <Button asChild>
      <a href="/test">Child Link</a>
    </Button>
  );
  const childLink = getByText('Child Link');
  expect(childLink).toBeTruthy();
});

test('applies additional className', () => {
  const { container } = render(<Button className="custom-class">Custom Class</Button>);
  const button = container.querySelector('button');
  
  expect(button?.classList.contains('custom-class')).toBe(true);
});

test('disables button when disabled prop is true', () => {
  const { container } = render(<Button disabled>Disabled</Button>);
  const button = container.querySelector('button');
  
  expect(button?.hasAttribute('disabled')).toBe(true);
});
