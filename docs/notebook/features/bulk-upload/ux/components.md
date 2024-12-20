# UX Components

Our bulk upload interface is composed of carefully designed components that work together to create a seamless user experience. Each component is crafted to be both intuitive and powerful, supporting users from novice to expert.

## Component Hierarchy

```mermaid
graph TD
    A[Bulk Upload Interface] --> B[Upload Zone]
    A --> C[Data Preview]
    A --> D[Route Groups]
    A --> E[Status Components]
    
    B --> B1[Drop Area]
    B --> B2[File Selection]
    B --> B3[Progress]
    
    C --> C1[Data Table]
    C --> C2[Validation]
    C --> C3[Filters]
    
    D --> D1[Map View]
    D --> D2[Group List]
    D --> D3[Controls]
    
    E --> E1[Loading]
    E --> E2[Error]
    E --> E3[Success]
```

## Upload Zone

The upload zone is the user's first point of interaction with our system. It must inspire confidence and provide clear feedback throughout the upload process.

### File Drop Area
```mermaid
classDiagram
    class UploadZone {
        +dragActive: boolean
        +fileList: File[]
        +uploadProgress: number
        +uploadStatus: string
        +errorMessage: string
        +onDrop(files: FileList)
        +onDragOver(event: DragEvent)
        +onDragLeave(event: DragEvent)
        +validateFile(file: File): boolean
        +startUpload(file: File): Promise
        +updateProgress(progress: number)
        +handleError(error: Error)
    }
```

**Specifications:**
- Dimensions: 400x200px (minimum)
- Padding: 24px
- Border: 2px dashed (default state)
- Border radius: 8px
- Background: Light gray (idle) / Light blue (drag over)

**States:**
1. Idle
   - Default border
   - Upload icon centered
   - "Drop files here" text
2. Drag Over
   - Highlighted border
   - Background color change
   - "Release to upload" text
3. Uploading
   - Progress bar visible
   - Cancel button available
   - File name display
4. Error
   - Error message display
   - Reset button
   - Error icon

### File Selection Button
- Primary button style
- Icon: upload cloud (24x24px)
- Text: "Choose File" or "Browse"
- Position: Center of upload zone
- Hover/Focus states defined

## Data Preview

The data preview section provides a comprehensive view of uploaded data with powerful editing capabilities.

### Preview Table Architecture

```mermaid
classDiagram
    class DataTable {
        +columns: Column[]
        +data: Row[]
        +sortConfig: SortConfig
        +filterConfig: FilterConfig
        +selectedRows: string[]
        +sort(column: string)
        +filter(criteria: FilterCriteria)
        +selectRow(id: string)
        +editCell(rowId: string, field: string)
        +validate()
    }
    
    class Column {
        +field: string
        +header: string
        +type: DataType
        +editable: boolean
        +validator: Function
    }
    
    class Row {
        +id: string
        +data: Record
        +errors: ValidationError[]
        +status: RowStatus
    }
    
    DataTable --> Column
    DataTable --> Row
```

### Preview Table Specifications
- Header height: 48px
- Row height: 40px
- Cell padding: 12px
- Border: 1px solid (light gray)
- Sticky header with shadow
- Alternating row colors
- Error highlighting (left border red)
- Inline editing with double-click
- Column sorting with indicators
- Search/filter functionality

### Validation Status Component
```mermaid
stateDiagram-v2
    [*] --> Validating
    Validating --> Valid
    Validating --> Invalid
    Invalid --> Fixing
    Fixing --> Validating
    Valid --> [*]
```

**Status Indicators:**
- Color-coded status (green/yellow/red)
- Error count with severity levels
- Quick-fix suggestions tooltip
- Bulk edit action buttons

## Route Groups

The route group interface combines spatial and list-based views for effective delivery management.

### Map View Component
```mermaid
classDiagram
    class MapView {
        +center: LatLng
        +zoom: number
        +markers: Marker[]
        +routes: Route[]
        +selectedGroup: string
        +panTo(latLng: LatLng)
        +setZoom(level: number)
        +selectMarker(id: string)
        +drawRoute(points: LatLng[])
        +updateGroups(groups: Group[])
    }
```

**Map Features:**
- Interactive map component (Leaflet/Google Maps)
- Custom marker clustering
- Route visualization with colors
- Group color coding (distinct colors)
- Zoom and pan controls
- Address markers with tooltips

### Group Management Interface
```mermaid
graph TD
    A[Group List] --> B[Group Card]
    B --> C[Delivery Items]
    B --> D[Statistics]
    B --> E[Actions]
    
    C --> C1[Item List]
    C --> C2[Drag Handle]
    
    D --> D1[Count]
    D --> D2[Distance]
    D --> D3[Time]
    
    E --> E1[Optimize]
    E --> E2[Split]
    E --> E3[Merge]
```

**Features:**
- Drag-and-drop interface
- Real-time group statistics
- Optimization controls
- Manual adjustment tools
- Group performance metrics

## Status Components

### Loading States
```mermaid
stateDiagram-v2
    [*] --> Initial
    Initial --> Loading
    Loading --> Processing
    Processing --> Complete
    Loading --> Error
    Processing --> Error
    Error --> Initial
    Complete --> [*]
```

**Progress Indicators:**
- Upload progress bar (linear)
- Processing spinner (circular)
- Step completion checklist
- Time estimates (dynamic)
- Cancel option

### Error Handling
```mermaid
graph TD
    A[Error Detected] --> B{Error Type}
    B -->|Validation| C[Inline Error]
    B -->|System| D[Toast Message]
    B -->|Critical| E[Error Modal]
    C --> F[Quick Fix]
    D --> G[Retry Option]
    E --> H[Support Contact]
```

**Error Components:**
- Toast notifications (auto-dismiss)
- Inline validation markers
- Error summary panel
- Recovery suggestion buttons
- Support contact information

### Success Feedback
```mermaid
sequenceDiagram
    participant U as User
    participant S as System
    participant F as Feedback
    U->>S: Complete Action
    S->>F: Trigger Success
    F->>U: Show Animation
    F->>U: Display Summary
    F->>U: Show Next Steps
```

**Success Elements:**
- Success animation (checkmark)
- Order summary card
- Next steps guidance
- Download options
- Action buttons
