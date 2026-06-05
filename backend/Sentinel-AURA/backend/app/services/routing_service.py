import openrouteservice
import logging
from typing import List, Dict, Any
from app.config.settings import settings

logger = logging.getLogger(__name__)

class RoutingService:
    def __init__(self):
        # You'll need to get an API key from https://openrouteservice.org/
        # For now, using a placeholder - replace with actual key
        self.client = openrouteservice.Client(key=settings.ors_api_key or "your_openrouteservice_api_key")

    async def get_route(self, source: Dict[str, float], destination: Dict[str, float], profile: str = "driving-car") -> Dict[str, Any]:
        """Get route from source to destination using OpenRouteService"""
        try:
            coords = [
                [source['lng'], source['lat']],  # ORS expects [lng, lat]
                [destination['lng'], destination['lat']]
            ]

            routes = self.client.directions(
                coordinates=coords,
                profile=profile,
                format='geojson',
                instructions=False,  # We don't need turn-by-turn instructions
                geometry_simplify=True
            )

            if routes and 'features' in routes and len(routes['features']) > 0:
                route = routes['features'][0]
                geometry = route['geometry']['coordinates']

                # Convert back to [lat, lng] format
                route_points = [{'lat': coord[1], 'lng': coord[0]} for coord in geometry]

                # Extract route metadata
                properties = route.get('properties', {})
                summary = properties.get('summary', {})

                return {
                    'route_points': route_points,
                    'distance': summary.get('distance', 0),  # in meters
                    'duration': summary.get('duration', 0),  # in seconds
                    'bbox': route.get('bbox', []),
                    'profile': profile
                }
            else:
                raise Exception("No route found")

        except Exception as e:
            logger.error(f"Routing error: {e}")
            # Fallback: return straight line route
            return {
                'route_points': [
                    {'lat': source['lat'], 'lng': source['lng']},
                    {'lat': destination['lat'], 'lng': destination['lng']}
                ],
                'distance': 0,
                'duration': 0,
                'bbox': [],
                'profile': profile,
                'fallback': True
            }

    async def get_alternative_routes(self, source: Dict[str, float], destination: Dict[str, float], alternatives: int = 2) -> List[Dict[str, Any]]:
        """Get multiple route alternatives"""
        try:
            coords = [
                [source['lng'], source['lat']],
                [destination['lng'], destination['lat']]
            ]

            routes = self.client.directions(
                coordinates=coords,
                profile='driving-car',
                format='geojson',
                instructions=False,
                alternatives=alternatives,
                geometry_simplify=True
            )

            alternative_routes = []
            if routes and 'features' in routes:
                for route in routes['features']:
                    geometry = route['geometry']['coordinates']
                    route_points = [{'lat': coord[1], 'lng': coord[0]} for coord in geometry]

                    properties = route.get('properties', {})
                    summary = properties.get('summary', {})

                    alternative_routes.append({
                        'route_points': route_points,
                        'distance': summary.get('distance', 0),
                        'duration': summary.get('duration', 0),
                        'bbox': route.get('bbox', []),
                    })

            return alternative_routes

        except Exception as e:
            logger.error(f"Alternative routes error: {e}")
            return []

# Global instance
routing_service = RoutingService()