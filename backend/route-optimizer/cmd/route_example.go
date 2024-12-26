package main

import (
	"context"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"log"
	"math"
	"os"
	"sort"
	"strconv"
	"sync"

	osrm "github.com/dolpheyn/antar/backend/osrm-sdk"
)

func loadDropOffPoints(filename string) ([]osrm.Coordinate, error) {
	csvFile, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	defer csvFile.Close()
	csvReader := csv.NewReader(csvFile)
	records, err := csvReader.ReadAll()
	if err != nil {
		return nil, err
	}
	dropOffPoints := make([]osrm.Coordinate, 0, len(records))
	for _, record := range records {
		lon, err := strconv.ParseFloat(record[0], 64)
		if err != nil {
			return nil, err
		}
		lat, err := strconv.ParseFloat(record[1], 64)
		if err != nil {
			return nil, err
		}
		dropOffPoints = append(dropOffPoints, osrm.Coordinate{
			Longitude: lon,
			Latitude:  lat,
		})
	}
	return dropOffPoints, nil
}

// clusterDropOffPoints takes a list of drop off points and groups them into clusters
// by dividing the circle around the pickup point into sectors.
// The angle parameter controls the angle of each sector, in degrees.
// The function returns a slice of clusters, where each cluster is a slice of
// coordinates.
func clusterDropOffPoints(dropOffPoints []osrm.Coordinate, pickupPoint osrm.Coordinate, angle float64) ([][]osrm.Coordinate, error) {
	if angle <= 0 || angle >= 360 {
		return nil, fmt.Errorf("angle must be between 0 and 360, got %f", angle)
	}

	type PolarPoint struct {
		Coordinate osrm.Coordinate
		Angle      float64
	}

	// Slice the map as a pizza, where the pickup point is the centerpoint
	// each slice's angle is controlled by the "angle" parameter
	// group dropOffPoints in the same slice together

	// Calculate angle and distance from pickup point
	polarPoints := make([]PolarPoint, len(dropOffPoints))
	for i, point := range dropOffPoints {
		// Calculate angle (in radians)
		dx := point.Longitude - pickupPoint.Longitude
		dy := point.Latitude - pickupPoint.Latitude
		polarAngle := math.Atan2(dy, dx)
		if polarAngle < 0 {
			polarAngle += 2 * math.Pi
		}

		polarPoints[i] = PolarPoint{
			Coordinate: point,
			Angle:      polarAngle * 180 / math.Pi,
		}
	}

	// Sort points by angle
	sort.Slice(polarPoints, func(i, j int) bool {
		return polarPoints[i].Angle < polarPoints[j].Angle
	})

	// Divide the circle into sectors
	numClusters := int(360 / angle)
	fmt.Println(numClusters)

	// Create clusters
	clusters := make([][]osrm.Coordinate, numClusters)

	// Distribute points into clusters
	for _, point := range polarPoints {
		clusterIndex := int(point.Angle / angle)
		if clusterIndex >= numClusters {
			clusterIndex = numClusters - 1
		}

		if clusters[clusterIndex] == nil {
			clusters[clusterIndex] = []osrm.Coordinate{point.Coordinate}
		} else {
			clusters[clusterIndex] = append(clusters[clusterIndex], point.Coordinate)
		}
	}

	// filter empty clusters
	for i := 0; i < len(clusters); i++ {
		if clusters[i] == nil || len(clusters[i]) == 0 {
			clusters = append(clusters[:i], clusters[i+1:]...)
			i--
		}
	}

	return clusters, nil
}

func sendRouteRequest(client *osrm.Client, pickupPoint osrm.Coordinate, dropOffPoints []osrm.Coordinate) (*osrm.RouteResponse, error) {
	if len(dropOffPoints) == 0 {
		return nil, fmt.Errorf("no drop off points provided")
	}
	resp, err := client.Route(context.Background(), osrm.RouteRequest{
		Coordinates:   append([]osrm.Coordinate{pickupPoint}, dropOffPoints...),
		Profile:       osrm.ProfileDriving,
		GenerateSteps: true,
		Annotations:   true,
		Overview:      osrm.OverviewFull,
		Geometries:    osrm.GeometryPolyline,
	})
	if err != nil {
		return nil, fmt.Errorf("error sending route request to %v: %w", dropOffPoints, err)
	}
	return resp, nil
}

func main() {
	// Create OSRM client
	client := osrm.NewClient("http://localhost:5000")
	pickupPoint := osrm.Coordinate{ // bloomthis warehouse
		Longitude: 101.62917384709634,
		Latitude:  3.107824318483157,
	}

	// load from route-optimizer/test-data/malaysia_random_points.csv
	// columns - lon,lat
	// parse to osrm.Coordinate
	dropOffPoints, err := loadDropOffPoints("test-data/malaysia_random_points.csv")
	if err != nil {
		log.Fatal(err)
	}
	clusterredDropOffPoints, err := clusterDropOffPoints(dropOffPoints, pickupPoint, 360/50)
	if err != nil {
		log.Fatal(err)
	}

	// Use semaphore to limit concurrent requests
	semaphoreSize := 10
	sem := make(chan struct{}, semaphoreSize)
	for range semaphoreSize {
		sem <- struct{}{}
	}
	wg := sync.WaitGroup{}

	routeResponses := make([]*osrm.RouteResponse, len(clusterredDropOffPoints))
	for i, dropOffPoints := range clusterredDropOffPoints {
		wg.Add(1)
		go func(i int, dropOffPoints []osrm.Coordinate) {
			<-sem
			defer wg.Done()
			defer func() { sem <- struct{}{} }()
			resp, err := sendRouteRequest(client, pickupPoint, dropOffPoints)
			if err != nil {
				log.Printf("Error sending route request to %v: %v", dropOffPoints, err)
				return
			}
			routeResponses[i] = resp
		}(i, dropOffPoints)
	}
	wg.Wait()

	// Write the array into a file
	f, err := os.Create("test-data/output.json")
	if err != nil {
		log.Fatalf("Error creating output file: %v", err)
	}
	defer f.Close()
	err = json.NewEncoder(f).Encode(routeResponses)
	if err != nil {
		log.Fatalf("Error writing to file: %v", err)
	}
}
