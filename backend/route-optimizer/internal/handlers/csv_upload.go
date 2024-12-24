package handlers

import (
	"net/http"

	"github.com/dolpheyn/antar/route-optimizer/internal/services"
	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
)

type DeliveryUploadHandler struct {
	logger     *zap.Logger
	csvService *services.CSVProcessorService
}

func NewDeliveryUploadHandler(logger *zap.Logger, csvService *services.CSVProcessorService) *DeliveryUploadHandler {
	return &DeliveryUploadHandler{
		logger:     logger,
		csvService: csvService,
	}
}

func (h *DeliveryUploadHandler) UploadCSV(c *gin.Context) {
	// Retrieve the uploaded file
	file, err := c.FormFile("csv_file")
	if err != nil {
		h.logger.Error("File upload error", zap.Error(err))
		c.JSON(http.StatusBadRequest, gin.H{
			"error": "Invalid file upload",
		})
		return
	}

	// Open the file
	src, err := file.Open()
	if err != nil {
		h.logger.Error("Error opening uploaded file", zap.Error(err))
		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "Could not process file",
		})
		return
	}
	defer src.Close()

	// Process the CSV
	_, metrics := h.csvService.ProcessCSV(src)

	// Log processing metrics
	h.logger.Info("CSV Upload Processing Metrics",
		zap.Int("total_records", metrics.TotalRecords),
		zap.Int("valid_records", metrics.ValidRecords),
		zap.Int("invalid_records", metrics.InvalidRecords),
		zap.Duration("processing_time", metrics.ProcessingTime),
	)

	// Determine response status based on validation results
	status := http.StatusOK
	if metrics.InvalidRecords > 0 {
		status = http.StatusPartialContent
	}

	// Return response
	c.JSON(status, gin.H{
		"total_records":   metrics.TotalRecords,
		"valid_records":   metrics.ValidRecords,
		"invalid_records": metrics.InvalidRecords,
	})
}
