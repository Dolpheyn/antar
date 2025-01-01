"""Route Optimization Module for Clustering and Route Generation."""

import csv
import math
from typing import List, Dict, Tuple

import numpy as np
import requests
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from .notebooks.osrm import OSRMClient, Coordinate, OSRMOverview, OSRMGeometry

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points on the earth.
    
    Args:
        lat1, lon1: Latitude and longitude of first point
        lat2, lon2: Latitude and longitude of second point
    
    Returns:
        Distance in kilometers
    """
    R = 6371  # Earth's radius in kilometers
    
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = (math.sin(dlat/2)**2 + 
         math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2)
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

def validate_coordinates(points: List[Tuple[float, float]]) -> bool:
    """
    Validate that all coordinates are within acceptable ranges.
    
    Args:
        points: List of (latitude, longitude) tuples
    
    Returns:
        Boolean indicating if all coordinates are valid
    """
    for lat, lon in points:
        if not (-90 <= lat <= 90 and -180 <= lon <= 180):
            return False
    return True

def load_points_from_csv(filepath: str) -> List[Tuple[float, float]]:
    """
    Load latitude and longitude points from a CSV file.
    
    Args:
        filepath: Path to the CSV file
    
    Returns:
        List of (latitude, longitude) tuples
    """
    points = []
    with open(filepath, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Skip header
        lat_col_idx = header.index('latitude')  
        lon_col_idx = header.index('longitude')
        # Validate coordinates
        for n_row, row in enumerate(reader):
            try:
                lat, lon = float(row[lat_col_idx]), float(row[lon_col_idx])
            except ValueError:
                raise ValueError(f"float conversion failed: {n_row}:{row}")
            if not validate_coordinates([(lat, lon)]):
                raise ValueError(f"Invalid coordinates in CSV file {n_row}:{row}")
            points.append((lat, lon))
    
    return points

def cluster_destinations(points: List[Tuple[float, float]], max_cluster_size: int = 5) -> List[List[Tuple[float, float]]]:
    """
    Cluster destinations using a modified K-Means approach.
    
    Args:
        points: List of (latitude, longitude) points
        max_cluster_size: Maximum number of destinations per cluster
    
    Returns:
        List of clusters, where each cluster is a list of (latitude, longitude) points
    """
    # Prepare data for clustering
    X = np.array(points)
    
    # Determine optimal number of clusters
    n_clusters = max(1, math.ceil(len(points) / max_cluster_size))
    
    # Perform clustering
    kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
    kmeans.fit(X)
    
    # Group points by cluster
    clusters = [[] for _ in range(n_clusters)]
    for point, label in zip(points, kmeans.labels_):
        clusters[label].append(point)
    
    return clusters

def optimize_route(points: List[Tuple[float, float]], osrm_url: str = 'http://localhost:5000') -> Dict:
    """
    Optimize route using OSRM service.
    
    Args:
        points: List of (latitude, longitude) points to route
        osrm_url: Base URL for OSRM service
    
    Returns:
        OSRM routing response
    """
    if len(points) < 2:
        raise ValueError("At least two points are required for routing")
    
    # Create OSRM Client
    client = OSRMClient(osrm_url)
    
    # Convert points to Coordinate objects
    coordinates = [Coordinate(lon, lat) for lat, lon in points]
    
    # Request route
    route_response = client.route(
        coordinates, 
        overview=OSRMOverview.FULL, 
        geometry=OSRMGeometry.GEOJSON
    )
    
    return route_response

def process_route_optimization(csv_path: str, max_cluster_size: int = 5) -> List[Dict]:
    """
    Full route optimization pipeline.
    
    Args:
        csv_path: Path to CSV file with points
        max_cluster_size: Maximum destinations per route
    
    Returns:
        List of optimized route responses
    """
    # Load and validate points
    points = load_points_from_csv(csv_path)
    
    # Cluster destinations
    clusters = cluster_destinations(points, max_cluster_size)
    
    # Optimize routes for each cluster
    optimized_routes = []
    for cluster in clusters:
        try:
            route = optimize_route(cluster)
            optimized_routes.append(route)
        except Exception as e:
            print(f"Error optimizing cluster: {e}")
    
    return optimized_routes
