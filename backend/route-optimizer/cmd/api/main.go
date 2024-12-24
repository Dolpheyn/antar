package main

import (
	"log"

	"github.com/dolpheyn/antar/route-optimizer/internal/server"
	"github.com/spf13/viper"
)

func main() {
	// Initialize configuration
	cfg, err := loadConfig()
	if err != nil {
		log.Fatalf("Failed to load configuration: %v", err)
	}

	// Start the server
	if err := server.Serve(cfg); err != nil {
		log.Fatalf("Server failed to start: %v", err)
	}
}

func loadConfig() (server.Config, error) {
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath(".")

	// Read configuration
	if err := viper.ReadInConfig(); err != nil {
		return server.Config{}, err
	}

	// Optional: Set default values
	viper.SetDefault("server.port", 8080)
	viper.SetDefault("server.max_upload_size", 5*1024*1024) // 5MB
	viper.SetDefault("validation.max_entries", 200)
	viper.SetDefault("validation.strict_mode", true)
	viper.SetDefault("logging.level", "info")
	viper.SetDefault("logging.output_paths", []string{"stdout"})

	// Unmarshal configuration
	var cfg server.Config
	if err := viper.Unmarshal(&cfg); err != nil {
		return server.Config{}, err
	}

	return cfg, nil
}
