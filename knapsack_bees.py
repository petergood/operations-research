#!/usr/bin/env python3

import random
from numpy.random import choice

def abc_knapsack(objects, max_volume, employed_count, onlooker_count, iter_max, p_min, p_max, exp):
  r = [objects[i][1] / objects[i][0] for i in range(0, len(objects))]
  weights = [objects[i][0] for i in range(0, len(objects))]
  mean_r = sum(r) / len(r)
  p = [min(1, (max_volume / sum(weights)) * (r[i] / mean_r)) for i in range(0, len(r))]
  p_ind = list(zip(p, range(0, len(p))))
  p_ind.sort()

  def get_state_profit(state):
    return sum([state[i] * objects[i][1] for i in range(0, len(state))])

  def get_state_volume(state):
    return sum([state[i] * objects[i][0] for i in range(0, len(state))])

  states = []

  def get_next_state(state, iter):
    p_change = p_min + (iter / iter_max) * (p_max - p_min)

    def get_candidate():
      return list(map(lambda val: choice([0 if val == 1 else 1, val], p=[p_change, 1 - p_change]), state))

    candidate = get_candidate()
    while get_state_volume(candidate) > max_volume:
      candidate = get_candidate()

    return candidate

  def get_initial_state():
    cap = 0
    state = [0 for _ in range(0, len(objects))]

    for i in range(len(objects)):
      (prob, ind) = p_ind[i]
      selection = choice([1, 0], p=[prob, 1 - prob])
      state[ind] = selection

      if selection == 1:
        cap += objects[ind][0]

      if cap >= max_volume:
        break

    return state

  for i in range(0, employed_count):
    states.append(get_initial_state())
    
  best_profit = 0
  best_sol = []

  for iter in range(0, iter_max):
    abandoned = []

    for i in range(0, len(states)):
      next_state = get_next_state(states[i], iter)
      profit = get_state_profit(next_state)

      if (profit > get_state_profit(states[i])):
        states[i] = next_state
      else:
        abandoned.append(i)

      if (profit > best_profit):
        best_profit = profit
        best_sol = next_state

    sum_profits = sum([get_state_profit(state) ** exp for state in states])
    probs = [(get_state_profit(state) ** exp) / sum_profits for state in states]

    for i in range(0, onlooker_count):
      selected = choice(range(0, len(states)), p=probs)
      next_state = get_next_state(states[selected], iter)
      profit = get_state_profit(next_state)

      if profit > best_profit:
        best_profit = profit
        best_sol = next_state

    for ind in abandoned:
      states[ind] = get_initial_state()

  return best_profit, best_sol

if __name__ == "__main__":
  min_val = 1
  max_val = 100
  val_count = 10

  volume = random.uniform(max_val, max_val + 300)
  # weight, price
  objects = [(random.uniform(min_val, volume), random.uniform(min_val, max_val), 0, 0) for _ in range(val_count)]

  # print(objects)
  # print(volume)

  profit, selected = abc_knapsack(
    objects, 
    volume, 
    employed_count=10,
    onlooker_count=10,
    iter_max=50,
    p_min=0.04,
    p_max=0.12,
    exp=3
  )

  print(f"Volume: {volume}")
  print(f"Objects: {objects}")
  print(f"Profit: {profit}")
  print(f"Selected: {selected}")
  print(f"Selected volume: {sum([selected[i] * objects[i][0] for i in range(0, len(selected))])}")
