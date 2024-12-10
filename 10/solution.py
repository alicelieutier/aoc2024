import os

INPUT_FILE = f'{os.path.dirname(__file__)}/input'

class TopoMap:
  def __init__(self, string):
    self.grid = [[int(n) for n in line] for line in string.split('\n') if line != '']
    self.height = len(self.grid)
    self.width = len(self.grid[0])

  # Virtually pad the grid with -1
  def get(self, pos):
    x, y = pos
    if 0 <= x < self.width and 0 <= y < self.height:
      return self.grid[y][x]
    return -1

  def neighbours(self, pos):
    x,y = pos
    yield (x-1, y)
    yield (x+1, y)
    yield (x, y-1)
    yield (x, y+1)

  def trailheads(self):
    for y in range(self.height):
      for x in range(self.width):
        if self.get((x,y)) == 0:
          yield (x,y)

  def score(self, trailhead):
    def nines_reachable(pos):
      altitude = self.get(pos)
      if altitude == 9:
        return {pos}
      results = set()
      for neighbour in self.neighbours(pos):
        if self.get(neighbour) == altitude + 1:
          results |= nines_reachable(neighbour)
      return results
    
    return len(nines_reachable(trailhead))
  
  def rating(self, pos):
    altitude = self.get(pos)
    if altitude == 9:
      return 1
    return sum(self.rating(neighbour) for neighbour in self.neighbours(pos) if self.get(neighbour) == altitude + 1)

def string_from_file(filename):
  with open(filename) as input:
    return input.read()

def part_1(string):
  topo_map = TopoMap(string)
  return sum(topo_map.score(trailhead) for trailhead in topo_map.trailheads())

def part_2(string):
  topo_map = TopoMap(string)
  return sum(topo_map.rating(trailhead) for trailhead in topo_map.trailheads())

# Solution
print(part_1(string_from_file(INPUT_FILE))) # 794
print(part_2(string_from_file(INPUT_FILE))) # 1706

# Tests
TEST_1 = '''
0123
1234
8765
9876
'''

TEST_2 = '''
2290229
2221298
2222227
6543456
7652987
8762222
9872222
'''

TEST_INPUT = '''
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
'''

assert TopoMap(TEST_1).score((0,0)) == 1
assert TopoMap(TEST_2).score((3,0)) == 4

assert part_1(TEST_INPUT) == 36
assert part_2(TEST_INPUT) == 81  # 20, 24, 10, 4, 1, 4, 5, 8, and 5
