"""Download OpenStreetMap data for OSRM."""
import os
import subprocess
import typer
from scripts.core import console

def download_map(
    region: str = typer.Option("malaysia-singapore-brunei", help="Region to download"),
    data_dir: str = typer.Option(None, help="Directory to store map data")
):
    """Download OpenStreetMap data for a specified region."""
    # Use default data directory if not specified
    if data_dir is None:
        data_dir = os.path.join(os.path.dirname(__file__), "..", "..", "osrm-data")

    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)

    # Construct download URL and local file path
    base_url = "https://download.geofabrik.de/asia"
    file_name = f"{region}-latest.osm.pbf"
    local_path = os.path.join(data_dir, file_name)
    download_url = f"{base_url}/{file_name}"

    with console.status(f"Downloading map data for {region}..."):
        try:
            # Use wget to download
            wget_cmd = [
                "wget", 
                "-O", local_path,  # Output to local file
                "--no-check-certificate",  # Bypass SSL verification
                download_url
            ]
            subprocess.run(wget_cmd, check=True)
            console.print(f"[green]✓[/green] Downloaded {file_name} successfully!")
        except subprocess.CalledProcessError as e:
            console.print(f"[red]Error downloading map: {e}[/red]")
            raise typer.Abort()

def main():
    typer.run(download_map)

if __name__ == "__main__":
    main()
