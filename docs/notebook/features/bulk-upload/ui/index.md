# Bulk Upload UI Design

## Design System Integration

The bulk upload interface follows our core design system principles while introducing specialized components for handling large-scale data operations.

## Color Palette

```css
:root {
  /* Primary Actions */
  --upload-primary: #2563eb;
  --upload-primary-hover: #1d4ed8;
  
  /* Status Colors */
  --validation-success: #059669;
  --validation-error: #dc2626;
  --validation-warning: #d97706;
  
  /* Background States */
  --dropzone-idle: #f8fafc;
  --dropzone-active: #e0f2fe;
  --dropzone-error: #fee2e2;
}
```

## Typography

| Element | Font | Weight | Size | Line Height |
|---------|------|---------|------|-------------|
| Section Title | Inter | 600 | 24px | 32px |
| Table Header | Inter | 500 | 14px | 20px |
| Data Text | Inter | 400 | 14px | 20px |
| Status Text | Inter | 500 | 12px | 16px |
| Helper Text | Inter | 400 | 12px | 16px |

## Spacing System

```css
:root {
  --spacing-xs: 0.25rem;  /* 4px */
  --spacing-sm: 0.5rem;   /* 8px */
  --spacing-md: 1rem;     /* 16px */
  --spacing-lg: 1.5rem;   /* 24px */
  --spacing-xl: 2rem;     /* 32px */
}
```

## Layout Grid

- Container max-width: 1280px
- Column grid: 12 columns
- Gutter width: 24px
- Margin: 16px (mobile) / 32px (desktop)

## Responsive Breakpoints

```css
:root {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
}
```
