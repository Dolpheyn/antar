package models

import (
	"time"

	"github.com/google/uuid"
)

type DeliveryRecord struct {
	ID                 uuid.UUID `json:"id" validate:"required"`
	SourceAddress      string    `json:"source_address" validate:"required,max=255"`
	DestinationAddress string    `json:"destination_address" validate:"required,max=255"`
	Weight             float64   `json:"weight" validate:"gte=0,lte=1000"`
	Volume             float64   `json:"volume" validate:"gte=0,lte=100"`
	ScheduledDelivery  time.Time `json:"scheduled_delivery" validate:"required"`
	Priority           int       `json:"priority" validate:"gte=1,lte=5"`
}

type ValidationError struct {
	Row     int    `json:"row"`
	Field   string `json:"field"`
	Message string `json:"message"`
}

type CSVUploadResponse struct {
	TotalRecords     int               `json:"total_records"`
	ValidRecords     int               `json:"valid_records"`
	InvalidRecords   int               `json:"invalid_records"`
	ValidationErrors []ValidationError `json:"validation_errors,omitempty"`
}
