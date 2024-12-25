import { describe, it, expect, vi } from 'vitest';
import { render, fireEvent } from '@testing-library/react';
import { Button } from '@/components/ui/button';

describe('Button Component', () => {
  it('renders with default variant and size', () => {
    const { getByRole } = render(<Button>Click me</Button>);
    const button = getByRole('button');
    
    expect(button).toHaveTextContent('Click me');
    expect(button).toHaveClass('bg-primary');
    expect(button).toHaveClass('h-10');
    expect(button).toHaveClass('px-4');
  });

  it('renders with different variants', () => {
    const { getByRole: getDestructive } = render(<Button variant="destructive">Delete</Button>);
    const { getByRole: getOutline } = render(<Button variant="outline">Outline</Button>);
    const { getByRole: getSecondary } = render(<Button variant="secondary">Secondary</Button>);

    const destructiveButton = getDestructive('button');
    const outlineButton = getOutline('button');
    const secondaryButton = getSecondary('button');

    expect(destructiveButton).toHaveClass('bg-destructive');
    expect(outlineButton).toHaveClass('border');
    expect(secondaryButton).toHaveClass('bg-secondary');
  });

  it('renders with different sizes', () => {
    const { getByRole: getSmall } = render(<Button size="sm">Small</Button>);
    const { getByRole: getLarge } = render(<Button size="lg">Large</Button>);
    const { getByRole: getIcon } = render(<Button size="icon">Icon</Button>);

    const smallButton = getSmall('button');
    const largeButton = getLarge('button');
    const iconButton = getIcon('button');

    expect(smallButton).toHaveClass('h-9');
    expect(largeButton).toHaveClass('h-11');
    expect(iconButton).toHaveClass('h-10 w-10');
  });

  it('handles click events', () => {
    const handleClick = vi.fn();
    const { getByRole } = render(<Button onClick={handleClick}>Click me</Button>);
    const button = getByRole('button');
    
    fireEvent.click(button);
    expect(handleClick).toHaveBeenCalledTimes(1);
  });

  it('renders as a child component when asChild is true', () => {
    const { container } = render(
      <Button asChild>
        <a href="/test">Link Button</a>
      </Button>
    );
    
    const link = container.querySelector('a');
    expect(link).toHaveTextContent('Link Button');
  });

  it('applies additional className', () => {
    const { getByRole } = render(<Button className="custom-class">Custom</Button>);
    const button = getByRole('button');
    
    expect(button).toHaveClass('custom-class');
  });

  it('disables button when disabled prop is true', () => {
    const { getByRole } = render(<Button disabled>Disabled</Button>);
    const button = getByRole('button');
    
    expect(button).toBeDisabled();
    expect(button).toHaveClass('disabled:opacity-50');
  });
});
