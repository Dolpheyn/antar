package services

import (
	"encoding/csv"
	"io"
	"time"

	"github.com/dolpheyn/antar/route-optimizer/internal/models"
	"github.com/dolpheyn/antar/route-optimizer/pkg/validation"
	"go.uber.org/zap"
)

type CSVProcessorService struct {
	logger    *zap.Logger
	validator *validation.CSVValidator
	config    validation.ValidationConfig
}

type ProcessingMetrics struct {
	TotalRecords     int
	ValidRecords     int
	InvalidRecords   int
	ProcessingTime   time.Duration
	MemoryAllocated  uint64
}

func NewCSVProcessorService(logger *zap.Logger, config validation.ValidationConfig) *CSVProcessorService {
	return &CSVProcessorService{
		logger:    logger,
		config:    config,
		validator: validation.NewCSVValidator(config),
	}
}

func (s *CSVProcessorService) ProcessCSV(csvReader io.Reader) (models.CSVUploadResponse, ProcessingMetrics) {
	start := time.Now()

	// Create CSV reader
	reader := csv.NewReader(csvReader)
	reader.FieldsPerRecord = -1 // Allow variable number of fields

	// Validate CSV
	records, validationErrors := validation.NewCSVValidator(validation.ValidationConfig{
		MaxEntries:  s.config.MaxEntries,
		StrictMode: s.config.StrictMode,
	}).ValidateCSV(reader)

	// Compute metrics
	metrics := ProcessingMetrics{
		TotalRecords:    len(records) + len(validationErrors),
		ValidRecords:    len(records),
		InvalidRecords:  len(validationErrors),
		ProcessingTime:  time.Since(start),
	}

	// Log processing metrics
	s.logProcessingMetrics(metrics)

	// Prepare response
	response := models.CSVUploadResponse{
		TotalRecords:     metrics.TotalRecords,
		ValidRecords:     metrics.ValidRecords,
		InvalidRecords:   metrics.InvalidRecords,
		ValidationErrors: validationErrors,
	}

	return response, metrics
}

func (s *CSVProcessorService) logProcessingMetrics(metrics ProcessingMetrics) {
	s.logger.Info("CSV Processing Completed",
		zap.Int("total_records", metrics.TotalRecords),
		zap.Int("valid_records", metrics.ValidRecords),
		zap.Int("invalid_records", metrics.InvalidRecords),
		zap.Duration("processing_time", metrics.ProcessingTime),
	)
}
