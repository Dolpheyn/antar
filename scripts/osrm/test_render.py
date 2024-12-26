"""Render OSRM route on a Leaflet map."""
import os
import typer
import requests
import webbrowser
from scripts.core import console
from scripts.core.console import print_success

def test_render(
    port: int = typer.Option(5000, help="OSRM server port"),
    start_lon: float = typer.Option(101.62917384709634, help="Starting longitude"),
    start_lat: float = typer.Option(3.107824318483157, help="Starting latitude"),
    end_lon: float = typer.Option(101.61640928213977, help="Ending longitude"),
    end_lat: float = typer.Option(3.1468522006525212, help="Ending latitude")
):
    """Render a route between two points using OSRM and Leaflet."""
    # Construct OSRM route request URL
    route_url = (
        f"http://localhost:{port}/route/v1/driving/"
        f"{start_lon},{start_lat};{end_lon},{end_lat}"
        "?overview=full&geometries=geojson"
    )

    with console.status("Fetching route from OSRM server..."):
        try:
            response = requests.get(route_url, timeout=10)
            route_data = response.json()

            if route_data.get('routes'):
                route = route_data['routes'][0]
                coordinates = route['geometry']['coordinates']
                distance = route['distance'] / 1000  # Convert to km
                duration = route['duration'] / 60  # Convert to minutes

                # Create a temporary HTML file for rendering
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <title>OSRM Route Visualization</title>
                    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
                    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
                    <style>
                        #map {{ height: 600px; }}
                    </style>
                </head>
                <body>
                    <div id="map"></div>
                    <div>
                        <p>Distance: {distance:.2f} km</p>
                        <p>Duration: {duration:.2f} minutes</p>
                    </div>
                    <script>
                        var map = L.map('map').setView([{start_lat}, {start_lon}], 13);
                        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                            attribution: '© OpenStreetMap contributors'
                        }}).addTo(map);

                        var routeCoords = {coordinates};
                        var routeLine = L.polyline(routeCoords.map(coord => [coord[1], coord[0]]), {{
                            color: 'blue',
                            weight: 5,
                            opacity: 0.7
                        }}).addTo(map);

                        L.marker([{start_lat}, {start_lon}]).addTo(map)
                            .bindPopup('Start Point').openPopup();
                        L.marker([{end_lat}, {end_lon}]).addTo(map)
                            .bindPopup('End Point').openPopup();

                        map.fitBounds(routeLine.getBounds());
                    </script>
                </body>
                </html>
                """

                # Write HTML to a temporary file
                temp_html = os.path.join(os.path.expanduser('~'), 'osrm_route_render.html')
                with open(temp_html, 'w') as f:
                    f.write(html_content)

                # Open the HTML file in the default web browser
                webbrowser.open(f'file://{temp_html}')
                print_success(f"Route rendered! Distance: {distance:.2f} km, Duration: {duration:.2f} minutes")
            else:
                console.print("[red]No route found between the specified points.[/red]")
        
        except requests.RequestException as e:
            console.print(f"[red]Error fetching route: {e}[/red]")
            raise typer.Abort()
