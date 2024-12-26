"""OSRM management CLI package."""
import typer

from scripts.osrm import (
    check_server_status, 
    cleanup_containers, 
    download_map, 
    full_setup, 
    process_map, 
    render_bulk,
    start_server, 
    stop_server, 
    test_render,
    watch_server_logs
)

# Create a Typer app for OSRM commands
osrm_app = typer.Typer(
    name="osrm",
    help="""
    Open Source Routing Machine (OSRM) management tools.

    - By default, this command will use the Malaysia-Singapore-Brunei map data from
    Geofabrik and store it in a directory named 'osrm-data'.

    - The routing profile will be the default 'car' profile.

    - This script is derived from the official OSRM backend README:
    https://github.com/Project-OSRM/osrm-backend/?tab=readme-ov-file#quick-start
    """,
    no_args_is_help=True,
)

# Add this command to the OSRM Typer app
osrm_app.command()(check_server_status)
osrm_app.command()(cleanup_containers)
osrm_app.command()(download_map)
osrm_app.command()(full_setup)
osrm_app.command()(process_map)
osrm_app.command()(render_bulk)
osrm_app.command()(start_server)
osrm_app.command()(stop_server)
osrm_app.command()(test_render)
osrm_app.command()(watch_server_logs)