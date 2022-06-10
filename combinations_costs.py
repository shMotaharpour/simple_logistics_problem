from collections import Counter, defaultdict
from itertools import combinations, combinations_with_replacement
from typing import Callable, Dict, List

from class_libs import Point, Route
from utils import deliveries_distances, deliveries_impacts_on_routes


class Board:
    def __init__(self, routes: Dict[int, Route], deliveries: Dict[int, Point]):
        self.routes = routes
        self.deliveries = deliveries
        self.deliveries_routes_distances = deliveries_impacts_on_routes(routes, deliveries)
        self.deliveries_distances = deliveries_distances(deliveries)

    def __iter__(self):  # examines the total path added on the routes for different possible scenarios
        routes_orders = combinations_with_replacement(self.routes, r=len(self.deliveries))
        routes_orders = filter(Board.__capacity_check(self.routes), routes_orders)
        for routes_order in routes_orders:
            tmp = defaultdict(list)
            for i, j in zip(routes_order, self.deliveries):
                tmp[i].append(j)
            yield routes_order, sum(self.analysis_effect(*item) for item in tmp.items())

    @staticmethod
    def __capacity_check(
            routes: Dict[int, Route]
            ) -> Callable:  # examines the allowable capacity of each route for each scenario
        def checker(ord_tuple: tuple) -> bool:
            nums = Counter(ord_tuple)
            return all(routes[name].capacity >= count for name, count in nums.items())

        return checker

    def analysis_effect(
            self, route_id: int, points_id_list: List[int]
            ):  # calculate the total path added on each route for different possible scenarios
        clusters = defaultdict(list)
        effect = 0
        source = self.deliveries_routes_distances[route_id]
        for point_id in points_id_list:
            clusters[source[point_id][0]].append(point_id)

        for ref, cluster in clusters.items():
            if len(cluster) == 1:
                effect += source[cluster[0]][1]
            else:
                ref_start, ref_end = self.calc_ref_point(ref, route_id)
                if len(cluster) == 2:
                    a, b = cluster
                    effect += self.deliveries_distances[a][b]
                    ap, bp = [self.deliveries[c] for c in cluster]
                    effect += min(
                            ref_start.distance(ap) + ref_end.distance(bp),
                            ref_start.distance(bp) + ref_end.distance(ap),
                            )
                elif len(cluster) == 3:
                    tmp_dict = {
                        (start, end): ref_start.distance(self.deliveries[start]) + ref_end.distance(
                                self.deliveries[end])
                        for start, end in combinations(cluster, 2)}
                    start, end = min(tmp_dict, key=lambda x: tmp_dict[x])
                    effect += tmp_dict[(start, end)]
                    mid = [p for p in cluster if p not in (start, end)][0]
                    effect += sum(self.deliveries_distances[mid][x] for x in (start, end))
                effect -= ref_start.distance(ref_end)
        return effect

    def calc_ref_point(self, ref, route_id):
        if ref == 0:
            ref_start = self.routes[route_id].pickup
            ref_end = self.routes[route_id].missions[0]
        else:
            ref_start = self.routes[route_id].missions[ref - 1]
            ref_end = self.routes[route_id].missions[ref]
        return ref_start, ref_end
