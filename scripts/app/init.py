"""Module for initializing project dependencies."""
import typer
import subprocess
import shutil
from typing import List, Dict, Any

DEPENDENCIES = [
    {
        "name": "poetry",
        "description": "A package manager for Python",
        "installer": ["pip", "install", "poetry"],
        "version": ["poetry", "--version"],
    },
    {
        "name": "next",
        "description": "A React framework for production",
        "installer": ["npm", "install", "-g", "next"],
        "version": ["next", "--version"],
    },
    {
        "name": "go",
        "description": "A statically typed, compiled, and garbage-collected language",
        "installer": [
            "wget",
            "-O",
            "/tmp/go.tar.gz",
            "https://go.dev/dl/go1.20.2.linux-amd64.tar.gz",
        ],
        "post_install": [
            ["tar", "-xf", "/tmp/go.tar.gz", "-C", "/usr/local"],
            ["rm", "-rf", "/usr/local/go/bin"],
        ],
        "version": ["go", "version"],
    },
]

init_app = typer.Typer(
    name="init",
    help="Initialize project dependencies",
    no_args_is_help=True,
)

@init_app.command(name="all")
def init_cli():
    """Initialize all project dependencies."""
    packages_to_install = [pkg for pkg in DEPENDENCIES if shutil.which(pkg["name"]) is None]
    if len(packages_to_install) == 0:
        print("All dependencies are already installed.")
        print("Installed versions:")
        for pkg in DEPENDENCIES:
            version = subprocess.check_output(pkg["version"]).decode().strip()
            print(f"- {pkg['name']}: {version} ✅")
        return

    # ask user for confirmation
    print("The following packages will be installed:")
    print("\n".join([f"- {pkg['name']} ({pkg['description']})" for pkg in packages_to_install]))

    confirm = input("Are you sure you want to continue? (y/n) ")
    if confirm.lower() != "y":
        print("Installation cancelled.")
        raise typer.Exit(1)

    # install packages
    failed_pkgs = install_packages(packages_to_install)
    if len(failed_pkgs) > 0:
        print(f"Failed to install {', '.join(failed_pkgs)}")
        raise typer.Exit(1)

def install_packages(packages_to_install: List[Dict[str, Any]]) -> List[str]:
    """Install a list of packages and their post-install commands."""
    failed_pkgs = []
    print("Installing:")
    for pkg in packages_to_install:
        print(f"- {pkg['name']} ({pkg['description']})")
        try:
            subprocess.run(pkg["installer"], check=True)
            for post_install_cmd in pkg.get("post_install", []):
                subprocess.run(post_install_cmd, check=True)
        except subprocess.CalledProcessError as e:
            failed_pkgs.append(pkg["name"])
            print(f"Failed to install {pkg['name']}:")
            print(e)

    return failed_pkgs
