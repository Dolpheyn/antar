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

func TestNewClient(t *testing.T) {
	baseURL := "http://example.com"
	
	// Test default client creation
	client := NewClient(baseURL)
	require.NotNil(t, client)
	assert.Equal(t, baseURL, client.baseURL)
	assert.NotNil(t, client.httpClient)
	assert.Equal(t, 30*time.Second, client.httpClient.Timeout)

	// Test client creation with custom HTTP client
	customHTTPClient := &http.Client{
		Timeout: 10 * time.Second,
	}
	customClient := NewClient(baseURL, WithHTTPClient(customHTTPClient))
	require.NotNil(t, customClient)
	assert.Equal(t, baseURL, customClient.baseURL)
	assert.Equal(t, customHTTPClient, customClient.httpClient)
}

func TestBuildURL(t *testing.T) {
	testCases := []struct {
		name        string
		baseURL     string
		service     string
		profile     Profile
		expectedURL string
	}{
		{
			name:        "Driving Profile",
			baseURL:     "http://example.com",
			service:     "route",
			profile:     ProfileDriving,
			expectedURL: "http://example.com/route/v1/driving",
		},
		{
			name:        "Walking Profile",
			baseURL:     "https://osrm.example.org",
			service:     "route",
			profile:     ProfileWalking,
			expectedURL: "https://osrm.example.org/route/v1/walking",
		},
		{
			name:        "Cycling Profile",
			baseURL:     "http://localhost:5000",
			service:     "route",
			profile:     ProfileCycling,
			expectedURL: "http://localhost:5000/route/v1/cycling",
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			client := NewClient(tc.baseURL)
			actualURL := client.buildURL(tc.service, tc.profile)
			assert.Equal(t, tc.expectedURL, actualURL)
		})
	}
}

func TestClientDo(t *testing.T) {
	testCases := []struct {
		name           string
		serverResponse string
		serverStatus   int
		setupMockError bool
	}{
		{
			name:           "Successful Request",
			serverResponse: "OK",
			serverStatus:   http.StatusOK,
		},
		{
			name:           "Network Error",
			setupMockError: true,
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

				w.WriteHeader(tc.serverStatus)
				w.Write([]byte(tc.serverResponse))
			}))
			defer server.Close()

			// Create client
			client := NewClient(server.URL)

			// Create request
			req, err := http.NewRequest("GET", server.URL, nil)
			require.NoError(t, err)

			// Perform request
			resp, err := client.do(context.Background(), req)

			if tc.setupMockError {
				// Expect an error for network failure
				require.Error(t, err)
				require.Nil(t, resp)
			} else {
				// Validate successful request
				require.NoError(t, err)
				require.NotNil(t, resp)
				assert.Equal(t, tc.serverStatus, resp.StatusCode)
			}
		})
	}
}
