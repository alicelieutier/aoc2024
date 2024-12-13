import os
from collections import deque
from itertools import cycle

INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def string_from_file(filename):
  with open(filename) as input:
    return input.read()
  
class Grid:
  def __init__(self, string):
    self.grid = [line for line in string.split('\n') if line != '']
    self.height = len(self.grid)
    self.width = len(self.grid[0])

  # Virtually pad the grid
  def get(self, pos):
    x, y = pos
    if 0 <= x < self.width and 0 <= y < self.height:
      return self.grid[y][x]
    return None

  def neighbours(self, pos):
    x,y = pos
    yield (x-1, y)
    yield (x+1, y)
    yield (x, y-1)
    yield (x, y+1)

  def explore_region(self, pos):
    plant = self.get(pos)
    plots = set()
    perimeter = 0
    edges= set()
    to_visit = deque([pos])
    while len(to_visit) > 0:
      current = to_visit.popleft()
      if current in plots:
        continue
      plots.add(current)
      for neighbour in self.neighbours(current):
        if neighbour not in plots:
          if self.get(neighbour) == plant:
            to_visit.append(neighbour)
          else:
            perimeter += 1
            edges.add((current, neighbour))
    return plots, len(plots), perimeter, edges

def sides_from_edges(edges):
  sides = 0
  while len(edges) > 0:
    (x,y),(xout,yout) = edges.pop()
    sides += 1
    # vertical or horizontal edge?
    if x == xout:
      possible = ((x-1,y),(x-1,yout))
      # go left
      while possible in edges:
        edges -= {possible}
        possible = ((possible[0][0]-1, y),(possible[0][0]-1, yout))
      # go right
      possible = ((x+1,y),(x+1,yout))
      while possible in edges:
        edges -= {possible}
        possible = ((possible[0][0]+1, y),(possible[0][0]+1, yout))

    elif y == yout:
      possible = ((x,y-1),(xout,y-1))
      # go up
      while possible in edges:
        edges -= {possible}
        possible = ((x, possible[0][1]-1),(xout, possible[0][1]-1))
      # go down
      possible = ((x,y+1),(xout,y+1))
      while possible in edges:
        edges -= {possible}
        possible = ((x, possible[0][1]+1),(xout, possible[0][1]+1))
    else:
      print(f'WHAT? {(x,y),(xout,yout)}')
  return sides

# Due to "modern" business practices, the price of fence required for a region
# is found by multiplying that region's area by its perimeter.
# The total price of fencing all regions on a map is found by
# adding together the price of fence for every region on the map.
def part_1(string):
  grid = Grid(string)
  visited_plots = set()
  price = 0
  for y in range(grid.height):
    for x in range(grid.width):
      if (x,y) not in visited_plots:
        plots, area, perimeter, _ = grid.explore_region((x,y))
        visited_plots |= plots
        price += area * perimeter
  return price

# find the number of sides instead of the perimeter
def part_2(string):
  grid = Grid(string)
  visited_plots = set()
  price = 0
  for y in range(grid.height):
    for x in range(grid.width):
      if (x,y) not in visited_plots:
        plots, area, _, edges = grid.explore_region((x,y))
        visited_plots |= plots
        sides = sides_from_edges(edges)
        price += area * sides
  return price

# Solution
print(part_1(string_from_file(INPUT_FILE))) # 1396562
print(part_2(string_from_file(INPUT_FILE))) # 844132

# Tests
TEST_SMALL = '''
AAAA
BBCD
BBCC
EEEC
'''
assert part_1(TEST_SMALL) == 140
assert part_2(TEST_SMALL) == 80

TEST_INPUT = '''
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
'''

assert part_1(TEST_INPUT) == 1930
assert part_2(TEST_INPUT) == 1206