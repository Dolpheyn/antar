# Antar Bulk CSV Upload - Technical Implementation Specification

## 🏗️ Project Initialization & Structure

### Project Bootstrap Commands
```bash
# Create project directory
mkdir -p backend/route-optimizer/cmd/api
mkdir -p backend/route-optimizer/internal/handlers
mkdir -p backend/route-optimizer/internal/models
mkdir -p backend/route-optimizer/internal/services
mkdir -p backend/route-optimizer/pkg/validation
mkdir -p backend/route-optimizer/scripts

# Initialize Go module
cd backend/route-optimizer
go mod init github.com/dolpheyn/antar/route-optimizer
```

### Project Structure
```
backend/route-optimizer/
│
├── cmd/
│   └── api/
│       └── main.go          # Application entry point
│
├── internal/
│   ├── handlers/
│   │   └── csv_upload.go    # HTTP request handlers
│   ├── models/
│   │   └── delivery.go      # Data models
│   └── services/
│       └── csv_processor.go # Business logic
│
├── pkg/
│   └── validation/
│       └── csv_validator.go # Reusable validation logic
│
├── scripts/
│   ├── setup.sh             # Development environment setup
│   └── deploy.sh            # Deployment scripts
│
├── config.yaml              # Configuration management
├── go.mod
└── go.sum
```

### Dependency Management
```bash
# Install core dependencies
go get -u github.com/gofiber/fiber/v2
go get -u go.uber.org/zap
go get -u github.com/go-playground/validator/v10

# Development dependencies
go get -u github.com/stretchr/testify
go get -u github.com/swaggo/swag/cmd/swag
```

### Configuration Management
```yaml
# config.yaml
server:
  port: 8080
  max_upload_size: 5242880  # 5MB in bytes

validation:
  max_entries: 200
  strict_mode: true

logging:
  level: info
  output_paths:
    - stdout
    - /var/log/antar/route-optimizer.log
```

### Justfile for Common Tasks
```justfile
# Build the application
build:
    go build -o bin/api cmd/api/main.go

# Run the application
run:
    go run cmd/api/main.go

# Run tests
test:
    go test ./... -cover

# Run linter
lint:
    golangci-lint run

# Generate API documentation
generate-docs:
    swag init -g cmd/api/main.go
```

## 🚀 Technical Architecture Overview

### Design Philosophy
- **Zero-Allocation Performance**: Minimize garbage collection overhead
- **Streaming Processing**: Handle large files without full memory load
- **Robust Error Handling**: Comprehensive validation with minimal performance penalty

### Technology Stack
- **Language**: Go 1.21+ (with generics and performance optimizations)
- **Web Framework**: `github.com/gofiber/fiber/v2` (fastest HTTP router)
- **CSV Parsing**: Custom implementation with `encoding/csv`
- **Validation**: `github.com/go-playground/validator/v10`
- **Logging**: `go.uber.org/zap` for structured, performant logging

## 🔍 Detailed Component Design

### 1. CSV Upload Handler
```go
type DeliveryUploadHandler struct {
    validator *validator.Validate
    logger    *zap.Logger
    storage   FileStorageService
}

type DeliveryRecord struct {
    DeliveryID       string  `validate:"required,alphanum"`
    PickupLat        float64 `validate:"required,latitude"`
    PickupLon        float64 `validate:"required,longitude"`
    DropoffLat       float64 `validate:"required,latitude"`
    DropoffLon       float64 `validate:"required,longitude"`
}

func (h *DeliveryUploadHandler) HandleBulkUploadCSV(c *fiber.Ctx) error {
    // High-performance file handling
    file, err := c.FormFile("csv")
    if err != nil {
        return handleUploadError(err)
    }

    // Stream-based processing
    records, validationErrors := h.processCSVStream(file)
    
    return c.JSON(UploadResponse{
        UploadID:        generateUniqueID(),
        TotalEntries:    len(records),
        ProcessedEntries: len(records) - len(validationErrors),
        ValidationErrors: validationErrors,
    })
}
```

### 2. CSV Streaming Processor
```go
func (h *DeliveryUploadHandler) processCSVStream(file *multipart.FileHeader) ([]DeliveryRecord, []ValidationError) {
    src, _ := file.Open()
    defer src.Close()

    reader := csv.NewReader(src)
    reader.FieldsPerRecord = 5  // Strict column count
    
    var records []DeliveryRecord
    var validationErrors []ValidationError

    // Zero-allocation CSV parsing
    for {
        record, err := reader.Read()
        if err == io.EOF {
            break
        }
        if err != nil {
            // Handle parsing errors
            continue
        }

        deliveryRecord := parseRecord(record)
        if err := h.validator.Struct(deliveryRecord); err != nil {
            validationErrors = append(validationErrors, mapValidationError(err))
            continue
        }

        records = append(records, deliveryRecord)
    }

    return records, validationErrors
}
```

### 3. Performance Optimization Techniques
- **Zero-Copy Parsing**: Minimize memory allocations
- **Streaming Processing**: Process files without loading entirely into memory
- **Concurrent Validation**: Use goroutines for parallel record validation
- **Preallocated Slices**: Reduce memory fragmentation

### 4. Error Handling Strategy
```go
type ValidationError struct {
    Row     int    `json:"row"`
    Column  string `json:"column"`
    Message string `json:"error"`
}

func mapValidationError(err error) ValidationError {
    // Convert validator errors to structured format
    // Provides clear, actionable feedback
}
```

## 🛡️ Security Considerations
- **File Size Limit**: 5MB hard cap
- **Sanitization**: Strict type conversion
- **Temporary Storage**: Secure, ephemeral file handling
- **Rate Limiting**: Implemented via middleware

## 🧪 Testing Strategy
- **Unit Tests**: Validate individual component behaviors
- **Integration Tests**: End-to-end upload scenarios
- **Benchmark Tests**: Ensure performance under load
- **Chaos Testing**: Validate error handling

### Performance Benchmarks
```go
func BenchmarkCSVUpload(b *testing.B) {
    // Simulate various file sizes and complexities
    // Measure:
    // - Processing time
    // - Memory allocations
    // - CPU usage
}
```

## 🚧 Potential Improvements
- Machine learning-based anomaly detection
- Advanced geospatial validation
- Support for more complex CSV structures
- Real-time validation metrics

## 💡 Interesting Tech Choices
- Using `fiber` for its raw performance
- Custom validation over generic libraries
- Stream-based processing philosophy

## 🔬 Monitoring & Observability
- Prometheus metrics endpoint
- Distributed tracing support
- Detailed performance logging

## 📊 Expected Performance Characteristics
- **Latency**: < 50ms for 200-entry CSV
- **Memory Usage**: < 10MB per request
- **CPU Overhead**: Minimal, constant-time parsing

---

#golang #systemdesign #performance #backend
