import math
import random

def generate_random_path(coord1: tuple, coord2: tuple, interval: float = 5.0, deviation: float = 0.8) -> dict:
    """
    Generate a list of randomly generated points along a "true path" based on a theoretical path.
    
    Parameters:
        coord1 (tuple): Starting coordinate (lat1, lon1).
        coord2 (tuple): Ending coordinate (lat2, lon2).
        interval (float): Distance (in meters) between each perpendicular line.
        deviation (float): Maximum deviation (in meters) from the theoretical path.
    
    Returns:
        dict: A dict of randomly generated points (lat, lon) along the "true path."
    """
    def haversine(lat1, lon1, lat2, lon2):
        """Calculate the great-circle distance between two points on the Earth's surface."""
        R = 6371000  # Earth's radius in meters
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi / 2)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2)**2
        return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    def interpolate_point(lat1, lon1, lat2, lon2, fraction):
        """Interpolate a point between two coordinates."""
        lat = lat1 + fraction * (lat2 - lat1)
        lon = lon1 + fraction * (lon2 - lon1)
        return lat, lon
    
    def add_perpendicular_deviation(lat, lon, bearing, deviation):
        """Add a random perpendicular deviation to a point."""
        deviation_distance = random.uniform(-deviation, deviation)
        delta_lat = deviation_distance * math.cos(bearing) / 111320  # Convert meters to degrees latitude
        delta_lon = deviation_distance * math.sin(bearing) / (111320 * math.cos(math.radians(lat)))
        return lat + delta_lat, lon + delta_lon
    
    # Calculate the total distance between the two points
    total_distance = haversine(coord1[0], coord1[1], coord2[0], coord2[1])
    num_intervals = int(total_distance // interval)
    
    # Calculate the bearing of the theoretical path
    delta_lon = math.radians(coord2[1] - coord1[1])
    delta_phi = math.log(math.tan(math.pi / 4 + math.radians(coord2[0]) / 2) /
                         math.tan(math.pi / 4 + math.radians(coord1[0]) / 2))
    bearing = math.atan2(delta_lon, delta_phi) + math.pi / 2  # Perpendicular bearing
    
    # Generate the points
    true_path = []
    for i in range(1, num_intervals + 1):
        fraction = i * interval / total_distance
        interp_lat, interp_lon = interpolate_point(coord1[0], coord1[1], coord2[0], coord2[1], fraction)
        deviated_lat, deviated_lon = add_perpendicular_deviation(interp_lat, interp_lon, bearing, deviation)
        true_path.append({'lat': deviated_lat, 'lng': deviated_lon})
    
    return true_path