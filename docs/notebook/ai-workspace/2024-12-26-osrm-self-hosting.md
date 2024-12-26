# Self-Hosting Open Source Routing Machine (OSRM)

## Overview
This document outlines the process of self-hosting OSRM (Open Source Routing Machine) for our routing optimization project, using Malaysia-Singapore-Brunei OpenStreetMap data.

## Prerequisites
- Docker
- Sufficient disk space (at least 10GB recommended)
- curl or wget
- Basic understanding of command-line interfaces

## Step 1: Download OpenStreetMap Data
We'll download the Malaysia-Singapore-Brunei region OSM data:

```bash
# Create a directory for OSM data
mkdir -p osrm-data

# Download the latest OSM data for Malaysia, Singapore, and Brunei
wget https://download.geofabrik.de/asia/malaysia-singapore-brunei-latest.osm.pbf -O osrm-data/malaysia-singapore-brunei.osm.pbf
```

## Step 2: Install OSRM
We'll use Docker to simplify the installation and setup process:

```bash
# Pull the latest OSRM backend image
docker pull ghcr.io/project-osrm/osrm-backend

# Extract the map data (using car profile)
docker run -t -v "${PWD}/osrm-data:/data" ghcr.io/project-osrm/osrm-backend osrm-extract -p /opt/car.lua /data/malaysia-singapore-brunei.osm.pbf || echo "osrm-extract failed"

# Partition the data
docker run -t -v "${PWD}/osrm-data:/data" ghcr.io/project-osrm/osrm-backend osrm-partition /data/malaysia-singapore-brunei.osrm || echo "osrm-partition failed"

# Customize the data
docker run -t -v "${PWD}/osrm-data:/data" ghcr.io/project-osrm/osrm-backend osrm-customize /data/malaysia-singapore-brunei.osrm || echo "osrm-customize failed"
```

### Notes on the Commands
- `-t`: Allocate a pseudo-TTY
- `-v "${PWD}/osrm-data:/data"`: Mount the local `osrm-data` directory to `/data` in the container
- `osrm-extract -p /opt/car.lua`: Use the car routing profile
- `|| echo "command-name failed"`: Provide error handling for each step

## Step 3: Start OSRM Server
```bash
# Start OSRM routing service with Multi-Level Dijkstra (MLD) algorithm
docker run -t -i -p 5000:5000 -v "${PWD}/osrm-data:/data" ghcr.io/project-osrm/osrm-backend osrm-routed --algorithm mld /data/malaysia-singapore-brunei.osrm
```

### Command Breakdown
- `-t -i`: Allocate a pseudo-TTY and keep STDIN open (interactive mode)
- `-p 5000:5000`: Map container port 5000 to host port 5000
- `-v "${PWD}/osrm-data:/data"`: Mount the local `osrm-data` directory to `/data` in the container
- `--algorithm mld`: Use Multi-Level Dijkstra algorithm for routing
- `/data/malaysia-singapore-brunei.osrm`: Specify the preprocessed map file

## Testing the Service
You can now test the OSRM routing service:

```bash
# Example routing request (replace with actual coordinates)
curl "http://localhost:5000/route/v1/driving/103.8198,1.3521;103.9915,1.3644?overview=full"
```

## Next Steps
- Integrate with our route optimization algorithm
- Implement caching mechanisms
- Set up monitoring and logging

## Potential Challenges
- Large dataset processing time
- Memory and CPU requirements
- Keeping map data up to date

## Future Improvements
- Implement automatic data update scripts
- Create a custom Docker compose setup
- Add more routing profiles (walking, cycling)

## References
- [OSRM Documentation](https://project-osrm.org/)
- [OpenStreetMap Data Downloads](https://download.geofabrik.de/)
