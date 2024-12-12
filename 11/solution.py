import os
from functools import cache
from collections import Counter

INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse_input(string):
  return [int(n) for n in string.split()]

def string_from_file(filename):
  with open(filename) as input:
    return input.read()

@ cache
def blink_one_stone(stone):
  if stone == 0:
    return (1,)
  string = str(stone)
  if len(string) % 2 == 0:
    return (int(string[:len(string)//2]), int(string[len(string)//2:]))
  return (stone*2024,)

def blink(stone_counter):
  counter = {}
  for stone, nb in stone_counter.items():
    for new_stone in blink_one_stone(stone):
      if new_stone not in counter:
        counter[new_stone] = 0
      counter[new_stone] += nb
  return counter

def parts(string, blinks=25):
  stones = parse_input(string)
  stone_numbers = Counter(stones)
  for _ in range(blinks):
    stone_numbers = blink(stone_numbers)
  return sum(stone_numbers.values())

# Solution
print(parts(string_from_file(INPUT_FILE))) # 
print(parts(string_from_file(INPUT_FILE), 75)) # 

# Tests
assert parts('125 17') == 55312
