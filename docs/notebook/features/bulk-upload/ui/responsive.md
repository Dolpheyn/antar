# Responsive Design

## Breakpoint System

### Core Breakpoints
```css
/* Mobile First Approach */
:root {
  --breakpoint-sm: 640px;   /* Small devices */
  --breakpoint-md: 768px;   /* Medium devices */
  --breakpoint-lg: 1024px;  /* Large devices */
  --breakpoint-xl: 1280px;  /* Extra large devices */
}
```

## Component Adaptations

### Upload Zone
```css
.upload-zone {
  padding: var(--spacing-md);
  margin: var(--spacing-md);
}

@media (min-width: 768px) {
  .upload-zone {
    padding: var(--spacing-xl);
    margin: var(--spacing-xl);
  }
}
```

### Data Table
```css
/* Mobile View */
.table-responsive {
  display: block;
  width: 100%;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

/* Card View for Mobile */
@media (max-width: 767px) {
  .table-row {
    display: flex;
    flex-direction: column;
    padding: var(--spacing-md);
    border: 1px solid var(--border);
    border-radius: 8px;
    margin-bottom: var(--spacing-md);
  }

  .table-cell {
    display: grid;
    grid-template-columns: 120px 1fr;
    padding: var(--spacing-xs) 0;
  }
}
```

### Route Groups
```css
.route-groups-grid {
  display: grid;
  gap: var(--spacing-md);
}

@media (min-width: 768px) {
  .route-groups-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 1024px) {
  .route-groups-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

## Layout Adjustments

### Container
```css
.container {
  width: 100%;
  padding-right: var(--spacing-md);
  padding-left: var(--spacing-md);
  margin-right: auto;
  margin-left: auto;
}

@media (min-width: 640px) {
  .container {
    max-width: 640px;
  }
}

@media (min-width: 768px) {
  .container {
    max-width: 768px;
  }
}

@media (min-width: 1024px) {
  .container {
    max-width: 1024px;
  }
}

@media (min-width: 1280px) {
  .container {
    max-width: 1280px;
  }
}
```

### Navigation
```css
.nav-tabs {
  display: flex;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

@media (min-width: 768px) {
  .nav-tabs {
    overflow: visible;
    justify-content: center;
  }
}
```

## Touch Interactions

### Mobile-specific Styles
```css
@media (max-width: 767px) {
  /* Larger touch targets */
  .button, 
  .input, 
  .select {
    min-height: 44px;
  }

  /* Touch-friendly spacing */
  .interactive-element {
    margin: var(--spacing-md) 0;
  }

  /* Disable hover states */
  .hover-effect {
    display: none;
  }
}
```
