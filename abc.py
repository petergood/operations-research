import math
import random
from visualization import draw_trace


class Bee:
    def __init__(self, path, distance):
        self.role = None
        self.path = path
        self.distance = distance
        self.cycle = 0
        self.probability = 0


def d(location_a, location_b):
    return math.dist(location_a, location_b)


def point_filter(point, path, orders):
    if point in path:
        return False
    if (point in orders) and (orders[point] not in path):
        return False

    return True


def get_random_path(orders_map):
    all_points = list(orders_map.keys()) + list(orders_map.values())
    path = []
    while len(path) != len(all_points):
        allowed_points = list(filter(lambda point: point_filter(point, path, orders_map),
                                     all_points))
        idx = random.randint(0, len(allowed_points)-1)
        path.append(allowed_points[idx])
    return path


def get_path_distance(path):
    dist = 0
    for i in range(1, len(path)):
        dist += d(path[i-1], path[i])
    return dist


def mutate_path(path, orders_map):
    idx = random.randint(1, len(path)-2)
    while orders_map.get(path[idx+1], None) == path[idx]:
        idx = random.randint(1, len(path)-2)
    path[idx], path[idx + 1] = path[idx + 1], path[idx]

    return path


def initialize_hive(population, orders_map):
    hive = []
    for _ in range(population):
        random_path = get_random_path(orders_map)
        distance = get_path_distance(random_path)
        hive.append(Bee(random_path, distance))

    return hive


def assign_roles(hive, employed_count, onlooker_count):
    for i in range(onlooker_count):
        hive[i].role = "ONLOOKER"
    for i in range(employed_count):
        hive[i + onlooker_count].role = "EMPLOYED"
        hive[i + onlooker_count].distance = get_path_distance(hive[i].path)

    return hive


def employed_cycle(bee, best_dist, orders_map, waggle_limit):
    new_path = mutate_path(bee.path, orders_map)
    new_dist = get_path_distance(new_path)

    if new_dist < best_dist:
        bee.path = new_path
        bee.distance = new_dist
        bee.cycle = 0
    else:
        bee.cycle += 1
    if bee.cycle > waggle_limit:
        bee.role = "SCOUT"
    return bee.distance, bee.path


def scout_cycle(bee, orders_map):
    new_path = get_random_path(orders_map)
    bee.path = new_path
    bee.distance = get_path_distance(new_path)
    bee.role = "EMPLOYED"
    bee.cycle = 0


def calculate_probability(hive, best_dist):
    total_dist = 0
    for h in hive:
        total_dist += h.distance
    for h in hive:
        h.probability = h.distance/total_dist

def neighborhood_search(hive, best_dist):
    calculate_probability(hive, best_dist)
    distribution = map(lambda bee: bee.probability, hive)
    bee = random.choices(hive, distribution)[0]

    return bee.path


def onlooker_cycle(hive, best_dist, best_path, orders_map):
    for i in range(len(hive)):
        if hive[i].role == "ONLOOKER":
            new_path = neighborhood_search(hive, best_dist)
            mutated_path = mutate_path(new_path, orders_map)
            new_dist = get_path_distance(mutated_path)
            if new_dist < best_dist:
                best_dist = new_dist
                best_path = mutated_path
    return best_dist, best_path


def waggle_dance(hive, best_dist, orders_map, scout_count, waggle_limit):
    best_path = []
    all_results = []

    for i in range(len(hive)):
        if hive[i].role == "EMPLOYED":
            dist, path = employed_cycle(
                hive[i], best_dist, orders_map, waggle_limit)
            if dist < best_dist:
                best_dist = dist
                best_path = path
            all_results.append((i, dist))
        elif hive[i].role == "SCOUT":
            scout_cycle(hive[i], orders_map)

    # set bees with the worts results as SCOUT bee
    all_results.sort(reverse=True, key=lambda res: res[1])
    new_scouts = all_results[0:int(scout_count)]
    for sc in new_scouts:
        hive[sc[0]].role = "SCOUT"

    return best_dist, best_path


def abc_tsp(orders, population, onlooker_percent, employed_percent, scout_percent, cycle_limit, waggle_limit):
    orders_map = dict()
    for _, _, pickup_point, drop_point in orders:
        orders_map[drop_point] = pickup_point

    onlooker_count = math.floor(population * onlooker_percent)
    employed_count = math.floor(population * employed_percent)
    scout_count = math.floor(population * scout_percent)

    hive = initialize_hive(population, orders_map)
    assign_roles(hive, employed_count, onlooker_count)

    best_path = get_random_path(orders_map)
    best_dist = get_path_distance(best_path)

    for _ in range(cycle_limit):
        waggled_dist, waggled_path = waggle_dance(
            hive, best_dist, orders_map, scout_count, waggle_limit)
        if waggled_dist < best_dist:
            best_dist = waggled_dist
            best_path = waggled_path

        searched_dist, searched_path = onlooker_cycle(
            hive, best_dist, best_path, orders_map)
        if searched_dist < best_dist:
            best_dist = searched_dist
            best_path = searched_path

    print(best_dist)
    return best_path


if __name__ == "__main__":
    orders = [(1, 1, (random.uniform(-1000, 1000), random.uniform(-1000, 1000)),
               (random.uniform(-1000, 1000), random.uniform(-1000, 1000))) for _ in range(5)]
    population = 100
    onlooker_percent = 0.5
    employed_percent = 0.5
    scout_percent = 0.2
    cycle_limit = 10
    waggle_limit = 5

    best_path = abc_tsp(orders, population, onlooker_percent,
                        employed_percent, scout_percent, cycle_limit, waggle_limit)

    trace = []
    for i in range(1, len(best_path)):
        trace.append((best_path[i-1], best_path[i]))

    draw_trace(orders, trace)
