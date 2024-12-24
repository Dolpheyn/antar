package services

import (
	"bytes"
	"testing"

	"github.com/dolpheyn/antar/route-optimizer/internal/models"
	"github.com/dolpheyn/antar/route-optimizer/pkg/validation"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"go.uber.org/zap"
)

func TestCSVProcessorService(t *testing.T) {
	// Create a no-op logger
	logger, err := zap.NewProduction()
	require.NoError(t, err)
	defer logger.Sync()

	testCases := []struct {
		name             string
		csvContent       string
		config           validation.ValidationConfig
		expectedResponse models.CSVUploadResponse
	}{
		{
			name: "Successful CSV Processing",
			csvContent: `Source,Destination,Weight,Volume,ScheduledDelivery,Priority
New York,Los Angeles,50.5,25.0,2024-12-31T10:30:00Z,3
Chicago,Houston,75.0,30.0,2024-12-31T11:30:00Z,2`,
			config: validation.ValidationConfig{
				MaxEntries:  200,
				StrictMode: false,
			},
			expectedResponse: models.CSVUploadResponse{
				TotalRecords:   2,
				ValidRecords:   2,
				InvalidRecords: 0,
			},
		},
		{
			name: "CSV with Invalid Record",
			csvContent: `Source,Destination,Weight,Volume,ScheduledDelivery,Priority
New York,Los Angeles,-50.5,25.0,2024-12-31T10:30:00Z,3
Chicago,Houston,75.0,30.0,2024-12-31T11:30:00Z,2`,
			config: validation.ValidationConfig{
				MaxEntries:  200,
				StrictMode: false,
			},
			expectedResponse: models.CSVUploadResponse{
				TotalRecords:   2,
				ValidRecords:   1,
				InvalidRecords: 1,
			},
		},
		{
			name: "Strict Mode with Invalid Record",
			csvContent: `Source,Destination,Weight,Volume,ScheduledDelivery,Priority
New York,Los Angeles,-50.5,25.0,2024-12-31T10:30:00Z,3
Chicago,Houston,75.0,30.0,2024-12-31T11:30:00Z,2`,
			config: validation.ValidationConfig{
				MaxEntries:  200,
				StrictMode: true,
			},
			expectedResponse: models.CSVUploadResponse{
				TotalRecords:   1,
				ValidRecords:   0,
				InvalidRecords: 1,
			},
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Create CSV reader from string
			csvReader := bytes.NewBufferString(tc.csvContent)

			// Create CSV processor service
			service := NewCSVProcessorService(logger, tc.config)

			// Process CSV
			response, metrics := service.ProcessCSV(csvReader)

			// Assertions
			assert.Equal(t, tc.expectedResponse.TotalRecords, response.TotalRecords)
			assert.Equal(t, tc.expectedResponse.ValidRecords, response.ValidRecords)
			assert.Equal(t, tc.expectedResponse.InvalidRecords, response.InvalidRecords)

			// Validate metrics
			assert.Equal(t, tc.expectedResponse.TotalRecords, metrics.TotalRecords)
			assert.Equal(t, tc.expectedResponse.ValidRecords, metrics.ValidRecords)
			assert.Equal(t, tc.expectedResponse.InvalidRecords, metrics.InvalidRecords)
			assert.NotZero(t, metrics.ProcessingTime)
		})
	}
}

func TestProcessingMetrics(t *testing.T) {
	metrics := ProcessingMetrics{
		TotalRecords:    100,
		ValidRecords:    80,
		InvalidRecords:  20,
		ProcessingTime:  1000000, // 1ms
		MemoryAllocated: 1024,
	}

	assert.Equal(t, 100, metrics.TotalRecords)
	assert.Equal(t, 80, metrics.ValidRecords)
	assert.Equal(t, 20, metrics.InvalidRecords)
	assert.NotZero(t, metrics.ProcessingTime)
	assert.Equal(t, uint64(1024), metrics.MemoryAllocated)
}
