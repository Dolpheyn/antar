"""Check the status of the OSRM server."""
import subprocess
import requests
import typer
from scripts.core import console

def check_server_status(
    region: str = typer.Option("malaysia-singapore-brunei", help="Region to check"),
    port: int = typer.Option(5000, help="Port to check")
):
    """Check the status of the OSRM routing server."""
    # Docker container name (matching the naming in start_server.py)
    server_container = f"antar-osrm-{region}-server"

    # Check Docker container status
    try:
        console.print("checking container status...")
        # Inspect container status
        container_status_cmd = [
            "docker", "inspect", 
            "-f", "{{.State.Status}}", 
            server_container
        ]
        console.print(f"[blue]Running command:\n$ {' '.join(container_status_cmd)}[/blue]")
        container_status_result = subprocess.run(
            container_status_cmd, 
            capture_output=True, 
            text=True, 
            check=True
        )
        container_status = container_status_result.stdout.strip()
        if container_status != "running":
            console.print(f"[yellow]Container {server_container} is not running (current status: {container_status})[/yellow]")
            raise typer.Abort()
        console.print(f"[green]Container status: {container_status}[/green]")
    except subprocess.CalledProcessError:
        console.print(f"[red]Unable to find Docker container {server_container}[/red]")
        raise typer.Abort()

    console.print()
    # If container is running, check server health via route request
    server_url = f"http://localhost:{port}/route/v1/driving/101.62917,3.10782;101.61640,3.14685"
    
    try:
        console.print("checking server status...")
        curl_cmd = ["curl", "-s", server_url]
        console.print(f"[blue]Running command:\n$ {' '.join(curl_cmd)}[/blue]")
        curl_result = subprocess.run(curl_cmd, capture_output=True, text=True, check=True)
        import json
        route_data = json.loads(curl_result.stdout)
        if route_data.get('routes'):
            route = route_data['routes'][0]
            console.print(f"[green]Route Distance:[/green] {route['distance']/1000:.2f} km")
            console.print(f"[green]Route Duration:[/green] {route['duration']/60:.2f} minutes")
        else:
            console.print(f"[yellow]Server returned no route data[/yellow]")
            raise typer.Abort()
    
    except requests.ConnectionError:
        console.print(f"[red]Unable to connect to OSRM server on port {port}[/red]")
        raise typer.Abort()
    except requests.Timeout:
        console.print(f"[red]Connection to OSRM server timed out[/red]")
        raise typer.Abort()
    except Exception as e:
        console.print(f"[red]Error checking server status: {e}[/red]")
        raise typer.Abort()
