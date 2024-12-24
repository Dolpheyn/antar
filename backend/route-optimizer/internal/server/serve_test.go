package server

import (
	"fmt"
	"net/http"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"go.uber.org/zap/zapcore"
)

func TestServe(t *testing.T) {
	testCases := []struct {
		name           string
		config         Config
		expectedError  bool
		expectedPort   int
		validationFunc func(t *testing.T, cfg Config)
	}{
		{
			name: "Default Configuration",
			config: Config{
				Server: struct {
					Port           int `mapstructure:"port"`
					MaxUploadSize  int `mapstructure:"max_upload_size"`
				}{
					Port:           8080,
					MaxUploadSize:  5 * 1024 * 1024, // 5MB
				},
				Validation: struct {
					MaxEntries  int  `mapstructure:"max_entries"`
					StrictMode bool `mapstructure:"strict_mode"`
				}{
					MaxEntries:  200,
					StrictMode: true,
				},
				Logging: struct {
					Level       string   `mapstructure:"level"`
					OutputPaths []string `mapstructure:"output_paths"`
				}{
					Level:       "info",
					OutputPaths: []string{"stdout"},
				},
			},
			expectedError: false,
			expectedPort:  8080,
			validationFunc: func(t *testing.T, cfg Config) {
				assert.Equal(t, 8080, cfg.Server.Port)
				assert.Equal(t, 5*1024*1024, cfg.Server.MaxUploadSize)
				assert.Equal(t, 200, cfg.Validation.MaxEntries)
				assert.True(t, cfg.Validation.StrictMode)
				assert.Equal(t, "info", cfg.Logging.Level)
				assert.Contains(t, cfg.Logging.OutputPaths, "stdout")
			},
		},
		{
			name: "Custom Configuration",
			config: Config{
				Server: struct {
					Port           int `mapstructure:"port"`
					MaxUploadSize  int `mapstructure:"max_upload_size"`
				}{
					Port:           9090,
					MaxUploadSize:  10 * 1024 * 1024, // 10MB
				},
				Validation: struct {
					MaxEntries  int  `mapstructure:"max_entries"`
					StrictMode bool `mapstructure:"strict_mode"`
				}{
					MaxEntries:  500,
					StrictMode: false,
				},
				Logging: struct {
					Level       string   `mapstructure:"level"`
					OutputPaths []string `mapstructure:"output_paths"`
				}{
					Level:       "debug",
					OutputPaths: []string{"stderr"},
				},
			},
			expectedError: false,
			expectedPort:  9090,
			validationFunc: func(t *testing.T, cfg Config) {
				assert.Equal(t, 9090, cfg.Server.Port)
				assert.Equal(t, 10*1024*1024, cfg.Server.MaxUploadSize)
				assert.Equal(t, 500, cfg.Validation.MaxEntries)
				assert.False(t, cfg.Validation.StrictMode)
				assert.Equal(t, "debug", cfg.Logging.Level)
				assert.Contains(t, cfg.Logging.OutputPaths, "stderr")
			},
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Run Serve in a goroutine
			errChan := make(chan error, 1)
			go func() {
				errChan <- Serve(tc.config)
			}()

			// Give the server a moment to start
			time.Sleep(100 * time.Millisecond)

			// Validate configuration
			tc.validationFunc(t, tc.config)

			// Test server connectivity
			req, err := http.NewRequest("POST", fmt.Sprintf("http://localhost:%d/upload", tc.config.Server.Port), nil)
			require.NoError(t, err)
			resp, err := http.DefaultClient.Do(req)
			if tc.expectedError {
				require.Error(t, err)
			} else {
				require.NoError(t, err)
				defer resp.Body.Close()

				// Expect 400 Bad Request (no file uploaded)
				assert.Equal(t, http.StatusBadRequest, resp.StatusCode)
			}

			// Stop the server
			// Note: In a real-world scenario, you'd want a more graceful shutdown mechanism
		})
	}
}

func TestParseLogLevel(t *testing.T) {
	testCases := []struct {
		name          string
		inputLevel    string
		expectedLevel zapcore.Level
	}{
		{"Debug Level", "debug", zapcore.DebugLevel},
		{"Info Level", "info", zapcore.InfoLevel},
		{"Warn Level", "warn", zapcore.WarnLevel},
		{"Error Level", "error", zapcore.ErrorLevel},
		{"Fatal Level", "fatal", zapcore.FatalLevel},
		{"Unknown Level", "unknown", zapcore.InfoLevel},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			assert.Equal(t, tc.expectedLevel, parseLogLevel(tc.inputLevel))
		})
	}
}
