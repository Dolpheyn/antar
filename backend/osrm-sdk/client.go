package osrm

import (
	"context"
	"fmt"
	"net/http"
	"time"
)

// Profile represents the routing profile
type Profile string

const (
	ProfileDriving Profile = "driving"
	ProfileWalking Profile = "walking"
	ProfileCycling Profile = "cycling"
)

// Client is the main OSRM client
type Client struct {
	baseURL    string
	httpClient *http.Client
}

// ClientOption allows configuring the OSRM client
type ClientOption func(*Client)

// WithHTTPClient sets a custom HTTP client
func WithHTTPClient(client *http.Client) ClientOption {
	return func(c *Client) {
		c.httpClient = client
	}
}

// NewClient creates a new OSRM client
func NewClient(baseURL string, opts ...ClientOption) *Client {
	client := &Client{
		baseURL: baseURL,
		httpClient: &http.Client{
			Timeout: 30 * time.Second,
		},
	}

	// Apply options
	for _, opt := range opts {
		opt(client)
	}

	return client
}

// buildURL constructs the full URL for a given service and profile
func (c *Client) buildURL(service string, profile Profile) string {
	return fmt.Sprintf("%s/%s/v1/%s", c.baseURL, service, profile)
}

// do performs the HTTP request
func (c *Client) do(ctx context.Context, req *http.Request) (*http.Response, error) {
	req = req.WithContext(ctx)
	return c.httpClient.Do(req)
}
