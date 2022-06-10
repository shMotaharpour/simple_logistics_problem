from typing import List

import numpy as np


class Point:
    """any kind of point on map such as delivery or mission"""
    try:
        from haversine import haversine
    except ModuleNotFoundError:
        print('Should Install haversine package to use haversine distance')
        haversine = None

    def __init__(self, id, lat, lon, **kwargs):
        self.id: int = id
        self.lat: float = lat
        self.lon: float = lon

    def __repr__(self):
        return f'[{self.id}]<{self.lat:0.2f},{self.lon:0.2f}>'

    def distance(self, other):
        assert isinstance(other, Point)
        if Point.haversine:
            return Point.haversine((self.lat, self.lon), (other.lat, other.lon))
        return ((self.lon - other.lon) ** 2 + (self.lat - other.lat) ** 2) ** 0.5


class Route:
    """a class to define each route and its parameters"""
    def __init__(self, routs_dict: dict, capacity=3, velocity=10):
        self.id: int = routs_dict['id']
        self._capacity = capacity
        self.missions: List[Point] = []
        self.extract_missions(routs_dict['missions'])
        self.pickup = Point(
                id=self.id,
                lat=routs_dict['pickup_lat'],
                lon=routs_dict['pickup_lon'],
                )
        self._news_missions: List[Point] = []
        self.velocity = velocity
        self._need_refresh = True
        self._timestamps: List[float] = []

    def __repr__(self):
        return f'[{self.id}]<missions:{len(self.missions) + len(self._news_missions)}, capacity:{self.capacity}'

    @property
    def capacity(self):
        return self._capacity - len(self._news_missions)

    def _refresh(self):
        if self._need_refresh:
            self._calc_timestamps()

    def add_mission(self, mission):  # adds a delivery point to the route list but does not locate
        self._need_refresh = True
        self._news_missions.append(mission)

    @property
    def timestamps(self):  # return timestamps list of route missions
        self._refresh()
        return self._timestamps

    def extract_missions(self, missions: dict):  # adds predefined mission points directly to route missions list
        self.missions = [Point(**data) for data in missions]

    def _calc_timestamps(self):
        if len(self._news_missions):
            self.attach_deliveries_to_missions()
        self._timestamps = [a.distance(b) / self.velocity for a, b in zip([self.pickup] + self.missions, self.missions)]
        self._need_refresh = False

    @property
    def route_total_timestamps(self):  # calculate total route time trip
        self._refresh()
        return sum(self._timestamps)

    def attach_deliveries_to_missions(self):  # locates added delivery points along the route
        for delivery in self._news_missions:
            self._delivery_join(delivery)
        self._capacity -= len(self._news_missions)
        self._news_missions = []

    def _delivery_join(self, delivery: Point):  # locates single delivery point along the route
        inx, _ = self.minimum_distance_increase(delivery)
        self.missions.insert(inx, delivery)

    def minimum_distance_increase(self, point: Point):  # finds the least possible distance increase
        dif_distances = []
        a = self.pickup
        a_path = point.distance(a)
        b_path = None
        for b in self.missions:
            b_path = point.distance(b)
            ab_path = a.distance(b)
            dif_distances.append(a_path + b_path - ab_path)
            a, a_path = b, b_path
        else:
            if b_path:
                dif_distances.append(b_path)
        inx = np.argmin(dif_distances)
        return inx, dif_distances[inx]

    def plot(self, show=True):
        try:
            import matplotlib.pyplot as plt
        except ModuleNotFoundError:
            print('Should Install matplotlib package to use plot')
            return None

        if len(self._news_missions):
            self.attach_deliveries_to_missions()
        points = np.array([[point.lat, point.lon] for point in [self.pickup, *self.missions]])
        if show:
            plt.plot(points[:, 0], points[:, 1], '*-')
            plt.show()
        else:
            return points[:, 0], points[:, 1]

    def rebuild_missions(self):  # tries to redistribute mission points in the route
        tmp = self.capacity
        self._news_missions += self.missions[1:]
        self.missions = self.missions[:1]
        self._need_refresh = True
        self.attach_deliveries_to_missions()
        self._capacity = tmp
