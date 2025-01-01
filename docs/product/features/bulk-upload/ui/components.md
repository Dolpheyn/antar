# UI Components

## Upload Zone Component

### Default State
```html
<div class="upload-zone">
  <div class="upload-icon">
    <svg><!-- Cloud upload icon --></svg>
  </div>
  <h3>Drop your CSV file here</h3>
  <p>or</p>
  <button class="upload-button">Browse Files</button>
  <p class="helper-text">Supported format: CSV</p>
</div>
```

```css
.upload-zone {
  border: 2px dashed var(--upload-border);
  border-radius: 8px;
  padding: var(--spacing-xl);
  background: var(--dropzone-idle);
  transition: all 0.2s ease;
}

.upload-zone:hover {
  border-color: var(--upload-primary);
}
```

## Data Table

### Header Design
```css
.table-header {
  background: var(--surface-alt);
  position: sticky;
  top: 0;
  z-index: 10;
}

.header-cell {
  padding: var(--spacing-sm) var(--spacing-md);
  font-weight: 500;
  color: var(--text-secondary);
}
```

### Row States
```css
.table-row {
  border-bottom: 1px solid var(--border);
}

.table-row:hover {
  background: var(--surface-hover);
}

.row-error {
  border-left: 3px solid var(--validation-error);
}
```

## Route Group Cards

### Card Layout
```css
.route-group {
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  padding: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-md);
}
```

## Status Indicators

### Progress Bar
```css
.progress-bar {
  height: 4px;
  background: var(--surface-alt);
  border-radius: 2px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: var(--upload-primary);
  transition: width 0.3s ease;
}
```

### Status Badges
```css
.status-badge {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.status-success {
  background: var(--validation-success-bg);
  color: var(--validation-success);
}

.status-error {
  background: var(--validation-error-bg);
  color: var(--validation-error);
}
```
