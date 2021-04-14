#!/usr/bin/env python3

import random
from functools import reduce
from numpy.random import choice

def aco_knapsack(objects, max_volume, cycle_count, ant_count, evaporation, trail_weight, attractiveness_weight):
  objects_filtered = list(filter(lambda obj: obj[0] <= max_volume, objects))
  if len(objects_filtered) == 0:
    return 0, 0, []

  objects = list(map(lambda obj: (obj[0], obj[1]), objects_filtered))
  n = len(objects)
  trail = [1] * len(objects)

  def get_probabilities(neighbours):
    s = reduce(lambda acc, j: acc + (trail[j] ** trail_weight) * (((objects[j][1] / objects[j][1] ** 2)) ** attractiveness_weight), neighbours, 0)
    return list(map(lambda j: ((trail[j] ** trail_weight) * (((objects[j][1] / objects[j][1] ** 2)) ** attractiveness_weight)) / s if j in neighbours else 0, range(n)))

  solution = []
  solution_volume = 0
  max_profit = 0

  for _ in range(cycle_count):
    ant_results = []

    for _ in range(ant_count):
      current_volume = max_volume
      neighbours = set(range(n))
      partial_solution = []
      profit = 0

      while (current_volume > 0):
        dist = get_probabilities(neighbours)
        j = choice(n, p=dist)
        partial_solution.append(j)

        (volume, cost) = objects[j]
        current_volume -= volume
        profit += cost
        neighbours = set(filter(lambda ind: objects[ind][0] <= current_volume and ind != j, neighbours))

        if len(neighbours) == 0:
          break
      
      if profit > max_profit:
        max_profit = profit
        solution = partial_solution
        solution_volume = max_volume - current_volume

      ant_results.append((profit, partial_solution))

    trail = list(map(lambda t: t * evaporation, trail))

    for result in ant_results:
      (ant_profit, ant_solution) = result
      delta = 1 / (1 + ((max_profit - ant_profit) / max_profit))
      
      for j in ant_solution:
        trail[j] += delta

  return max_profit, solution_volume, list(map(lambda i: objects_filtered[i], solution))

if __name__ == "__main__":
  min_val = 1
  max_val = 100
  val_count = 5

  volume = random.uniform(min_val, max_val)
  objects = [(random.uniform(min_val, volume), random.uniform(min_val, volume), 0, 0) for _ in range(val_count)]

  print(f"Volume: {volume}")

  profit, solution_volume, selected = aco_knapsack(
    objects,
    max_volume=volume,
    cycle_count=100,
    ant_count=100,
    evaporation=0.1,
    trail_weight=1,
    attractiveness_weight=1
  )

  print(f"Profit: {profit}; volume: {solution_volume}; selected: {selected}")