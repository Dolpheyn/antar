package osrm

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
)

// RouteRequest represents the configuration for a route request
type RouteRequest struct {
	Coordinates []Coordinate
	Profile     Profile

	// Optional parameters
	Bearings         []Bearing
	Radiuses         []float64
	GenerateSteps    bool
	Annotations      bool
	Geometries       GeometryType
	Overview         OverviewType
	ContinueStraight bool
	Alternatives     bool
}

// Coordinate represents a geographic coordinate
type Coordinate struct {
	Longitude float64
	Latitude  float64
}

// Bearing represents the bearing at a coordinate
type Bearing struct {
	Value float64
	Range float64
}

// GeometryType defines the geometry representation
type GeometryType string

const (
	GeometryPolyline  GeometryType = "polyline"
	GeometryPolyline6 GeometryType = "polyline6"
	GeometryGeoJSON   GeometryType = "geojson"
)

// OverviewType defines the route overview detail
type OverviewType string

const (
	OverviewSimplified OverviewType = "simplified"
	OverviewFull       OverviewType = "full"
	OverviewFalse      OverviewType = "false"
)

// RouteResponse represents the OSRM route response
type RouteResponse struct {
	Code      string     `json:"code"`
	Routes    []Route    `json:"routes"`
	Waypoints []Waypoint `json:"waypoints"`
}

// Route represents a single route
type Route struct {
	Geometry   string     `json:"geometry"`
	Legs       []RouteLeg `json:"legs"`
	WeightName string     `json:"weight_name"`
	Weight     float64    `json:"weight"`
	Duration   float64    `json:"duration"`
	Distance   float64    `json:"distance"`
}

// RouteLeg represents a leg of the route
type RouteLeg struct {
	Steps    []RouteStep `json:"steps"`
	Summary  string      `json:"summary"`
	Weight   float64     `json:"weight"`
	Duration float64     `json:"duration"`
	Distance float64     `json:"distance"`
}

// RouteStep represents a step in the route
type RouteStep struct {
	Geometry string  `json:"geometry"`
	Mode     string  `json:"mode"`
	Distance float64 `json:"distance"`
	Duration float64 `json:"duration"`
}

// Waypoint represents a waypoint in the route
type Waypoint struct {
	Hint     string    `json:"hint"`
	Distance float64   `json:"distance"`
	Name     string    `json:"name"`
	Location []float64 `json:"location"`
}

// Route sends a route request to the OSRM service
func (c *Client) Route(ctx context.Context, req RouteRequest) (*RouteResponse, error) {
	// Construct coordinates string
	coordStrings := make([]string, len(req.Coordinates))
	for i, coord := range req.Coordinates {
		coordStrings[i] = fmt.Sprintf("%f,%f", coord.Longitude, coord.Latitude)
	}
	coordPath := strings.Join(coordStrings, ";")

	// Construct full URL
	fullURL := fmt.Sprintf("%s/%s", c.buildURL("route", req.Profile), coordPath)

	// Create HTTP request
	httpReq, err := http.NewRequest("GET", fullURL, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}

	// Add query parameters
	q := httpReq.URL.Query()

	if req.GenerateSteps {
		q.Add("steps", "true")
	}
	if req.Annotations {
		q.Add("annotations", "true")
	}
	if req.Geometries != "" {
		q.Add("geometries", string(req.Geometries))
	}
	if req.Overview != "" {
		q.Add("overview", string(req.Overview))
	}
	if req.ContinueStraight {
		q.Add("continue_straight", "true")
	}
	if req.Alternatives {
		q.Add("alternatives", "true")
	}

	// Add bearings if provided
	if len(req.Bearings) > 0 {
		bearingStrings := make([]string, len(req.Bearings))
		for i, bearing := range req.Bearings {
			bearingStrings[i] = fmt.Sprintf("%f,%f", bearing.Value, bearing.Range)
		}
		q.Add("bearings", strings.Join(bearingStrings, ";"))
	}

	// Add radiuses if provided
	if len(req.Radiuses) > 0 {
		radiusStrings := make([]string, len(req.Radiuses))
		for i, radius := range req.Radiuses {
			radiusStrings[i] = fmt.Sprintf("%f", radius)
		}
		q.Add("radiuses", strings.Join(radiusStrings, ";"))
	}

	httpReq.URL.RawQuery = q.Encode()

	// Send request
	resp, err := c.do(ctx, httpReq)
	if err != nil {
		return nil, fmt.Errorf("request failed: %w", err)
	}
	defer resp.Body.Close()

	// Parse response
	var routeResp RouteResponse
	if err := json.NewDecoder(resp.Body).Decode(&routeResp); err != nil {
		return nil, fmt.Errorf("failed to decode response: %w", err)
	}

	// Check response code
	if routeResp.Code != "Ok" {
		return nil, fmt.Errorf("OSRM returned error: %s", routeResp.Code)
	}

	return &routeResp, nil
}
