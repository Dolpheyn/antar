# Bulk Upload Flow

## Overview

The bulk upload flow is designed to help users efficiently upload and process multiple deliveries at once. The system guides users through a series of well-defined stages, each with clear objectives and feedback mechanisms.

## User Journey Map

```mermaid
journey
    title Bulk Upload User Journey
    section Upload
        Choose file method: 5: User
        Select/Drop file: 3: User
        Validate format: 3: System
    section Validation
        Review data: 5: User
        Fix errors: 4: User
        Verify addresses: 3: System
    section Route Planning
        View groups: 5: User
        Adjust routes: 4: User
        Optimize: 3: System
    section Confirmation
        Review summary: 5: User
        Confirm changes: 4: User
        Complete upload: 3: System
```

## Detailed Flow Diagram

```mermaid
flowchart TB
    Start([Start]) --> Upload[Upload CSV]
    Upload --> Validate{Validate Format}
    Validate -->|Invalid| ShowError[Show Error Message]
    ShowError --> Upload
    Validate -->|Valid| Preview[Show Data Preview]
    Preview --> EditData{Edit Data?}
    EditData -->|Yes| EditRows[Edit Row Data]
    EditRows --> Preview
    EditData -->|No| Process[Process Data]
    Process --> RouteGroups[Show Route Groups]
    RouteGroups --> AdjustGroups{Adjust Groups?}
    AdjustGroups -->|Yes| ModifyGroups[Modify Groups]
    ModifyGroups --> RouteGroups
    AdjustGroups -->|No| Confirm{Confirm Upload?}
    Confirm -->|No| Cancel([Cancel])
    Confirm -->|Yes| Submit[Submit Deliveries]
    Submit --> Success([Success])

    subgraph Upload Process
        Upload
        Validate
        ShowError
    end

    subgraph Data Validation
        Preview
        EditData
        EditRows
        Process
    end

    subgraph Route Management
        RouteGroups
        AdjustGroups
        ModifyGroups
    end

    subgraph Completion
        Confirm
        Submit
        Success
    end
```

## Stage Details

### 1. Upload Stage

```mermaid
stateDiagram-v2
    [*] --> Idle
    Idle --> FileSelected: Choose File
    Idle --> DragOver: File Dragged
    DragOver --> Validating: File Dropped
    FileSelected --> Validating: File Selected
    Validating --> Error: Invalid Format
    Validating --> Processing: Valid Format
    Error --> Idle: Reset
    Processing --> Preview: Complete
```

#### File Selection
- **Drag-and-Drop Zone**
  - Active area: 400x200px minimum
  - Visual feedback on hover/drag
  - Supported file types: CSV
  - Max file size: 10MB

- **Manual Selection**
  - Browse button placement: Center
  - File picker: Native OS
  - Multiple file support: No

#### Format Validation
- **Required Columns**
  - Delivery ID (unique)
  - Customer Name
  - Delivery Address
  - Contact Number
  - Time Window
  - Package Details

- **Template Support**
  - Download template button
  - Sample data row
  - Column descriptions
  - Format guidelines

### 2. Validation Stage

```mermaid
sequenceDiagram
    participant U as User
    participant S as System
    participant V as Validator
    
    U->>S: Upload File
    S->>V: Validate Format
    V-->>S: Format OK
    S->>V: Validate Data
    V-->>S: Show Issues
    S->>U: Display Preview
    U->>S: Edit Data
    S->>V: Revalidate
    V-->>S: All Valid
    S->>U: Enable Proceed
```

#### Data Preview
- **Table View**
  - Pagination: 50 rows/page
  - Column sorting
  - Quick filters
  - Search functionality
  - Row selection

- **Validation Rules**
  | Field | Validation | Error Message |
  |-------|------------|---------------|
  | ID | Unique | Duplicate delivery ID |
  | Name | Required | Customer name required |
  | Address | Geocodable | Invalid address format |
  | Contact | Format check | Invalid phone number |
  | Time | Range check | Outside operation hours |

#### Error Management
- **Visual Indicators**
  - Row level: Left border (red)
  - Cell level: Background (light red)
  - Field level: Icon with tooltip

- **Bulk Operations**
  - Select all with errors
  - Bulk edit similar errors
  - Copy/paste from Excel
  - Undo/redo support

### 3. Route Planning Stage

```mermaid
graph TD
    A[Load Deliveries] --> B{Group Algorithm}
    B -->|Distance| C[Distance-based]
    B -->|Time| D[Time-window]
    B -->|Hybrid| E[Mixed Mode]
    C --> F[Show Groups]
    D --> F
    E --> F
    F --> G{Manual Adjust}
    G -->|Yes| H[Drag-Drop]
    G -->|No| I[Finalize]
```

#### Route Groups
- **Map View**
  - Zoom levels: 10-18
  - Marker clustering
  - Route lines with direction
  - Group color coding
  - Interactive markers

- **Group Management**
  - Drag-drop between groups
  - Auto-rebalance option
  - Split/merge groups
  - Optimize button

#### Optimization
- **Algorithms**
  - Distance-based grouping
  - Time-window clustering
  - Vehicle capacity check
  - Route efficiency score

### 4. Confirmation Stage

```mermaid
stateDiagram-v2
    [*] --> ReviewSummary
    ReviewSummary --> ConfirmDialog: Proceed
    ReviewSummary --> EditGroups: Back
    ConfirmDialog --> Processing: Confirm
    ConfirmDialog --> ReviewSummary: Cancel
    Processing --> Success: Complete
    Processing --> Error: Failed
    Error --> ReviewSummary: Retry
    Success --> [*]
```

#### Final Review
- **Summary View**
  - Total deliveries
  - Group distribution
  - Cost estimation
  - Time projections

- **Confirmation Dialog**
  - Clear action buttons
  - Review checklist
  - Terms acceptance
  - Cancel option

## Error Handling

### System States
```mermaid
stateDiagram-v2
    [*] --> Normal
    Normal --> Warning: Minor Issue
    Normal --> Error: Major Issue
    Warning --> Normal: Resolved
    Error --> Normal: Fixed
    Error --> Fatal: Unrecoverable
    Fatal --> [*]: Restart
```

### Error Types
1. **Validation Errors**
   - Field-level validation
   - Business rule violations
   - Format inconsistencies
   - Missing required data

2. **System Errors**
   - Network timeout
   - Server errors
   - File corruption
   - Memory limits

### Recovery Mechanisms
- Auto-save every 30 seconds
- Local storage backup
- Session recovery
- Error retry logic

## Success Scenarios

### Completion States
```mermaid
sequenceDiagram
    participant U as User
    participant S as System
    participant D as Database
    
    U->>S: Confirm Upload
    S->>D: Save Data
    D-->>S: Success
    S->>U: Show Animation
    S->>U: Display Summary
    S->>U: Offer Download
    U->>S: Download Receipt
    S->>U: Complete
```

### Success Actions
1. **Visual Feedback**
   - Success animation
   - Confetti effect
   - Status update
   - Summary card

2. **Next Steps**
   - Download receipt
   - View deliveries
   - Start tracking
   - Share results

3. **Follow-up**
   - Email confirmation
   - Track link
   - Support contact
   - Feedback request
