"""Process OpenStreetMap data for OSRM routing."""
import os
import subprocess
import typer
from scripts.core import console
from .download_map import download_map

def process_map(
    region: str = typer.Option("malaysia-singapore-brunei", help="Region to process"),
    data_dir: str = typer.Option("osrm-data", help="Directory with map data"),
    profile: str = typer.Option("car", help="Routing profile (car, foot, bike)"),
    cleanup: bool = typer.Option(True, help="Cleanup containers after processing")
):
    """Process OpenStreetMap data for routing using OSRM."""
    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)

    # Construct file paths
    file_name = f"{region}-latest.osm.pbf"
    map_file = os.path.join(data_dir, file_name)

    # Check if map file exists, download if not
    if not os.path.exists(map_file):
        console.print(f"Map file {file_name} not found. Downloading...")
        download_map(region=region, data_dir=data_dir)

    # Docker container names
    extract_container = f"antar-osrm-{region}-extract"
    partition_container = f"antar-osrm-{region}-partition"
    customize_container = f"antar-osrm-{region}-customize"

    # OSRM processing steps
    processing_steps = [
        {
            "name": "extract",
            "container": extract_container,
            "command": [
                "docker", "run", "--rm", "-v", f"{os.path.abspath(data_dir)}:/data",
                "osrm/osrm-backend", "osrm-extract", f"/data/{file_name}", 
                f"--profile", f"/opt/osrm/profiles/{profile}.lua"
            ]
        },
        {
            "name": "partition",
            "container": partition_container,
            "command": [
                "docker", "run", "--rm", "-v", f"{os.path.abspath(data_dir)}:/data",
                "osrm/osrm-backend", "osrm-partition", 
                f"/data/{os.path.splitext(file_name)[0]}.osrm"
            ]
        },
        {
            "name": "customize",
            "container": customize_container,
            "command": [
                "docker", "run", "--rm", "-v", f"{os.path.abspath(data_dir)}:/data",
                "osrm/osrm-backend", "osrm-customize", 
                f"/data/{os.path.splitext(file_name)[0]}.osrm"
            ]
        }
    ]

    # Run processing steps
    for step in processing_steps:
        with console.status(f"Running {step['name']} for {region}..."):
            try:
                subprocess.run(step['command'], check=True)
                print_success(f"{step['name'].capitalize()} completed successfully")
            except subprocess.CalledProcessError as e:
                console.print(f"[red]Error in {step['name']} step: {e}[/red]")
                raise typer.Abort()

    # Optional cleanup
    if cleanup:
        for step in processing_steps:
            try:
                subprocess.run(["docker", "rm", "-f", step['container']], 
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception:
                pass

    print_success(f"OSRM map processing for {region} completed!")