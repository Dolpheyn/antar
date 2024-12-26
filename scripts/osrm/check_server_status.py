#!/usr/bin/env python3
import requests
import typer
from scripts.core import console

def check_server_status(
    region: str = typer.Option("malaysia-singapore-brunei", help="Region to check"),
    port: int = typer.Option(5000, help="Port the OSRM server is running on")
):
    """Check the status of the OSRM routing server."""
    try:
        # Construct the health check URL
        url = f"http://localhost:{port}/route/v1/driving/101.629174,3.107824;101.616409,3.146852"
        
        # Send a test request
        response = requests.get(url, timeout=5)
        
        # Check if response is successful
        if response.status_code == 200:
            console.print(f"[green]OSRM server for {region} is running successfully on port {port}[/green]")
            return True
        else:
            console.print(f"[yellow]OSRM server returned status code {response.status_code}[/yellow]")
            return False
    
    except requests.RequestException as e:
        console.print(f"[red]Error connecting to OSRM server: {e}[/red]")
        return False

def main():
    typer.run(check_server_status)

if __name__ == "__main__":
    main()
