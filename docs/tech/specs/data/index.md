# Data Models

## Core Models

### Order
```mermaid
classDiagram
    class Order {
        +String id
        +String batchId
        +String merchantId
        +Location pickup
        +Location dropoff
        +TimeWindow timeWindow
        +String priority
        +String status
        +DateTime createdAt
        +DateTime updatedAt
    }

    class Location {
        +String address
        +Float latitude
        +Float longitude
        +String contactName
        +String contactPhone
    }

    class TimeWindow {
        +DateTime start
        +DateTime end
    }
```

### Route
```mermaid
classDiagram
    class Route {
        +String id
        +List~Order~ orders
        +Provider provider
        +Float cost
        +Int duration
        +DateTime startTime
        +String status
    }

    class Provider {
        +String id
        +String name
        +PricingModel pricing
        +List~String~ supportedAreas
    }
```

## Data Validation

### Order Validation
- Required fields
  - merchantId
  - pickup.address
  - dropoff.address
  - timeWindow
- Optional fields
  - priority (default: normal)
  - batchId

### Route Validation
- Required fields
  - orders (min: 1)
  - provider
- Optional fields
  - startTime (default: ASAP)

## Status Flows

### Order Status
1. PENDING
2. PROCESSING
3. OPTIMIZED
4. ASSIGNED
5. IN_PROGRESS
6. COMPLETED
7. FAILED

### Route Status
1. PLANNING
2. OPTIMIZED
3. ASSIGNED
4. IN_PROGRESS
5. COMPLETED
6. FAILED
