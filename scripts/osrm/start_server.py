"""Start OSRM routing server."""
import os
import subprocess
import typer
from scripts.core import console
from .process_map import process_map

def start_server(
    region: str = typer.Option("malaysia-singapore-brunei", help="Region to serve"),
    data_dir: str = typer.Option("osrm-data", help="Directory with processed map data"),
    port: int = typer.Option(5000, help="Port to expose OSRM server"),
    algorithm: str = typer.Option("mld", help="Routing algorithm")
):
    """Start OSRM routing server for a specified region."""
    # Construct file paths
    file_name = f"{region}-latest.osm.pbf"
    processed_map = os.path.join(data_dir, f"{os.path.splitext(file_name)[0]}.osrm")

    # Check if processed map exists, process if not
    if not os.path.exists(processed_map):
        console.print(f"Processed map not found. Processing map first...")
        process_map(region=region, data_dir=data_dir)

    # Docker container name
    server_container = f"antar-osrm-{region}-server"

    # Prepare Docker command
    docker_command = [
        "docker", "run", "-d", 
        "--name", server_container,
        "-p", f"{port}:5000",
        "-v", f"{os.path.abspath(data_dir)}:/data",
        "osrm/osrm-backend", 
        "osrm-routed", 
        f"/data/{os.path.splitext(file_name)[0]}.osrm",
        f"--algorithm={algorithm}"
    ]

    # Start OSRM server
    with console.status(f"Starting OSRM server for {region} on port {port}..."):
        try:
            subprocess.run(docker_command, check=True)
            print_success(f"OSRM server started successfully on port {port}")
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error starting OSRM server: {e}[/red]")
            raise typer.Abort()