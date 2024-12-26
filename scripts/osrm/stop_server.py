"""Stop the OSRM routing server."""
import subprocess
import typer
from scripts.core import console

def stop_server(
    region: str = typer.Option("malaysia-singapore-brunei", help="Region to stop")
):
    """Stop the OSRM routing server for a specified region."""
    # Docker container name
    server_container = f"antar-osrm-{region}-server"

    # Stop and remove the container
    with console.status(f"Stopping OSRM server for {region}..."):
        try:
            # Stop the container
            subprocess.run(
                ["docker", "stop", server_container], 
                check=True, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            )
            
            # Remove the container
            subprocess.run(
                ["docker", "rm", server_container], 
                check=True, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.DEVNULL
            )
            
            print_success(f"OSRM server for {region} stopped and removed successfully")
        
        except subprocess.CalledProcessError:
            console.print(f"[yellow]No running OSRM server found for {region}[/yellow]")
        except Exception as e:
            console.print(f"[red]Error stopping OSRM server: {e}[/red]")
            raise typer.Abort()