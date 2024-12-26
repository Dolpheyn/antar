package osrm

import (
	"context"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestRouteRequest(t *testing.T) {
	// Mock OSRM server
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Validate request parameters
		assert.Equal(t, "/route/v1/driving/101.629174,3.107824;101.616409,3.146852", r.URL.Path)

		// Send mock response
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{
			"code": "Ok",
			"routes": [{
				"geometry": "mock_geometry",
				"legs": [{
					"steps": [],
					"summary": "",
					"weight": 554.5,
					"duration": 554.5,
					"distance": 7536.8
				}],
				"weight_name": "routability",
				"weight": 554.5,
				"duration": 554.5,
				"distance": 7536.8
			}],
			"waypoints": [
				{
					"hint": "mock_hint_1",
					"distance": 19.503735740,
					"name": "Jalan 20/2",
					"location": [101.629009, 3.107884]
				},
				{
					"hint": "mock_hint_2",
					"distance": 7.629860439,
					"name": "",
					"location": [101.616476, 3.146837]
				}
			]
		}`))
	}))
	defer server.Close()

	// Create client
	client := NewClient(server.URL)

	// Prepare route request
	req := RouteRequest{
		Coordinates: []Coordinate{
			{Longitude: 101.629174, Latitude: 3.107824},
			{Longitude: 101.616409, Latitude: 3.146852},
		},
		Profile: ProfileDriving,
	}

	// Send route request
	resp, err := client.Route(context.Background(), req)

	// Validate response
	require.NoError(t, err)
	require.NotNil(t, resp)

	assert.Equal(t, "Ok", resp.Code)
	require.Len(t, resp.Routes, 1)

	route := resp.Routes[0]
	assert.Equal(t, "mock_geometry", route.Geometry)
	assert.Equal(t, "routability", route.WeightName)
	assert.Equal(t, 554.5, route.Weight)
	assert.Equal(t, 554.5, route.Duration)
	assert.Equal(t, 7536.8, route.Distance)

	require.Len(t, resp.Waypoints, 2)
	assert.Equal(t, "Jalan 20/2", resp.Waypoints[0].Name)
	assert.Equal(t, 101.629009, resp.Waypoints[0].Location[0])
	assert.Equal(t, 3.107884, resp.Waypoints[0].Location[1])
}

func TestRouteRequestWithOptions(t *testing.T) {
	testCases := []struct {
		name                string
		req                 RouteRequest
		expectedQueryParams map[string]string
	}{
		{
			name: "All Options Enabled",
			req: RouteRequest{
				Coordinates: []Coordinate{
					{Longitude: 101.629174, Latitude: 3.107824},
					{Longitude: 101.616409, Latitude: 3.146852},
				},
				Profile:          ProfileDriving,
				GenerateSteps:    true,
				Annotations:      true,
				Geometries:       GeometryPolyline6,
				Overview:         OverviewFull,
				ContinueStraight: true,
				Alternatives:     true,
			},
			expectedQueryParams: map[string]string{
				"steps":             "true",
				"annotations":       "true",
				"geometries":        "polyline6",
				"overview":          "full",
				"continue_straight": "true",
				"alternatives":      "true",
			},
		},
		{
			name: "Minimal Options",
			req: RouteRequest{
				Coordinates: []Coordinate{
					{Longitude: 101.629174, Latitude: 3.107824},
					{Longitude: 101.616409, Latitude: 3.146852},
				},
				Profile: ProfileDriving,
			},
			expectedQueryParams: map[string]string{},
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Mock OSRM server
			server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				// Validate request parameters
				assert.Equal(t, "/route/v1/driving/101.629174,3.107824;101.616409,3.146852", r.URL.Path)

				// Check query parameters
				q := r.URL.Query()
				for k, v := range tc.expectedQueryParams {
					assert.Equal(t, v, q.Get(k), "Query param %s should match", k)
				}

				// Send mock response
				w.Header().Set("Content-Type", "application/json")
				w.Write([]byte(`{"code": "Ok", "routes": [], "waypoints": []}`))
			}))
			defer server.Close()

			// Create client
			client := NewClient(server.URL)

			// Send route request
			resp, err := client.Route(context.Background(), tc.req)

			// Validate response
			require.NoError(t, err)
			require.NotNil(t, resp)
		})
	}
}

func TestRouteRequestWithAllOptions(t *testing.T) {
	testCases := []struct {
		name        string
		req         RouteRequest
		expectedURL string
	}{
		{
			name: "Full Options Request",
			req: RouteRequest{
				Coordinates: []Coordinate{
					{Longitude: 101.629174, Latitude: 3.107824},
					{Longitude: 101.616409, Latitude: 3.146852},
				},
				Profile:          ProfileDriving,
				GenerateSteps:    true,
				Annotations:      true,
				Geometries:       GeometryGeoJSON,
				Overview:         OverviewFull,
				ContinueStraight: true,
				Alternatives:     true,
			},
			expectedURL: "/route/v1/driving/101.629174,3.107824;101.616409,3.146852",
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Mock OSRM server
			server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				// Validate request parameters
				assert.Equal(t, tc.expectedURL, r.URL.Path)

				// Check query parameters
				q := r.URL.Query()
				assert.Equal(t, "true", q.Get("steps"))
				assert.Equal(t, "true", q.Get("annotations"))
				assert.Equal(t, string(GeometryGeoJSON), q.Get("geometries"))
				assert.Equal(t, string(OverviewFull), q.Get("overview"))
				assert.Equal(t, "true", q.Get("continue_straight"))
				assert.Equal(t, "true", q.Get("alternatives"))

				// Send mock response
				w.Header().Set("Content-Type", "application/json")
				w.Write([]byte(`{
					"code": "Ok",
					"routes": [{
						"geometry": "mock_geometry",
						"legs": [],
						"weight_name": "routability",
						"weight": 0,
						"duration": 0,
						"distance": 0
					}],
					"waypoints": []
				}`))
			}))
			defer server.Close()

			// Create client
			client := NewClient(server.URL)

			// Send route request
			resp, err := client.Route(context.Background(), tc.req)

			// Validate response
			require.NoError(t, err)
			require.NotNil(t, resp)
		})
	}
}

func TestRouteRequestError(t *testing.T) {
	// Mock OSRM server returning an error
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"code": "InvalidRequest"}`))
	}))
	defer server.Close()

	// Create client
	client := NewClient(server.URL)

	// Prepare route request
	req := RouteRequest{
		Coordinates: []Coordinate{
			{Longitude: 101.629174, Latitude: 3.107824},
			{Longitude: 101.616409, Latitude: 3.146852},
		},
		Profile: ProfileDriving,
	}

	// Send route request
	resp, err := client.Route(context.Background(), req)

	// Validate error
	assert.Error(t, err)
	assert.Nil(t, resp)
	assert.Contains(t, err.Error(), "OSRM returned error: InvalidRequest")
}

func TestRouteRequestWithBearingsAndRadiuses(t *testing.T) {
	testCases := []struct {
		name                string
		bearings            []Bearing
		radiuses            []float64
		expectBearingsQuery string
		expectRadiusesQuery string
	}{
		{
			name: "Two Bearings and Radiuses",
			bearings: []Bearing{
				{Value: 90.0, Range: 45.0},
				{Value: 270.0, Range: 90.0},
			},
			radiuses:            []float64{100.0, 200.0},
			expectBearingsQuery: "90.000000,45.000000;270.000000,90.000000",
			expectRadiusesQuery: "100.000000;200.000000",
		},
		{
			name:                "No Bearings or Radiuses",
			bearings:            nil,
			radiuses:            nil,
			expectBearingsQuery: "",
			expectRadiusesQuery: "",
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Mock OSRM server
			server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				// Validate request parameters
				assert.Equal(t, "/route/v1/driving/101.629174,3.107824;101.616409,3.146852", r.URL.Path)

				// Check query parameters
				q := r.URL.Query()
				if tc.bearings != nil {
					bearingsQuery := q.Get("bearings")
					assert.Equal(t, tc.expectBearingsQuery, bearingsQuery, "Bearings query should match")
				}
				if tc.radiuses != nil {
					radiusesQuery := q.Get("radiuses")
					assert.Equal(t, tc.expectRadiusesQuery, radiusesQuery, "Radiuses query should match")
				}

				// Send mock response
				w.Header().Set("Content-Type", "application/json")
				w.Write([]byte(`{"code": "Ok", "routes": [], "waypoints": []}`))
			}))
			defer server.Close()

			// Create client
			client := NewClient(server.URL)

			// Prepare route request
			req := RouteRequest{
				Coordinates: []Coordinate{
					{Longitude: 101.629174, Latitude: 3.107824},
					{Longitude: 101.616409, Latitude: 3.146852},
				},
				Profile:  ProfileDriving,
				Bearings: tc.bearings,
				Radiuses: tc.radiuses,
			}

			// Send route request
			resp, err := client.Route(context.Background(), req)

			// Validate response
			require.NoError(t, err)
			require.NotNil(t, resp)
		})
	}
}

func TestRouteRequestWithInvalidCoordinates(t *testing.T) {
	testCases := []struct {
		name         string
		coordinates  []Coordinate
		expectError  bool
		mockResponse string
	}{
		{
			name:         "Single Coordinate",
			coordinates:  []Coordinate{{Longitude: 101.629174, Latitude: 3.107824}},
			expectError:  true,
			mockResponse: `{"code": "InvalidRequest", "message": "Not enough coordinates"}`,
		},
		{
			name:         "Empty Coordinates",
			coordinates:  []Coordinate{},
			expectError:  true,
			mockResponse: `{"code": "InvalidRequest", "message": "No coordinates provided"}`,
		},
		{
			name: "Two Valid Coordinates",
			coordinates: []Coordinate{
				{Longitude: 101.629174, Latitude: 3.107824},
				{Longitude: 101.616409, Latitude: 3.146852},
			},
			expectError:  false,
			mockResponse: `{"code": "Ok", "routes": [], "waypoints": []}`,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Create client with a mock server
			server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				w.Header().Set("Content-Type", "application/json")
				w.Write([]byte(tc.mockResponse))
			}))
			defer server.Close()

			// Create client
			client := NewClient(server.URL)

			// Prepare route request
			req := RouteRequest{
				Coordinates: tc.coordinates,
				Profile:     ProfileDriving,
			}

			// Send route request
			resp, err := client.Route(context.Background(), req)

			// Validate response
			if tc.expectError {
				assert.Error(t, err)
				assert.Nil(t, resp)
				if tc.name == "Two Valid Coordinates" {
					assert.Contains(t, err.Error(), "OSRM returned error")
				}
			} else {
				require.NoError(t, err)
				require.NotNil(t, resp)
			}
		})
	}
}

func TestRouteRequestWithDifferentProfiles(t *testing.T) {
	testCases := []struct {
		name         string
		profile      Profile
		coordinates  []Coordinate
		expectedPath string
	}{
		{
			name:    "Driving Profile",
			profile: ProfileDriving,
			coordinates: []Coordinate{
				{Longitude: 101.629174, Latitude: 3.107824},
				{Longitude: 101.616409, Latitude: 3.146852},
			},
			expectedPath: "/route/v1/driving/101.629174,3.107824;101.616409,3.146852",
		},
		{
			name:    "Walking Profile",
			profile: ProfileWalking,
			coordinates: []Coordinate{
				{Longitude: 101.629174, Latitude: 3.107824},
				{Longitude: 101.616409, Latitude: 3.146852},
			},
			expectedPath: "/route/v1/walking/101.629174,3.107824;101.616409,3.146852",
		},
		{
			name:    "Cycling Profile",
			profile: ProfileCycling,
			coordinates: []Coordinate{
				{Longitude: 101.629174, Latitude: 3.107824},
				{Longitude: 101.616409, Latitude: 3.146852},
			},
			expectedPath: "/route/v1/cycling/101.629174,3.107824;101.616409,3.146852",
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Mock OSRM server
			server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				// Validate request parameters
				assert.Equal(t, tc.expectedPath, r.URL.Path)

				// Send mock response
				w.Header().Set("Content-Type", "application/json")
				w.Write([]byte(`{"code": "Ok", "routes": [], "waypoints": []}`))
			}))
			defer server.Close()

			// Create client
			client := NewClient(server.URL)

			// Prepare route request
			req := RouteRequest{
				Coordinates: tc.coordinates,
				Profile:     tc.profile,
			}

			// Send route request
			resp, err := client.Route(context.Background(), req)

			// Validate response
			require.NoError(t, err)
			require.NotNil(t, resp)
		})
	}
}

func TestRouteRequestWithCustomHTTPClient(t *testing.T) {
	// Mock OSRM server
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Send mock response
		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(`{"code": "Ok", "routes": [], "waypoints": []}`))
	}))
	defer server.Close()

	// Create custom HTTP client
	customClient := &http.Client{
		Timeout: 10 * time.Second,
	}

	// Create client with custom HTTP client
	client := NewClient(server.URL, WithHTTPClient(customClient))

	// Prepare route request
	req := RouteRequest{
		Coordinates: []Coordinate{
			{Longitude: 101.629174, Latitude: 3.107824},
			{Longitude: 101.616409, Latitude: 3.146852},
		},
		Profile: ProfileDriving,
	}

	// Send route request
	resp, err := client.Route(context.Background(), req)

	// Validate response
	require.NoError(t, err)
	require.NotNil(t, resp)
}

func TestRouteRequestErrorCases(t *testing.T) {
	testCases := []struct {
		name           string
		responseBody   string
		expectedError  string
		setupMockError bool
	}{
		{
			name:          "Invalid JSON Response",
			responseBody:  `{invalid json}`,
			expectedError: "failed to decode response:",
		},
		{
			name: "Non-OK Response Code",
			responseBody: `{
				"code": "Error",
				"message": "Something went wrong"
			}`,
			expectedError: "OSRM returned error: Error",
		},
		{
			name:           "Network Error",
			setupMockError: true,
			expectedError:  "request failed:",
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Create a mock server
			server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				if tc.setupMockError {
					// Simulate a network error by closing the connection
					hj, ok := w.(http.Hijacker)
					require.True(t, ok, "server must support hijacking")

					conn, _, err := hj.Hijack()
					require.NoError(t, err)
					conn.Close()
					return
				}

				// Set content type and write response body
				w.Header().Set("Content-Type", "application/json")
				w.Write([]byte(tc.responseBody))
			}))
			defer server.Close()

			// Create client
			client := NewClient(server.URL)

			// Prepare route request
			req := RouteRequest{
				Coordinates: []Coordinate{
					{Longitude: 101.629174, Latitude: 3.107824},
					{Longitude: 101.616409, Latitude: 3.146852},
				},
				Profile: ProfileDriving,
			}

			// Send route request
			resp, err := client.Route(context.Background(), req)

			// Validate error
			require.Error(t, err)
			require.Nil(t, resp)

			// Check for specific error message
			assert.Contains(t, err.Error(), tc.expectedError)
		})
	}
}

func TestRouteRequestCreationErrors(t *testing.T) {
	testCases := []struct {
		name          string
		url           string
		expectedError string
	}{
		{
			name:          "Invalid URL Parsing",
			url:           "http://\x00<-invalid",
			expectedError: "failed to create request",
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			// Create client
			client := NewClient(tc.url)

			// Send route request
			resp, err := client.Route(context.Background(), RouteRequest{
				Coordinates: []Coordinate{
					{Longitude: 101.629174, Latitude: 3.107824},
					{Longitude: 101.616409, Latitude: 3.146852},
				},
				Profile: ProfileDriving,
			})

			// Validate error
			require.Error(t, err)
			require.Nil(t, resp)

			// Check for specific error message
			assert.Contains(t, err.Error(), tc.expectedError)
		})
	}
}
