# API Specifications

## API Overview
Our API is designed for simplicity and efficiency, focusing on bulk operations and route optimization.

## Endpoints

### Bulk Operations

#### Upload Orders
```yaml
POST /api/v1/orders/bulk
Description: Upload multiple orders via CSV or JSON
Authentication: Required
Content-Type: multipart/form-data

Parameters:
  - file: File (CSV/JSON)
  - merchant_id: string
```

#### Get Batch Status
```yaml
GET /api/v1/orders/bulk/{batchId}
Description: Check status of a bulk upload
Authentication: Required
```

### Route Management

#### Optimize Routes
```yaml
POST /api/v1/routes/optimize
Description: Generate optimized routes for orders
Authentication: Required
Content-Type: application/json

Body:
{
  "orders": ["order_id_1", "order_id_2"],
  "constraints": {
    "time_window": {
      "start": "datetime",
      "end": "datetime"
    },
    "priority": "string"
  }
}
```

## Authentication
- Bearer token authentication
- API keys for server-to-server
- Rate limiting per client

## Error Handling
Standard error response format:
```yaml
{
  "error": string,
  "message": string,
  "details": object
}
```

## Rate Limits
- 100 requests per minute per client
- Bulk uploads: 5 per minute
- Route optimizations: 10 per minute
