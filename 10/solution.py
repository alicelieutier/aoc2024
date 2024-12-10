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
    for xx, yy in (x-1, y),(x+1, y), (x, y-1), (x, y+1):
      yield (xx,yy)

  def trailheads(self):
    for y in range(self.height):
      for x in range(self.width):
        if self.grid[y][x] == 0:
          yield (x,y)

  def score(self, trailhead):
    memo = {}

    def nines_reachable(pos):
      if pos not in memo:
        altitude = self.get(pos)
        if altitude == 9:
          memo[pos] = {pos}
        else:
          results = set()
          for neighbour in self.neighbours(pos):
            if self.get(neighbour) == altitude + 1:
              results |= nines_reachable(neighbour)
          memo[pos] = results
      return memo[pos]
    reachable_nines = nines_reachable(trailhead)
    return len(reachable_nines)

def parse_input(string):
  return TopoMap(string)

def string_from_file(filename):
  with open(filename) as input:
    return input.read()
  
# a hiking trail is any path that starts at height 0, ends at height 9,
# and always increases by a height of exactly 1 at each step.
# Hiking trails never include diagonal steps.
# A trailhead's score is the number of 9-height positions
# reachable from that trailhead via a hiking trail
# What is the sum of the scores of all trailheads on your topographic map?
def part_1(string):
  topo_map = parse_input(string)
  return sum(topo_map.score(trailhead) for trailhead in topo_map.trailheads())

def part_2(string):
  pass

# Solution
print(part_1(string_from_file(INPUT_FILE))) # 
# print(part_2(string_from_file(INPUT_FILE))) # 

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

