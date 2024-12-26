import os
import subprocess
import typer
import glob
from scripts.core import console
from .process_map import process_map
from scripts.core.console import print_success

def start_server(
    region: str = typer.Option("malaysia-singapore-brunei", help="Region to serve"),
    port: int = typer.Option(5000, help="Port to run OSRM server"),
    data_dir: str = typer.Option("osrm-data", help="Directory with map data"),
    profile: str = typer.Option("car", help="Routing profile to use"),
    algorithm: str = typer.Option("mld", help=""),
):
    """Start OSRM routing server for a specified region."""
    # Use default data directory if not specified
    data_dir = os.path.abspath(data_dir)

    # Construct file paths
    osrm_file_name = f"{region}-latest.osrm"
    processed_map_glob = os.path.join(data_dir, f"{region}-latest.osrm.*")
    processed_map_files = glob.glob(processed_map_glob)

    # Check if processed map exists, process if not
    if not processed_map_files:
        if typer.confirm(f"Processed map not found. Process map for {region}?"):
            process_map(region=region, data_dir=data_dir, profile=profile)
        else:
            console.print(f"[yellow]Skipping map processing for {region}.[/yellow]")
            raise typer.Abort()

    # Check if server is already running
    server_container_name = f"antar-osrm-{region}-server"
    container_state_cmd = ["docker", "inspect", "--format", "{{.State.Running}}", server_container_name]
    try:
        output = subprocess.check_output(container_state_cmd, stderr=subprocess.DEVNULL).decode().strip()
        if output == "true":
            console.print(f"[yellow]OSRM server for {region} is already running.[/yellow]")
            raise typer.Abort()
    except subprocess.CalledProcessError:
        pass

    try:
        # Start OSRM server
        server_container_name = f"antar-osrm-{region}-server"
        server_cmd = [
            "docker", "run", "--rm", "-d", 
            "--name", server_container_name,
            "-p", f"{port}:5000", 
            "-v", f"{data_dir}:/data", 
            "ghcr.io/project-osrm/osrm-backend", 
            "osrm-routed", 
            f"/data/{osrm_file_name}", 
            "--algorithm", algorithm,
        ]

        subprocess.run(server_cmd, check=True)
        print_success(f"OSRM server started successfully on port {port}")

    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error starting OSRM server: {e}[/red]")
        raise typer.Abort()

def main():
    typer.run(start_server)

if __name__ == "__main__":
    main()
