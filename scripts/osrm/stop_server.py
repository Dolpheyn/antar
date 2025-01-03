"""Stop the OSRM routing server."""
import subprocess
import typer
from scripts.core import console
from scripts.core.console import print_success

def stop_server(
    region: str = typer.Option("malaysia-singapore-brunei", help="Region to stop")
):
    """Stop the OSRM routing server for a specified region."""
    # Docker container name
    server_container_name = f"antar-osrm-{region}-server"

    # Stop and remove the container
    with console.status(f"Stopping OSRM server for {region}..."):
        try:
            # Stop the container
            subprocess.run(
                ["docker", "stop", server_container_name], 
                check=True, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            )
            print_success(f"OSRM server for {region} stopped and removed successfully")
        
        except Exception as e:
            console.print(f"[red]Error stopping OSRM server: {e}[/red]")
            raise typer.Abort()
