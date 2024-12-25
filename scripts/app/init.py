"""Module for initializing project dependencies."""

from enum import Enum
import subprocess
import shutil
import typer
from typing import List, Optional, Tuple

from dataclasses import dataclass

class DependencyGroup(Enum):
    techops = "techops"
    docs = "docs"
    frontend = "frontend"
    backend = "backend"

@dataclass
class Dependency:
    """A dependency with its installer, version checker, and post-install commands."""
    name: str
    group: Tuple[DependencyGroup, ...]
    description: str
    installer: List[str]
    version: List[str]
    post_install: Optional[List[List[str]]] = None

DEPENDENCIES: List[Dependency] = [
    Dependency(
        name="pip",
        group=(DependencyGroup.techops, DependencyGroup.docs),
        description="Python package installer",
        installer=["python3", "-m", "ensurepip", "--upgrade"],
        version=["pip", "--version"],
    ),
    Dependency(
        name="poetry",
        group=(DependencyGroup.techops, DependencyGroup.docs),
        description="A package manager for Python",
        installer=["pipx", "install", "poetry"],
        version=["poetry", "--version"],
    ),
    Dependency(
        name="npm",
        group=(DependencyGroup.frontend),
        description="Node.js package manager",
        installer=["curl", "-fsSL", "https://raw.githubusercontent.com/tj/n/master/bin/n | bash -s", "lts"],
        version=["npm", "--version"],
    ),
    Dependency(
        name="next",
        group=(DependencyGroup.frontend),
        description="A React framework for production",
        installer=["npm", "install", "-g", "next"],
        version=["next", "--version"],
    ),
    Dependency(
        name="go",
        group=(DependencyGroup.backend),
        description="A statically typed, compiled, and garbage-collected language",
        installer=[
            "wget",
            "-O",
            "/tmp/go.tar.gz",
            "https://go.dev/dl/go1.20.2.linux-amd64.tar.gz",
        ],
        post_install=[
            ["tar", "-xf", "/tmp/go.tar.gz", "-C", "/usr/local"],
            ["rm", "-rf", "/usr/local/go/bin"],
        ],
        version=["go", "version"],
    ),
    Dependency(
        name="bun",
        group=(DependencyGroup.frontend),
        description="A fast JavaScript runtime and package manager",
        installer=["npm", "install", "-g", "bun"],
        version=["bun", "--version"],
    ),
]


init_app = typer.Typer(
    name="init",
    help="Initialize project dependencies",
    no_args_is_help=True,
)

def is_installed(pkg: Dependency) -> bool:
    """Check if a package is installed."""
    return shutil.which(pkg.name) is not None

@init_app.command(name="all")
def init_cli(
    ci: bool = typer.Option(
        False, "--ci", help="Skip interactive confirmation, useful for CI/CD"
    ),
):
    """Initialize all project dependencies."""
    print("You are about to initialize the project dependencies.")
    print("But first, let's see which ones are already installed.")
    already_installed = [pkg for pkg in DEPENDENCIES if is_installed(pkg)]
    if len(already_installed) == len(DEPENDENCIES):
        print("\nAlready installed:")
        print_dependencies_with_version(already_installed)
        print("\nAll dependencies are already installed. You are good to go!")
        print("Happy building!")
        raise typer.Exit(0)

    print("\nThe following dependencies are already installed:")
    print_dependencies_with_version(already_installed)
    packages_to_install = [pkg for pkg in DEPENDENCIES if not is_installed(pkg)]
    print("\nThe following dependencies need to be installed:")
    print(
        "\n".join(
            [
                f"- {pkg.name}: {pkg.description}"
                for pkg in packages_to_install
            ]
        )
    )
    if not ci:
        confirm = input("\nAre you sure you want to continue? (Y/n) ")
        if confirm.lower() == "n" or confirm.lower() == "no":
            print("Installation cancelled.")
            print("No changes were made.")
            print("\nHave a nice day!")
            raise typer.Exit(0)

    # install packages
    successful_pkgs, failed_pkgs = install_packages(packages_to_install)
    print("\n"+ "Summary".center(50, "="))
    print("Already installed:")
    print_dependencies_with_version(already_installed)
    print("Installed in this execution:")
    print_dependencies_with_version([pkg for pkg in DEPENDENCIES if pkg.name in successful_pkgs])
    if len(failed_pkgs) > 0:
        print(f"Failed to install {', '.join(failed_pkgs)}")
        print("Please check the output above to see the errors.")
        print("No changes were made.")
        print("\nIf you need help, please create an issue at https://github.com/dolpheyn/antar/issues")
        print("Have a nice day!")
        raise typer.Exit(1)

    print("\nAll dependencies have been installed!")
    print("Happy building!")


def print_dependencies_with_version(dependencies: List[Dependency]):
    """Print installed versions of all dependencies."""
    for pkg in dependencies:
        version = subprocess.check_output(pkg.version).decode().strip()
        print(f"- {pkg.name}: {version} ")


def install_packages(packages_to_install: List[Dependency]) -> Tuple[List[str], List[str]]:
    """Install a list of packages and their post-install commands."""
    successful_pkgs = []
    failed_pkgs = []
    for pkg in packages_to_install:
        print("\nInstalling:")
        print(f"- {pkg.name} ({pkg.description})")
        try:
            print(f"\033[92m  $ {' '.join(pkg.installer)}\033[0m")
            subprocess.run(pkg.installer, check=True)
            for post_install_cmd in pkg.post_install or []:
                subprocess.run(post_install_cmd, check=True)
            successful_pkgs.append(pkg.name)
        except subprocess.CalledProcessError as e:
            failed_pkgs.append(pkg.name)
            print(f"Failed to install {pkg.name}:")
            print(e)

    return successful_pkgs, failed_pkgs
