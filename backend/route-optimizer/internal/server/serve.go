package server

import (
	"fmt"

	"github.com/dolpheyn/antar/route-optimizer/internal/handlers"
	"github.com/dolpheyn/antar/route-optimizer/internal/services"
	"github.com/dolpheyn/antar/route-optimizer/pkg/validation"
	"github.com/gin-gonic/gin"
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

// Config represents the complete application configuration
type Config struct {
	Server struct {
		Port           int `mapstructure:"port"`
		MaxUploadSize  int `mapstructure:"max_upload_size"`
	} `mapstructure:"server"`
	
	Validation struct {
		MaxEntries  int  `mapstructure:"max_entries"`
		StrictMode bool `mapstructure:"strict_mode"`
	} `mapstructure:"validation"`
	
	Logging struct {
		Level       string   `mapstructure:"level"`
		OutputPaths []string `mapstructure:"output_paths"`
	} `mapstructure:"logging"`
}

// Serve starts the HTTP server with the given configuration
func Serve(cfg Config) error {
	// Initialize logger
	loggerConfig := zap.Config{
		Level:       zap.NewAtomicLevelAt(parseLogLevel(cfg.Logging.Level)),
		Development: false,
		Sampling: &zap.SamplingConfig{
			Initial:    100,
			Thereafter: 100,
		},
		Encoding:         "json",
		EncoderConfig:    zap.NewProductionEncoderConfig(),
		OutputPaths:      cfg.Logging.OutputPaths,
		ErrorOutputPaths: []string{"stderr"},
	}

	logger, err := loggerConfig.Build()
	if err != nil {
		return fmt.Errorf("failed to create logger: %w", err)
	}
	defer logger.Sync()

	// Create CSV processor service
	csvConfig := validation.ValidationConfig{
		MaxEntries:  cfg.Validation.MaxEntries,
		StrictMode: cfg.Validation.StrictMode,
	}
	csvService := services.NewCSVProcessorService(logger, csvConfig)

	// Create upload handler
	uploadHandler := handlers.NewDeliveryUploadHandler(logger, csvService)

	// Setup Gin router
	router := gin.Default()

	// Configure max file upload size
	router.MaxMultipartMemory = int64(cfg.Server.MaxUploadSize)

	// Routes
	router.POST("/upload", uploadHandler.UploadCSV)

	// Start server
	serverAddr := fmt.Sprintf(":%d", cfg.Server.Port)
	logger.Info("Starting server", zap.String("address", serverAddr))
	
	return router.Run(serverAddr)
}

// parseLogLevel converts string log level to zapcore.Level
func parseLogLevel(level string) zapcore.Level {
	switch level {
	case "debug":
		return zapcore.DebugLevel
	case "info":
		return zapcore.InfoLevel
	case "warn":
		return zapcore.WarnLevel
	case "error":
		return zapcore.ErrorLevel
	case "fatal":
		return zapcore.FatalLevel
	default:
		return zapcore.InfoLevel
	}
}
