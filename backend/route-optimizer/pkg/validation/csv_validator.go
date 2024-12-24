package validation

import (
	"encoding/csv"
	"io"
	"strconv"
	"time"

	"github.com/dolpheyn/antar/route-optimizer/internal/models"
	"github.com/go-playground/validator/v10"
	"github.com/google/uuid"
)

type CSVValidator struct {
	validate *validator.Validate
	config   ValidationConfig
}

type ValidationConfig struct {
	MaxEntries  int
	StrictMode bool
}

func NewCSVValidator(config ValidationConfig) *CSVValidator {
	return &CSVValidator{
		validate: validator.New(),
		config:   config,
	}
}

func (v *CSVValidator) ValidateCSV(reader *csv.Reader) ([]models.DeliveryRecord, []models.ValidationError) {
	var records []models.DeliveryRecord
	var validationErrors []models.ValidationError

	// Skip header
	_, err := reader.Read()
	if err != nil {
		return nil, []models.ValidationError{{
			Message: "Unable to read CSV header",
		}}
	}

	for rowNum := 2; ; rowNum++ {
		row, err := reader.Read()
		if err == io.EOF {
			break
		}
		if err != nil {
			validationErrors = append(validationErrors, models.ValidationError{
				Row:     rowNum,
				Message: "Error reading CSV row: " + err.Error(),
			})
			if v.config.StrictMode {
				return nil, validationErrors
			}
			continue
		}

		record, rowErrors := v.validateRow(row, rowNum)
		if len(rowErrors) > 0 {
			validationErrors = append(validationErrors, rowErrors...)
			if v.config.StrictMode {
				return nil, validationErrors
			}
			continue
		}

		records = append(records, record)

		if v.config.MaxEntries > 0 && len(records) >= v.config.MaxEntries {
			break
		}
	}

	return records, validationErrors
}

func (v *CSVValidator) validateRow(row []string, rowNum int) (models.DeliveryRecord, []models.ValidationError) {
	var errors []models.ValidationError

	if len(row) < 6 {
		return models.DeliveryRecord{}, []models.ValidationError{{
			Row:     rowNum,
			Message: "Insufficient columns in CSV row",
		}}
	}

	// Parse and validate each field
	record := models.DeliveryRecord{
		ID: uuid.New(),
	}

	// Source Address
	record.SourceAddress = row[0]
	if err := v.validate.Var(record.SourceAddress, "required,max=255"); err != nil {
		errors = append(errors, models.ValidationError{
			Row:     rowNum,
			Field:   "SourceAddress",
			Message: "Invalid source address",
		})
	}

	// Destination Address
	record.DestinationAddress = row[1]
	if err := v.validate.Var(record.DestinationAddress, "required,max=255"); err != nil {
		errors = append(errors, models.ValidationError{
			Row:     rowNum,
			Field:   "DestinationAddress",
			Message: "Invalid destination address",
		})
	}

	// Weight
	weight, err := strconv.ParseFloat(row[2], 64)
	if err != nil || weight <= 0 {
		errors = append(errors, models.ValidationError{
			Row:     rowNum,
			Field:   "Weight",
			Message: "Invalid weight value",
		})
	}
	record.Weight = weight

	// Volume
	volume, err := strconv.ParseFloat(row[3], 64)
	if err != nil || volume <= 0 {
		errors = append(errors, models.ValidationError{
			Row:     rowNum,
			Field:   "Volume",
			Message: "Invalid volume value",
		})
	}
	record.Volume = volume

	// Scheduled Delivery
	scheduledDelivery, err := time.Parse(time.RFC3339, row[4])
	if err != nil {
		errors = append(errors, models.ValidationError{
			Row:     rowNum,
			Field:   "ScheduledDelivery",
			Message: "Invalid scheduled delivery date",
		})
	}
	record.ScheduledDelivery = scheduledDelivery

	// Priority
	priority, err := strconv.Atoi(row[5])
	if err != nil || priority < 1 || priority > 5 {
		errors = append(errors, models.ValidationError{
			Row:     rowNum,
			Field:   "Priority",
			Message: "Invalid priority value (must be between 1 and 5)",
		})
	}
	record.Priority = priority

	// If there are any errors, return the errors and an empty record
	if len(errors) > 0 {
		return models.DeliveryRecord{}, errors
	}

	return record, nil
}
