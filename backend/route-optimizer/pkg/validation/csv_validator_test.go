package validation

import (
	"encoding/csv"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestCSVValidator(t *testing.T) {
	testCases := []struct {
		name             string
		csvContent       string
		config           ValidationConfig
		expectedRecords  int
		expectedErrors   int
	}{
		{
			name: "Successful CSV Processing",
			csvContent: `Source,Destination,Weight,Volume,ScheduledDelivery,Priority
New York,Los Angeles,50.5,25.0,2024-12-31T10:30:00Z,3
Chicago,Houston,75.0,30.0,2024-12-31T11:30:00Z,2`,
			config: ValidationConfig{
				MaxEntries:  200,
				StrictMode: false,
			},
			expectedRecords: 2,
			expectedErrors:  0,
		},
		{
			name: "CSV with Invalid Record",
			csvContent: `Source,Destination,Weight,Volume,ScheduledDelivery,Priority
New York,Los Angeles,-50.5,25.0,2024-12-31T10:30:00Z,3
Chicago,Houston,75.0,30.0,2024-12-31T11:30:00Z,2`,
			config: ValidationConfig{
				MaxEntries:  200,
				StrictMode: false,
			},
			expectedRecords: 1,
			expectedErrors:  1,
		},
		{
			name: "Strict Mode with Invalid Record",
			csvContent: `Source,Destination,Weight,Volume,ScheduledDelivery,Priority
New York,Los Angeles,-50.5,25.0,2024-12-31T10:30:00Z,3
Chicago,Houston,75.0,30.0,2024-12-31T11:30:00Z,2`,
			config: ValidationConfig{
				MaxEntries:  200,
				StrictMode: true,
			},
			expectedRecords: 0,
			expectedErrors:  1,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Create CSV reader from string
			reader := csv.NewReader(strings.NewReader(tc.csvContent))

			// Create validator
			validator := NewCSVValidator(tc.config)

			// Validate CSV
			records, validationErrors := validator.ValidateCSV(reader)

			// Assertions
			assert.Len(t, records, tc.expectedRecords, "Number of valid records")
			assert.Len(t, validationErrors, tc.expectedErrors, "Number of validation errors")
		})
	}
}

func TestValidationConfig(t *testing.T) {
	testCases := []struct {
		name           string
		maxEntries     int
		strictMode     bool
	}{
		{
			name:           "Default Config",
			maxEntries:     200,
			strictMode:     false,
		},
		{
			name:           "Strict Mode",
			maxEntries:     100,
			strictMode:     true,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			config := ValidationConfig{
				MaxEntries:  tc.maxEntries,
				StrictMode: tc.strictMode,
			}

			assert.Equal(t, tc.maxEntries, config.MaxEntries)
			assert.Equal(t, tc.strictMode, config.StrictMode)
		})
	}
}

func TestValidateRow(t *testing.T) {
	validator := NewCSVValidator(ValidationConfig{
		MaxEntries:  200,
		StrictMode: true,
	})

	testCases := []struct {
		name           string
		row            []string
		expectError    bool
		errorFieldName string
	}{
		{
			name: "Valid Row",
			row: []string{
				"New York", 
				"Los Angeles", 
				"50.5", 
				"25.0", 
				"2024-12-31T10:30:00Z", 
				"3",
			},
			expectError: false,
		},
		{
			name: "Invalid Weight",
			row: []string{
				"New York", 
				"Los Angeles", 
				"-50.5", 
				"25.0", 
				"2024-12-31T10:30:00Z", 
				"3",
			},
			expectError: true,
			errorFieldName: "Weight",
		},
		{
			name: "Invalid Address Length",
			row: []string{
				strings.Repeat("A", 300), 
				"Los Angeles", 
				"50.5", 
				"25.0", 
				"2024-12-31T10:30:00Z", 
				"3",
			},
			expectError: true,
			errorFieldName: "SourceAddress",
		},
		{
			name: "Invalid Priority",
			row: []string{
				"New York", 
				"Los Angeles", 
				"50.5", 
				"25.0", 
				"2024-12-31T10:30:00Z", 
				"6",
			},
			expectError: true,
			errorFieldName: "Priority",
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			record, errors := validator.validateRow(tc.row, 2)

			if tc.expectError {
				require.NotEmpty(t, errors, "Expected validation errors")
				assert.Contains(t, errors[0].Field, tc.errorFieldName)
			} else {
				assert.Empty(t, errors, "Expected no validation errors")
				assert.NotNil(t, record.ID, "Record should be created")
			}
		})
	}
}
