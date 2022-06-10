from operator import itemgetter
from typing import Tuple
from collections import defaultdict
from combinations_costs import Board
from utils import plot_deliveries_routes, read_jsons
from pprint import pprint as pp

if __name__ == '__main__':
    routes, deliveries = read_jsons(
            # routes_file_path='./test/routes.json',
            # deliveries_file_path='./test/deliveries.json'
            )
    plot_deliveries_routes(routes, deliveries)  # Routes and Delivery points have been plot before adding
    board = Board(routes, deliveries)  # an object of calculation Board
    costs = [*board]  # Possible arrangements for adding delivery points and distance changes results
    best: Tuple[tuple, int] = min(board, key=itemgetter(-1))  # best arrangement for adding delivery points
    arrangement = defaultdict(list)
    for route, (delivery_id, delivery) in zip(best[0], deliveries.items()):
        routes[route].add_mission(delivery)
        arrangement[route].append(delivery_id)
    plot_deliveries_routes(routes, deliveries)  # Routes and Delivery points after adding
    print(*costs, sep='\n')
    print('best arrangement for adding delivery points:')
    pp(arrangement)
