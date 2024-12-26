"""Cleanup OSRM processing containers."""
import subprocess
import typer
from scripts.core import console

def cleanup_containers(
    region: str = typer.Option("malaysia-singapore-brunei", help="Region to cleanup")
):
    """Cleanup OSRM processing containers for a specified region."""
    # Docker container names
    containers = [
        f"antar-osrm-{region}-extract",
        f"antar-osrm-{region}-partition",
        f"antar-osrm-{region}-customize",
        f"antar-osrm-{region}-server"
    ]

    # Cleanup containers
    with console.status(f"Cleaning up OSRM containers for {region}..."):
        removed_containers = []
        failed_containers = []

        for container in containers:
            try:
                # Stop container if running
                subprocess.run(
                    ["docker", "stop", container], 
                    check=False, 
                    stdout=subprocess.DEVNULL, 
                    stderr=subprocess.DEVNULL
                )
                
                # Remove container
                subprocess.run(
                    ["docker", "rm", container], 
                    check=True, 
                    stdout=subprocess.DEVNULL, 
                    stderr=subprocess.DEVNULL
                )
                removed_containers.append(container)
            
            except subprocess.CalledProcessError:
                failed_containers.append(container)

        # Print results
        if removed_containers:
            console.print(f"[green]Removed containers:[/green] {', '.join(removed_containers)}")
        
        if failed_containers:
            console.print(f"[yellow]Could not remove containers:[/yellow] {', '.join(failed_containers)}")
        
        if not removed_containers and not failed_containers:
            console.print(f"[yellow]No OSRM containers found for {region}[/yellow]")
