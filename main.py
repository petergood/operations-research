#!/usr/bin/env python3

import random
from knapsack import aco_knapsack
from tsp import aso_tsp
from abc_algorithm import abc_tsp
from visualization import draw_trace
import sys

if __name__ == "__main__":
  knapsack_iterations = 100
  knapsack_ants = 100
  knapsack_evaporation = 0.1
  knapsack_alpha = 1
  knapsack_beta = 1

  tsp_iterations = 10
  tsp_Q = 1
  tsp_evaporation = 0.1
  tsp_alpha = 0.5
  tsp_beta = 0.5
  tsp_heuristic_coefficient = 1


  # Example set of objects
  min_val = 1
  max_val = 100
  val_count = 20
  volume = random.uniform(min_val, max_val)
  objects = [tuple(random.uniform(min_val, volume) for _ in range(2)) 
    + tuple(tuple(random.uniform(min_val, max_val) for _ in range(2)) for _ in range(2))
    for _ in range(val_count)]

  print(f"Max volume: {volume}")

  profit, _, selected_objects = aco_knapsack(
    objects,
    max_volume=volume,
    cycle_count=knapsack_iterations,
    ant_count=knapsack_ants,
    evaporation=knapsack_evaporation,
    trail_weight=knapsack_alpha,
    attractiveness_weight=knapsack_beta
  )

  trace = None
  if len(sys.argv) == 1 or sys.argv[1] == 'ASO':
    trace = aso_tsp(
      orders=selected_objects, 
      iterations=tsp_iterations, 
      Q=tsp_Q, 
      alfa=tsp_alpha, 
      beta=tsp_beta, 
      heuristic_coefficient=tsp_heuristic_coefficient,
      evaporation=tsp_evaporation)
  else:
    population = 100
    onlooker_percent = 0.5
    employed_percent = 0.5
    scout_percent = 0.2
    cycle_limit = 10
    waggle_limit = 5
    trace = abc_tsp(selected_objects, population, onlooker_percent, employed_percent, scout_percent, cycle_limit, waggle_limit)

  

  print(f"Profit: {profit}")
  print(f"Trace: {trace}")

  draw_trace(selected_objects, trace)

