package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"

	osrm "github.com/dolpheyn/antar/backend/osrm-sdk"
)

func main() {
	// Create OSRM client
	client := osrm.NewClient("http://localhost:5000")

	// Prepare route request
	req := osrm.RouteRequest{
		Coordinates: []osrm.Coordinate{
			{Longitude: 101.62917384709634, Latitude: 3.107824318483157},
			{Longitude: 101.61640928213977, Latitude: 3.1468522006525212},
		},
		Profile: osrm.ProfileDriving,
		GenerateSteps: false,
		Overview: osrm.OverviewFalse,
	}

	// Send route request
	resp, err := client.Route(context.Background(), req)
	if err != nil {
		log.Fatalf("Error sending route request: %v", err)
	}

	// Pretty print the response
	prettyJSON, err := json.MarshalIndent(resp, "", "  ")
	if err != nil {
		log.Fatalf("Error formatting JSON: %v", err)
	}

	fmt.Println(string(prettyJSON))
}
