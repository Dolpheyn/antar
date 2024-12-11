# API Specifications

## REST APIs

### Order Management

#### Create Order
```yaml
POST /api/v1/orders
Content-Type: application/json

{
  "merchantId": "string",
  "pickup": {
    "address": "string",
    "contact": "string"
  },
  "delivery": {
    "address": "string",
    "contact": "string"
  }
}
```

#### Get Order Status
```yaml
GET /api/v1/orders/{orderId}
```

## WebSocket APIs

### Real-time Updates
```yaml
WS /ws/v1/orders/{orderId}/updates
```
