"""Download OpenStreetMap data for OSRM."""
import os
import typer
from scripts.core import console

def download_map(
    region: str = typer.Option("malaysia-singapore-brunei", help="Region to download"),
    data_dir: str = typer.Option("osrm-data", help="Directory to store map data")
):
    """Download OpenStreetMap data for a specified region."""
    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)

    # Construct download URL and local file path
    base_url = "https://download.geofabrik.de/asia"
    file_name = f"{region}-latest.osm.pbf"
    local_path = os.path.join(data_dir, file_name)
    download_url = f"{base_url}/{file_name}"

    with console.status(f"Downloading map data for {region}..."):
        try:
            import urllib.request
            urllib.request.urlretrieve(download_url, local_path)
            console.print(f"[green]✓[/green] Downloaded {file_name} successfully!")
        except Exception as e:
            typer.echo(f"Error downloading map: {e}")
            raise typer.Abort()