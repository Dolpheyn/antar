# Antar Route Optimization API Design

## API Specification

### 1. Bulk CSV Upload Endpoint
```
POST /api/v1/deliveries/bulk-upload-csv
```
#### Request
- Content-Type: multipart/form-data
- File: CSV file with delivery data

#### Request Body
- CSV file containing delivery information
- Expected CSV Columns:
  * delivery_id
  * pickup_latitude
  * pickup_longitude
  * dropoff_latitude
  * dropoff_longitude

#### Response Codes
- 200 OK: Successful file upload and initial validation
- 400 Bad Request: Invalid file format
- 413 Payload Too Large: File exceeds size limits

#### Response Body
```json
{
  "upload_id": "unique_upload_identifier",
  "total_entries": 200,
  "processed_entries": 180,
  "failed_entries": 20,
  "validation_errors": [
    {
      "row": 5,
      "column": "delivery_id",
      "error": "Invalid format"
    }
  ]
}
```

## CSV File Validation Rules
1. File Size Limits
   - Soft Limit: 1 MB
   - Hard Limit: 5 MB

2. Delivery ID Validation
   - Must be unique
   - Non-empty
   - Alphanumeric characters only

3. Coordinate Validation
   - Latitude Range: -90 to 90
   - Longitude Range: -180 to 180
   - Must be valid decimal numbers

## Security Considerations
- File upload size restrictions
- Basic input sanitization
- Temporary file storage with automatic cleanup

## Error Handling
- Provide detailed error messages
- Highlight specific rows with issues
- Support partial upload of valid rows

## Performance Considerations
- Quick initial validation
- Efficient CSV parsing
- Minimal processing overhead

## Future Expansion Points
- Route optimization endpoint
- Detailed error reporting
- File download for error logs
