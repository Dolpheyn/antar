# UI Animations

## Transition Definitions

### Base Transitions
```css
:root {
  --transition-fast: 150ms ease;
  --transition-base: 200ms ease;
  --transition-slow: 300ms ease;
}
```

## Upload Zone Animations

### Drag State
```css
.upload-zone {
  transition: all var(--transition-base);
}

.upload-zone--drag-active {
  transform: scale(1.02);
  border-color: var(--upload-primary);
  background: var(--dropzone-active);
}
```

### Upload Progress
```css
@keyframes progress-pulse {
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}

.progress-bar--active {
  animation: progress-pulse 2s infinite;
}
```

## Table Interactions

### Row Hover
```css
.table-row {
  transition: background var(--transition-fast);
}

.table-row:hover {
  background: var(--surface-hover);
}
```

### Edit Mode
```css
.cell-edit {
  transition: all var(--transition-base);
}

.cell-edit--active {
  box-shadow: 0 0 0 2px var(--upload-primary);
  background: white;
}
```

## Route Group Animations

### Card Expansion
```css
.route-group__details {
  height: 0;
  opacity: 0;
  transition: all var(--transition-slow);
}

.route-group--expanded .route-group__details {
  height: auto;
  opacity: 1;
}
```

### Drag and Drop
```css
.route-group--dragging {
  transform: scale(1.02);
  box-shadow: 0 8px 16px rgba(0,0,0,0.1);
  transition: all var(--transition-base);
}
```

## Status Transitions

### Success State
```css
@keyframes success-check {
  0% { transform: scale(0); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.status-success-icon {
  animation: success-check 0.5s var(--transition-base);
}
```

### Error State
```css
@keyframes error-shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  75% { transform: translateX(4px); }
}

.status-error {
  animation: error-shake 0.4s var(--transition-base);
}
```

## Loading States

### Skeleton Loading
```css
@keyframes skeleton-loading {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

.skeleton {
  background: linear-gradient(90deg, 
    var(--skeleton-start) 25%, 
    var(--skeleton-end) 37%, 
    var(--skeleton-start) 63%
  );
  background-size: 400% 100%;
  animation: skeleton-loading 1.4s ease infinite;
}
```
