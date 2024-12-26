import os
import subprocess
import typer
from scripts.app import osrm
from scripts.core import console
from .download_map import download_map
from scripts.core.console import print_success

def process_map(
    region: str = typer.Option("malaysia-singapore-brunei", help="Region to process"),
    profile: str = typer.Option("car", help="OSRM profile to use"),
    data_dir: str = typer.Option("osrm-data", help="Directory to store map data"),
    force: bool = typer.Option(False, help="Force reprocessing of map")
):
    """Process OpenStreetMap data for routing using OSRM."""
    # Use default data directory if not specified
    data_dir = os.path.abspath(data_dir)
    os.makedirs(data_dir, exist_ok=True)

    # Download map if not exists or force flag is set
    osm_file_name = f"{region}-latest.osm.pbf"
    osm_file_path = os.path.join(data_dir, osm_file_name)
    if not os.path.exists(osm_file_path) or force == True:
        confirm = typer.confirm(f"Download map for {region}? This will overwrite existing map data in {data_dir}.")
        if confirm:
            download_map(region=region, data_dir=data_dir)
        else:
            console.print(f"[yellow]Skipping map download for {region}.[/yellow]")
            typer.Exit(0)

    # Check if processed map already exists and not forcing reprocessing
    osrm_file_name = f"{region}-latest.osrm"
    processed_map = os.path.join(data_dir, osrm_file_name)
    if os.path.exists(processed_map) and force == False:
        console.print(f"[yellow]Processed map {os.path.basename(processed_map)} already exists. Skipping processing.[/yellow]")
        return processed_map

    # Construct profile path
    profile_path = f"/opt/{profile}.lua"

    try:
        # Extract map
        extract_cmd = [
            "docker", "run", "--rm", 
            "-v", f"{data_dir}:/data", 
            "ghcr.io/project-osrm/osrm-backend", 
            "osrm-extract", 
            f"/data/{osm_file_name}", 
            "--profile", 
            profile_path
        ]
        subprocess.run(extract_cmd, check=True)

        # Partition map
        partition_cmd = [
            "docker", "run", "--rm", 
            "-v", f"{data_dir}:/data", 
            "ghcr.io/project-osrm/osrm-backend", 
            "osrm-partition", 
            f"/data/{osrm_file_name}"
        ]
        subprocess.run(partition_cmd, check=True)

        # Customize map
        customize_cmd = [
            "docker", "run", "--rm", 
            "-v", f"{data_dir}:/data", 
            "ghcr.io/project-osrm/osrm-backend", 
            "osrm-customize", 
            f"/data/{osrm_file_name}"
        ]
        subprocess.run(customize_cmd, check=True)

    except subprocess.CalledProcessError as e:
        console.print(f"[red]Error processing map: {e}[/red]")
        try:
            # Clean up potentially corrupted files
            os.remove(processed_map)
        except Exception:
            pass
        raise typer.Abort()

    print_success(f"OSRM map processing for {region} completed!")
    return processed_map

def main():
    typer.run(process_map)

if __name__ == "__main__":
    main()
