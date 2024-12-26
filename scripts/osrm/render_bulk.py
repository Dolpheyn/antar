"""Render multiple OSRM routes on a Leaflet map."""
import os
import json
import typer
import webbrowser
from scripts.core.console import print_success

def render_bulk(
    path_json: str = typer.Option(..., help="Path to JSON file with route data"),
    points_csv: str = typer.Option(..., help="Path to JSON file with points data"),
    start_lon: float = typer.Option(101.62917384709634, help="Starting longitude"),
    start_lat: float = typer.Option(3.107824318483157, help="Starting latitude")
):
    """Render multiple routes from a JSON file using OSRM and Leaflet."""
    # Read JSON file
    from polyline import decode
    # Read JSON file
    from polyline import decode

    with open(path_json, 'r') as f:
        routes_data = json.load(f)
        for route_data in routes_data:
            route_data['routes'][0]['geometry'] = [
                [coord[0], coord[1]] for coord in
                decode(route_data['routes'][0]['geometry'])
            ]
    with open(points_csv, 'r') as f:
        points_data = [line.strip().split(',') for line in f]
        points = [[float(point[1]), float(point[0])] for point in points_data]

    # Prepare HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>OSRM Multiple Routes Visualization</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
        <style>
            body, html {{ height: 100%; margin: 0px; }}
            #map {{ height: 100%; }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <script>
            var map = L.map('map').setView([{start_lat}, {start_lon}], 13);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: 'OpenStreetMap contributors'
            }}).addTo(map);

            // Start marker
            L.marker([{start_lat}, {start_lon}]).addTo(map)
                .bindPopup('Bloomthis Warehouse').openPopup();

            var points = {points};
            points.forEach(point => {{
                L.marker([point[0], point[1]]).addTo(map);
            }});

            var routes = {routes_data};
            routes.forEach((route, index) => {{
                if (route && route.routes && route.routes.length > 0) {{
                    var routeInfo = route.routes[0];
                    var coordinates = routeInfo.geometry;
                    var distance = (routeInfo.distance / 1000).toFixed(2);
                    var duration = (routeInfo.duration / 60).toFixed(2);

                    // Create a polyline for the route
                    var routeLine = L.polyline(
                        coordinates.map(coord => [coord[0], coord[1]]),
                        {{
                            color: ['blue', 'red', 'green', 'purple', 'orange'][index % 5],
                            weight: 5,
                            opacity: 0.7,
                            interactive: true,
                        }}
                    ).addTo(map);
                }}
            }});

            // Fit map to all routes
            var routeLines = map.eachLayer(function(layer) {{
                if (layer instanceof L.Polyline) {{
                    map.fitBounds(layer.getBounds(), {{ padding: [50, 50] }});
                }}
            }});
        </script>
    </body>
    </html>
    """

    # Write HTML to a temporary file
    temp_html = os.path.join(os.path.expanduser('~'), 'osrm_multiple_routes_render.html')
    with open(temp_html, 'w') as f:
        f.write(html_content)

    # Open the HTML file in the default web browser
    webbrowser.open(f'file://{temp_html}')
    print_success(f"Multiple routes rendered from {path_json}")
