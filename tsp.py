import math
import random
from visualization import draw_trace
from collections import defaultdict


def d(location_a, location_b):
    return math.dist(location_a, location_b)


def point_filter(point, visited, orders):
    if point in visited:
        return False
    if (point in orders) and (orders[point] not in visited):
        return False

    return True


def p(orders, point_a, point_b, tau, all_points, visited_points, alfa, beta, heuristic_coefficient):
    if point_b in visited_points:
        return 0
    if (point_b in orders) and (orders[point_b] not in visited_points):
        return 0

    ij = tuple(sorted([point_a, point_b]))

    t = tau[ij]
    n = d(point_a, point_b)**(-1) * heuristic_coefficient
    nominator = (t**alfa) * (n**beta)

    allowed_points = list(filter(lambda point: point_filter(point, visited_points, orders),
                                 all_points))
    iks = map(lambda point: tuple(sorted([point_a, point])), allowed_points)
    values_to_sum = list(map(lambda ik: (
        tau[ik]**alfa)*(d(ik[0], ik[1])**(-1)*heuristic_coefficient)**beta, iks))
    denominator = sum(values_to_sum)

    if denominator == 0:
        return n
    return nominator / denominator


def add_pheromone_map(map_1, map_2):
    for key in map_2:
        map_1[key] += map_2[key]

def evaporate(pheromone_map, evaporation):
    for key in pheromone_map:
        pheromone_map[key] *= evaporation

def choose_next_point(orders, current_position, all_points, visited, pheromone_map, alfa, beta, heuristic_coefficient):
    distribution = map(lambda point: p(
        orders, current_position, point, pheromone_map, all_points, visited, alfa, beta, heuristic_coefficient), all_points)
    return random.choices(all_points, distribution)[0]


def ant_iteration(orders, starting_point, all_points, pheromone_map, Q, alfa, beta, heuristic_coefficient):
    local_pheromone_map = pheromone_map.copy()
    visited = [starting_point]
    trace = []
    trace_length = 0
    current_position = starting_point
    while set(visited) != set(all_points):
        prev_position = current_position
        current_position = choose_next_point(
            orders, current_position, all_points, visited, pheromone_map, alfa, beta, heuristic_coefficient)
        visited.append(current_position)
        trace.append(tuple([prev_position, current_position]))
        trace_length += d(current_position, prev_position)

    pheromone = Q/trace_length
    for edge in trace:
        local_pheromone_map[edge] += pheromone

    return local_pheromone_map, trace, trace_length


def aso_tsp(orders, iterations, Q, alfa, beta, heuristic_coefficient, evaporation):
    orders_map = dict()
    for _, _, pickup_point, drop_point in orders:
        orders_map[drop_point] = pickup_point
    best_trace = []
    min_length = -1
    all_points = list(orders_map.keys()) + list(orders_map.values())
    starting_points = list(orders_map.values())
    pheromone_map = defaultdict(int)
    for i in range(iterations):
        pheromone_map_acc = pheromone_map.copy()
        for point in starting_points:
            update_for_pheromone_map, trace, trace_length = ant_iteration(
                orders, point, all_points, pheromone_map, Q, alfa, beta, heuristic_coefficient)
            add_pheromone_map(pheromone_map_acc, update_for_pheromone_map)
            if min_length == -1:
                min_length = trace_length
            if trace_length < min_length:
                min_length = trace_length
                best_trace = trace
        add_pheromone_map(pheromone_map, pheromone_map_acc)
        evaporate(pheromone_map, evaporation)

    return best_trace


if __name__ == "__main__":
    orders = [(1, 1,(random.uniform(-1000, 1000), random.uniform(-1000, 1000)),
            (random.uniform(-1000, 1000), random.uniform(-1000, 1000))) for _ in range(5)]
    trace = aso_tsp(orders, 10, 1, 0.5, 0.5, 1, 0.1)
    draw_trace(orders, trace)

