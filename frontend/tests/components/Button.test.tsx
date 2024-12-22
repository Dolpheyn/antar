import { describe, it, expect } from 'vitest';

// Simple button component for testing
const TestButton = ({ children, onClick }: { 
  children: React.ReactNode, 
  onClick?: () => void 
}) => {
  return {
    type: 'button',
    props: { children, onClick },
    render: () => `<button>${children}</button>`
  };
};

describe('Button Component', () => {
  it('renders correctly', () => {
    const button = TestButton({ children: 'Click me' });
    
    expect(button.type).toBe('button');
    expect(button.props.children).toBe('Click me');
    expect(button.render()).toBe('<button>Click me</button>');
  });

  it('handles click events', () => {
    let clicked = false;
    const button = TestButton({ 
      children: 'Click me', 
      onClick: () => { clicked = true } 
    });
    
    button.props.onClick?.();
    expect(clicked).toBe(true);
  });
});
