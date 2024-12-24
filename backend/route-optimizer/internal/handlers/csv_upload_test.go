package handlers

import (
	"bytes"
	"mime/multipart"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/dolpheyn/antar/route-optimizer/internal/services"
	"github.com/dolpheyn/antar/route-optimizer/pkg/validation"
	"github.com/gin-gonic/gin"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"go.uber.org/zap"
)

func setupTestRouter(handler *DeliveryUploadHandler) *gin.Engine {
	gin.SetMode(gin.TestMode)
	router := gin.Default()
	router.POST("/upload", handler.UploadCSV)
	return router
}

func createCSVMultipartRequest(csvContent string) (*http.Request, error) {
	// Create a buffer to store the multipart form data
	body := &bytes.Buffer{}
	writer := multipart.NewWriter(body)

	// Create a CSV file part
	part, err := writer.CreateFormFile("csv_file", "test.csv")
	if err != nil {
		return nil, err
	}

	// Write CSV content to the part
	_, err = part.Write([]byte(csvContent))
	if err != nil {
		return nil, err
	}

	// Close the multipart writer
	err = writer.Close()
	if err != nil {
		return nil, err
	}

	// Create the request
	req, err := http.NewRequest("POST", "/upload", body)
	if err != nil {
		return nil, err
	}
	req.Header.Set("Content-Type", writer.FormDataContentType())

	return req, nil
}

func TestDeliveryUploadHandler(t *testing.T) {
	// Create a no-op logger
	logger, err := zap.NewProduction()
	require.NoError(t, err)
	defer logger.Sync()

	testCases := []struct {
		name             string
		csvContent       string
		config           validation.ValidationConfig
		expectedStatus   int
	}{
		{
			name: "Successful CSV Upload",
			csvContent: `Source,Destination,Weight,Volume,ScheduledDelivery,Priority
New York,Los Angeles,50.5,25.0,2024-12-31T10:30:00Z,3
Chicago,Houston,75.0,30.0,2024-12-31T11:30:00Z,2`,
			config: validation.ValidationConfig{
				MaxEntries:  200,
				StrictMode: false,
			},
			expectedStatus: http.StatusOK,
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
			expectedStatus: http.StatusPartialContent,
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
			expectedStatus: http.StatusPartialContent,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Create CSV processor service
			csvService := services.NewCSVProcessorService(logger, tc.config)

			// Create upload handler
			uploadHandler := NewDeliveryUploadHandler(logger, csvService)

			// Setup router
			router := setupTestRouter(uploadHandler)

			// Create multipart request with CSV
			req, err := createCSVMultipartRequest(tc.csvContent)
			require.NoError(t, err)

			// Create response recorder
			w := httptest.NewRecorder()

			// Perform the request
			router.ServeHTTP(w, req)

			// Assertions
			assert.Equal(t, tc.expectedStatus, w.Code)
		})
	}
}

func TestDeliveryUploadHandlerErrorCases(t *testing.T) {
	// Create a no-op logger
	logger, err := zap.NewProduction()
	require.NoError(t, err)
	defer logger.Sync()

	testCases := []struct {
		name             string
		requestSetup     func(req *http.Request)
		expectedStatus   int
		expectedMessage  string
	}{
		{
			name: "No File Uploaded",
			requestSetup: func(req *http.Request) {
				req.Header.Set("Content-Type", "multipart/form-data")
			},
			expectedStatus:  http.StatusBadRequest,
			expectedMessage: "Invalid file upload",
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Create CSV processor service
			csvService := services.NewCSVProcessorService(logger, validation.ValidationConfig{
				MaxEntries:  200,
				StrictMode: false,
			})

			// Create upload handler
			uploadHandler := NewDeliveryUploadHandler(logger, csvService)

			// Setup router
			router := setupTestRouter(uploadHandler)

			// Create request
			req, err := http.NewRequest("POST", "/upload", nil)
			require.NoError(t, err)

			// Apply request setup
			if tc.requestSetup != nil {
				tc.requestSetup(req)
			}

			// Create response recorder
			w := httptest.NewRecorder()

			// Perform the request
			router.ServeHTTP(w, req)

			// Assertions
			assert.Equal(t, tc.expectedStatus, w.Code)
		})
	}
}
