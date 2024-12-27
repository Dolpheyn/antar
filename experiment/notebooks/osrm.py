"""
OSRM (Open Source Routing Machine) Client for v5.24.0

This module provides a comprehensive client for interacting with OSRM services.
Supports route, nearest, table, match, trip, and tile services.

References:
- OSRM API Documentation: https://project-osrm.org/docs/v5.24.0/api/
"""

import enum
import typing
import requests
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Union, Tuple


class OSRMProfile(str, enum.Enum):
    """Predefined routing profiles supported by OSRM."""
    DRIVING = "driving"
    WALKING = "walking"
    CYCLING = "cycling"
    WHEELCHAIR = "wheelchair"


class OSRMGeometry(str, enum.Enum):
    """Geometry encoding formats for route responses."""
    POLYLINE = "polyline"
    POLYLINE6 = "polyline6"
    GEOJSON = "geojson"


class OSRMOverview(str, enum.Enum):
    """Level of detail for route geometry overview."""
    SIMPLIFIED = "simplified"
    FULL = "full"
    FALSE = "false"


@dataclass
class Coordinate:
    """
    Represents a geographical coordinate.
    
    Attributes:
        longitude (float): Longitude in decimal degrees
        latitude (float): Latitude in decimal degrees
    """
    longitude: float
    latitude: float

    def __iter__(self):
        """Allow unpacking into [lon, lat] for OSRM API."""
        yield self.longitude
        yield self.latitude


@dataclass
class OSRMClient:
    """
    OSRM Client for making routing service requests.
    
    Attributes:
        base_url (str): Base URL of the OSRM service
        timeout (int, optional): Request timeout in seconds
    """
    base_url: str
    timeout: int = 30

    def _request(
        self, 
        service: str, 
        profile: OSRMProfile, 
        coordinates: List[Coordinate], 
        params: Optional[Dict] = None
    ) -> Dict:
        """
        Make a generic request to OSRM service.
        
        Args:
            service (str): OSRM service endpoint
            profile (OSRMProfile): Routing profile
            coordinates (List[Coordinate]): Coordinates for the request
            params (Dict, optional): Additional query parameters
        
        Returns:
            Dict: JSON response from OSRM
        
        Raises:
            requests.RequestException: For network or API errors
        """
        # Validate coordinates
        validate_coordinates(coordinates)
        
        # Convert coordinates to semicolon-separated string of lon,lat
        coords_str = ";".join(f"{coord.longitude},{coord.latitude}" for coord in coordinates)
        
        # Construct URL with path parameters
        url = f"{self.base_url}/{service}/v1/{profile.value}/{coords_str}"
        
        try:
            # Merge default and additional parameters
            request_params = params or {}
            response = requests.get(url, params=request_params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"OSRM API request failed: {e}") from e

    def route(
        self, 
        coordinates: List[Coordinate],
        *,
        profile: OSRMProfile = OSRMProfile.DRIVING,
        alternatives: bool = False,
        steps: bool = False,
        annotations: bool = False,
        overview: OSRMOverview = OSRMOverview.SIMPLIFIED,
        geometry: OSRMGeometry = OSRMGeometry.POLYLINE
    ) -> Dict:
        """
        Request route between multiple coordinates.
        
        Args:
            coordinates (List[Coordinate]): Sequence of coordinates to route through
            profile (OSRMProfile, optional): Routing profile
            alternatives (bool, optional): Request alternative routes
            steps (bool, optional): Include step information
            annotations (bool, optional): Include detailed annotations
            overview (OSRMOverview, optional): Geometry overview detail
            geometry (OSRMGeometry, optional): Geometry encoding format
        
        Returns:
            Dict: Route response from OSRM
        """
        params = {
            "alternatives": str(alternatives).lower(),
            "steps": str(steps).lower(),
            "annotations": str(annotations).lower(),
            "overview": overview.value,
            "geometries": geometry.value
        }
        return self._request("route", profile, coordinates, params)

    def nearest(
        self, 
        coordinate: Coordinate, 
        *, 
        profile: OSRMProfile = OSRMProfile.DRIVING,
        number: int = 1
    ) -> Dict:
        """
        Find nearest road or path to a given coordinate.
        
        Args:
            coordinate (Coordinate): Target coordinate
            profile (OSRMProfile, optional): Routing profile
            number (int, optional): Number of nearest points to return
        
        Returns:
            Dict: Nearest points response
        """
        params = {"number": number}
        return self._request("nearest", profile, [coordinate], params)

    def table(
        self, 
        coordinates: List[Coordinate], 
        *, 
        profile: OSRMProfile = OSRMProfile.DRIVING,
        sources: Optional[List[int]] = None,
        destinations: Optional[List[int]] = None
    ) -> Dict:
        """
        Compute distance/duration table between coordinates.
        
        Args:
            coordinates (List[Coordinate]): Coordinates to compute table for
            profile (OSRMProfile, optional): Routing profile
            sources (List[int], optional): Indices of source coordinates
            destinations (List[int], optional): Indices of destination coordinates
        
        Returns:
            Dict: Distance/duration matrix
        """
        params = {}
        if sources is not None:
            params["sources"] = ";".join(map(str, sources))
        if destinations is not None:
            params["destinations"] = ";".join(map(str, destinations))
        
        return self._request("table", profile, coordinates, params)

    def match(
        self, 
        coordinates: List[Coordinate], 
        *, 
        profile: OSRMProfile = OSRMProfile.DRIVING,
        timestamps: Optional[List[int]] = None,
        geometry: OSRMGeometry = OSRMGeometry.POLYLINE
    ) -> Dict:
        """
        Match GPS trace to road network.
        
        Args:
            coordinates (List[Coordinate]): GPS trace coordinates
            profile (OSRMProfile, optional): Routing profile
            timestamps (List[int], optional): Timestamps for each coordinate
            geometry (OSRMGeometry, optional): Geometry encoding format
        
        Returns:
            Dict: Matched route response
        """
        params = {"geometries": geometry.value}
        if timestamps is not None:
            params["timestamps"] = ";".join(map(str, timestamps))
        
        return self._request("match", profile, coordinates, params)

    def trip(
        self, 
        coordinates: List[Coordinate], 
        *, 
        profile: OSRMProfile = OSRMProfile.DRIVING,
        source: str = "first",
        destination: str = "last",
        roundtrip: bool = False,
        geometry: OSRMGeometry = OSRMGeometry.POLYLINE
    ) -> Dict:
        """
        Compute the shortest trip through all given coordinates.
        
        Args:
            coordinates (List[Coordinate]): Coordinates to visit
            profile (OSRMProfile, optional): Routing profile
            source (str, optional): Start point strategy
            destination (str, optional): End point strategy
            roundtrip (bool, optional): Force roundtrip
            geometry (OSRMGeometry, optional): Geometry encoding format
        
        Returns:
            Dict: Trip route response
        """
        params = {
            "source": source,
            "destination": destination,
            "roundtrip": str(roundtrip).lower(),
            "geometries": geometry.value
        }
        return self._request("trip", profile, coordinates, params)


def decode_polyline(encoded_polyline: str, precision: int = 5) -> List[Coordinate]:
    """
    Decode an encoded polyline into a list of coordinates.
    
    This implementation supports both polyline and polyline6 encoding.
    
    Args:
        encoded_polyline (str): Encoded polyline string
        precision (int, optional): Decimal precision (5 for standard, 6 for high precision)
    
    Returns:
        List[Coordinate]: Decoded coordinates
    
    Raises:
        ValueError: If the polyline is invalid
    """
    try:
        import polyline
    except ImportError:
        raise ImportError("Please install 'polyline' library: pip install polyline")
    
    try:
        decoded_coords = polyline.decode(encoded_polyline, precision)
        return [Coordinate(lon, lat) for lat, lon in decoded_coords]
    except Exception as e:
        raise ValueError(f"Failed to decode polyline: {e}") from e


def encode_polyline(coordinates: List[Coordinate], precision: int = 5) -> str:
    """
    Encode a list of coordinates into a polyline string.
    
    Args:
        coordinates (List[Coordinate]): Coordinates to encode
        precision (int, optional): Decimal precision (5 for standard, 6 for high precision)
    
    Returns:
        str: Encoded polyline string
    """
    try:
        import polyline
    except ImportError:
        raise ImportError("Please install 'polyline' library: pip install polyline")
    
    coord_tuples = [(coord.latitude, coord.longitude) for coord in coordinates]
    return polyline.encode(coord_tuples, precision)


@dataclass
class RouteAnalyzer:
    """
    Utility class for analyzing OSRM route responses.
    
    Provides methods to extract and process route information.
    
    Attributes:
        route_response (Dict): OSRM route response
    """
    route_response: Dict

    def total_distance(self, unit: str = 'km') -> float:
        """
        Calculate total route distance.
        
        Args:
            unit (str, optional): Distance unit ('km' or 'm')
        
        Returns:
            float: Total route distance
        """
        if not self.route_response.get('routes'):
            return 0.0
        
        distance_meters = self.route_response['routes'][0].get('distance', 0)
        return distance_meters / 1000 if unit == 'km' else distance_meters

    def total_duration(self, unit: str = 'min') -> float:
        """
        Calculate total route duration.
        
        Args:
            unit (str, optional): Duration unit ('min' or 'sec')
        
        Returns:
            float: Total route duration
        """
        if not self.route_response.get('routes'):
            return 0.0
        
        duration_seconds = self.route_response['routes'][0].get('duration', 0)
        return duration_seconds / 60 if unit == 'min' else duration_seconds

    def route_coordinates(self) -> List[Coordinate]:
        """
        Extract route coordinates from the response.
        
        Returns:
            List[Coordinate]: Coordinates along the route
        """
        if not self.route_response.get('routes'):
            return []
        
        geometry = self.route_response['routes'][0].get('geometry', '')
        return decode_polyline(geometry)

    def route_steps(self) -> List[Dict]:
        """
        Extract route navigation steps.
        
        Returns:
            List[Dict]: Detailed navigation steps
        """
        if not self.route_response.get('routes'):
            return []
        
        return self.route_response['routes'][0].get('legs', [])[0].get('steps', [])


def validate_coordinates(coordinates: List[Coordinate]) -> None:
    """
    Validate a list of coordinates.
    
    Args:
        coordinates (List[Coordinate]): Coordinates to validate
    
    Raises:
        ValueError: If coordinates are invalid
    """
    if not coordinates:
        raise ValueError("Coordinates list cannot be empty")
    
    for coord in coordinates:
        if not (-180 <= coord.longitude <= 180):
            raise ValueError(f"Invalid longitude: {coord.longitude}")
        if not (-90 <= coord.latitude <= 90):
            raise ValueError(f"Invalid latitude: {coord.latitude}")


# Example usage
if __name__ == "__main__":
    client = OSRMClient("http://localhost:5000")
    
    # Example route between two points
    coordinates = [
        Coordinate(101.62917, 3.10782),  # Start
        Coordinate(101.63917, 3.11782)   # End
    ]
    
    # Validate coordinates
    validate_coordinates(coordinates)
    
    # Compute route
    route_response = client.route(coordinates)
    
    # Analyze route
    analyzer = RouteAnalyzer(route_response)
    
    print(f"Total Distance: {analyzer.total_distance():.2f} km")
    print(f"Total Duration: {analyzer.total_duration():.2f} min")
    print(f"Route Coordinates: {len(analyzer.route_coordinates())} points")
    
    # Encode and decode polyline
    encoded = encode_polyline(coordinates)
    decoded = decode_polyline(encoded)
    print(f"Encoded Polyline: {encoded}")
    print(f"Decoded Coordinates: {decoded}")