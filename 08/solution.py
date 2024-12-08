import os
from itertools import combinations
from math import gcd

TEST_INPUT = '''
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
'''
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse_data(string):
  grid = [line.strip() for line in string.split('\n') if line != '']
  height = len(grid)
  width = len(grid[0])
  antennae = {}
  for y in range(height):
    for x in range(width):
      char = grid[y][x]
      if char != '.':
        if char not in antennae:
          antennae[char] = []
        antennae[char].append((x,y))

  def within_boundaries(pos):
    x,y = pos
    return 0 <= x < width and 0 <= y < height
  return antennae, within_boundaries

def string_from_file(filename):
  with open(filename) as input:
    return input.read()

def within_boundaries(height, width, pos):
  x,y = pos
  return 0 <= x < width and 0 <= y < height

def debug_print(antinodes, antennae, height=12, width=12):
  antenna_by_pos = {}
  for t, positions in antennae.items():
    for pos in positions:
      antenna_by_pos[pos] = t
  for y in range(height):
    line = []
    for x in range(width):
      if (x,y) in antinodes:
        line.append('#')
      elif (x,y) in antenna_by_pos:
        line.append(antenna_by_pos[(x,y)])
      else:
        line.append('.')
    print(''.join(line))

def part_1(string):
  antennae, within_boundaries = parse_data(string)
  antinodes = set()
  for _, positions in antennae.items():
    for (ax,ay) , (bx,by) in combinations(positions,2):
      dx, dy = ax - bx, ay - by
      antinodes |= {(ax + dx, ay + dy),(bx - dx, by - dy)}
  return len([1 for pos in antinodes if within_boundaries(pos)])

def part_2(string):
  antennae, within_boundaries = parse_data(string)
  antinodes = set()
  for _, positions in antennae.items():
    for (ax,ay) , (bx,by) in combinations(positions,2):
      dx, dy = ax - bx, ay - by
      dx, dy = dx // gcd(dx,dy), dy // gcd(dx,dy)
      antinodes.add((ax,ay))
      # go both directions
      x,y = (ax + dx, ay + dy)
      while within_boundaries((x,y)):
        antinodes.add((x,y))
        x,y = x + dx, y + dy
      x,y = (ax - dx, ay - dy)
      while within_boundaries((x,y)):
        antinodes.add((x,y))
        x,y = x - dx, y - dy
  return len(antinodes)

# Solution
print(part_1(string_from_file(INPUT_FILE))) # 
print(part_2(string_from_file(INPUT_FILE))) # 

# Tests
assert part_1(TEST_INPUT) == 14
assert part_2(TEST_INPUT) == 34

TEST_1 = '''
..........
..........
..........
....a.....
........a.
.....a....
..........
..........
..........
..........
'''
assert part_1(TEST_1) == 4
