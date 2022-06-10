import json
from collections import defaultdict
from typing import Dict

import matplotlib.pyplot as plt
import numpy as np

from class_libs import Point, Route


def read_jsons(
        *,
        routes_file_path: int = './routes.json',
        deliveries_file_path: int = './deliveries.json'
        ) -> (Dict[int, Route], Dict[int, Point]):
    with open(routes_file_path) as f, open(deliveries_file_path) as d:
        routes = json.load(f)
        deliveries = json.load(d)

    routes = [Route(route) for route in routes]
    routes = {route.id: route for route in routes}
    deliveries = [Point(**delivery) for delivery in deliveries]
    deliveries = {delivery.id: delivery for delivery in deliveries}
    return routes, deliveries


def compare_rebuild_routes(routes: Dict[int, Route], show=False):
    """Simple function to reorder missions in routes"""
    a = []
    for route in routes.values():
        print(route.route_total_timestamps)
        route.rebuild_missions()
        print(route.route_total_timestamps, end='\n\n')
        if show:
            a.append(route.plot(show=False))
    if show:
        start_points = np.array([[route.pickup.lat, route.pickup.lon] for route in routes.values()]).T
        plt.scatter(start_points[0], start_points[1], 'k')
        [plt.plot(*b, c) for b, c in zip(a, '+-. *- --'.split())]
        plt.show()


def plot_deliveries_routes(routes: Dict[int, Route], deliveries: Dict[int, Point]):
    """plot Deliveries and Missions in order of Routes"""
    start_points = np.array([[route.pickup.lat, route.pickup.lon] for route in routes.values()]).T
    plt.scatter(start_points[0], start_points[1], color='red', marker='o', label='route start')
    deliveries_points = np.array([[delivery.lat, delivery.lon] for delivery in deliveries.values()]).T
    plt.scatter(deliveries_points[0], deliveries_points[1], color='black', marker='o', label='delivery point')
    routes_lines = [route.plot(show=False) for route in routes.values()]
    [plt.plot(*b, c) for b, c in zip(routes_lines, '+-. *- ^-'.split())]
    plt.legend()
    plt.show()


def deliveries_impacts_on_routes(routes: Dict[int, Route], deliveries: Dict[int, Point]):
    """Calculates the distance increase due to the addition of a delivery point to a route for all cases"""
    distances = defaultdict(dict)
    for route_id, route in routes.items():
        for delivery_id, delivery in deliveries.items():
            distances[route_id][delivery_id] = route.minimum_distance_increase(delivery)
    return distances


def deliveries_distances(deliveries: Dict[int, Point]):
    """Calculates the distance between of delivery points"""
    from itertools import combinations
    distances = defaultdict(dict)
    for a, b in combinations(deliveries, r=2):
        distances[a][b] = distances[b][a] = Point.distance(deliveries[a], deliveries[b])
    return distances
