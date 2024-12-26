"""Complete OSRM setup: download, process, and start server."""
import typer
from scripts.core import console
from .download_map import download_map
from .process_map import process_map
from .start_server import start_server

def full_setup(
    region: str = typer.Option("malaysia-singapore-brunei", help="Region to set up"),
    data_dir: str = typer.Option("osrm-data", help="Directory to store map data"),
    port: int = typer.Option(5000, help="Port to expose OSRM server"),
    profile: str = typer.Option("car", help="Routing profile"),
    algorithm: str = typer.Option("mld", help="Routing algorithm")
):
    """Complete OSRM setup: download map, process data, and start server."""
    with console.status(f"Performing full OSRM setup for {region}..."):
        try:
            # Step 1: Download map
            download_map(region=region, data_dir=data_dir)
            print_success("Map download completed")

            # Step 2: Process map
            process_map(region=region, data_dir=data_dir, profile=profile)
            print_success("Map processing completed")

            # Step 3: Start server
            start_server(region=region, data_dir=data_dir, port=port, algorithm=algorithm)
            print_success("OSRM server started successfully")

            console.print(f"[green]Full OSRM setup for {region} completed![/green]")
        
        except Exception as e:
            console.print(f"[red]Error during full setup: {e}[/red]")
            raise typer.Abort()