"""
Routing Service
Uses OpenRouteService API for route calculation
"""
import requests
from typing import Dict, List, Tuple
import os


class RoutingService:
    """Service for calculating routes using OpenRouteService"""
    
    # Using public demo server (rate limited) - users should get their own API key
    ORS_API_URL = "https://api.openrouteservice.org/v2/directions/driving-hgv"
    
    def __init__(self, api_key: str = None):
        """
        Initialize routing service
        
        Args:
            api_key: OpenRouteService API key (optional, will use env var if not provided)
        """
        self.api_key = api_key or os.getenv('ORS_API_KEY', '')
    
    def geocode_address(self, address: str) -> Tuple[float, float]:
        """
        Convert address to coordinates using Nominatim (OpenStreetMap)
        
        Args:
            address: Address string
            
        Returns:
            Tuple of (latitude, longitude)
        """
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': address,
            'format': 'json',
            'limit': 1
        }
        headers = {
            'User-Agent': 'ELD-Trip-Planner/1.0'
        }
        
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data and len(data) > 0:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                # Validate coordinates are reasonable (world bounds)
                if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
                    raise ValueError(f"Invalid coordinates for address: {address}")
                return lat, lon
            else:
                raise ValueError(f"Could not geocode address: {address}")
        except Exception as e:
            raise Exception(f"Geocoding error: {str(e)}")
    
    def calculate_route(self, start_coords: Tuple[float, float], 
                       end_coords: Tuple[float, float],
                       waypoints: List[Tuple[float, float]] = None) -> Dict:
        """
        Calculate route between coordinates
        
        Args:
            start_coords: Starting (lat, lon)
            end_coords: Ending (lat, lon)
            waypoints: Optional list of waypoint coordinates
            
        Returns:
            Dictionary with route information
        """
        # Build coordinates list [lon, lat] format for ORS
        coordinates = [[start_coords[1], start_coords[0]]]
        
        if waypoints:
            for wp in waypoints:
                coordinates.append([wp[1], wp[0]])
        
        coordinates.append([end_coords[1], end_coords[0]])
        
        # Try with API key first, fall back to OSRM if no key
        if self.api_key:
            return self._calculate_route_ors(coordinates)
        else:
            return self._calculate_route_osrm(coordinates)
    
    def _calculate_route_ors(self, coordinates: List[List[float]]) -> Dict:
        """Calculate route using OpenRouteService"""
        headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }
        
        body = {
            'coordinates': coordinates,
            'instructions': True,
            'units': 'mi'
        }
        
        try:
            response = requests.post(
                self.ORS_API_URL,
                json=body,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            
            route = data['routes'][0]
            
            return {
                'distance_miles': route['summary']['distance'] * 0.000621371,  # meters to miles
                'duration_hours': route['summary']['duration'] / 3600,  # seconds to hours
                'geometry': route['geometry'],
                'instructions': self._format_instructions(route.get('segments', []))
            }
        except Exception as e:
            # Fallback to OSRM if ORS fails
            print(f"ORS routing failed: {str(e)}, falling back to OSRM")
            return self._calculate_route_osrm(coordinates)
    
    def _calculate_route_osrm(self, coordinates: List[List[float]]) -> Dict:
        """
        Calculate route using OSRM (free, no API key needed)
        Fallback option when ORS is not available
        """
        # Format coordinates for OSRM: lon,lat;lon,lat
        coords_str = ';'.join([f"{lon},{lat}" for lon, lat in coordinates])
        
        url = f"https://router.project-osrm.org/route/v1/driving/{coords_str}"
        params = {
            'overview': 'full',
            'geometries': 'geojson',
            'steps': 'true'
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data['code'] != 'Ok':
                raise Exception(f"OSRM routing error: {data.get('message', 'Unknown error')}")
            
            route = data['routes'][0]
            
            return {
                'distance_miles': route['distance'] * 0.000621371,  # meters to miles
                'duration_hours': route['duration'] / 3600,  # seconds to hours
                'geometry': route['geometry'],
                'instructions': self._format_osrm_instructions(route.get('legs', []))
            }
        except Exception as e:
            raise Exception(f"Routing error: {str(e)}")
    
    def _format_instructions(self, segments: List[Dict]) -> List[Dict]:
        """Format ORS instructions"""
        instructions = []
        for segment in segments:
            for step in segment.get('steps', []):
                instructions.append({
                    'instruction': step.get('instruction', ''),
                    'distance_miles': step.get('distance', 0) * 0.000621371,
                    'duration_hours': step.get('duration', 0) / 3600
                })
        return instructions
    
    def _format_osrm_instructions(self, legs: List[Dict]) -> List[Dict]:
        """Format OSRM instructions"""
        instructions = []
        for leg in legs:
            for step in leg.get('steps', []):
                maneuver = step.get('maneuver', {})
                instruction = f"{maneuver.get('type', 'continue').title()}"
                if 'name' in step and step['name']:
                    instruction += f" onto {step['name']}"
                
                instructions.append({
                    'instruction': instruction,
                    'distance_miles': step.get('distance', 0) * 0.000621371,
                    'duration_hours': step.get('duration', 0) / 3600
                })
        return instructions
    
    def get_route_with_stops(self, current_location: str, pickup_location: str, 
                            dropoff_location: str) -> Dict:
        """
        Calculate complete route with pickup and dropoff
        
        Args:
            current_location: Current location address
            pickup_location: Pickup location address
            dropoff_location: Dropoff location address
            
        Returns:
            Dictionary with complete route information
        """
        # Geocode all locations
        current_coords = self.geocode_address(current_location)
        pickup_coords = self.geocode_address(pickup_location)
        dropoff_coords = self.geocode_address(dropoff_location)
        
        # Calculate route segments
        # Segment 1: Current to Pickup
        route_to_pickup = self.calculate_route(current_coords, pickup_coords)
        
        # Segment 2: Pickup to Dropoff
        route_to_dropoff = self.calculate_route(pickup_coords, dropoff_coords)
        
        # Combine routes
        total_distance = route_to_pickup['distance_miles'] + route_to_dropoff['distance_miles']
        total_duration = route_to_pickup['duration_hours'] + route_to_dropoff['duration_hours']
        
        return {
            'current_location': {
                'address': current_location,
                'coordinates': current_coords
            },
            'pickup_location': {
                'address': pickup_location,
                'coordinates': pickup_coords
            },
            'dropoff_location': {
                'address': dropoff_location,
                'coordinates': dropoff_coords
            },
            'route_to_pickup': route_to_pickup,
            'route_to_dropoff': route_to_dropoff,
            'total_distance_miles': total_distance,
            'total_duration_hours': total_duration
        }
