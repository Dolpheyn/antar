"""Watch logs for the OSRM server Docker container."""
import subprocess
import typer
from scripts.core import console

def watch_server_logs(
    region: str = typer.Option("malaysia-singapore-brunei", help="Region to check"),
    follow: bool = typer.Option(True, "--follow", "-f", help="Follow log output"),
    tail: int = typer.Option(100, "--tail", "-n", help="Number of log lines to show")
):
    """Watch or retrieve logs for the OSRM routing server container."""
    # Docker container name (matching the naming in start_server.py)
    server_container = f"antar-osrm-{region}-server"

    # Prepare docker logs command
    log_cmd = ["docker", "logs"]
    
    # Add follow flag if specified
    if follow:
        log_cmd.append("-f")
    
    # Add tail lines option
    log_cmd.extend(["-n", str(tail)])
    
    # Add container name
    log_cmd.append(server_container)

    try:
        console.print(f"[blue]Running command:\n$ {' '.join(log_cmd)}[/blue]")
        
        # Run the docker logs command
        subprocess.run(log_cmd, check=True)
    
    except subprocess.CalledProcessError:
        console.print(f"[red]Unable to retrieve logs for container {server_container}[/red]")
        raise typer.Abort()

if __name__ == "__main__":
    typer.run(watch_server_logs)
