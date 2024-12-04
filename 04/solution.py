import os

TEST_INPUT = '''
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
'''
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

class Grid:
  def __init__(self, string):
    self.grid = [line.strip() for line in string.split('\n') if line != '']
    self.height = len(self.grid)
    self.width = len(self.grid[0])

  # Virtually pad the grid with #
  def get(self, x, y):
    if x >= 0 and x < self.width and y >= 0 and y < self.height:
      return self.grid[y][x]
    return '#'

def grid_from_file(filename):
  with open(filename) as input:
    return Grid(input.read())

def gen_coords_in_direction(x,y,dx,dy,n):
  for _ in range(n):
    y = y + dy
    x = x + dx
    yield x, y

DIRS = [
  (-1,-1),(-1, 0),(-1,1),
  ( 0,-1),        (0 ,1),
  ( 1,-1),( 1, 0),(1 ,1),
]

# X is at x,y
def is_MAS_in_direction(grid, x,y, dx,dy):
  return ''.join(grid.get(xx,yy) for xx,yy in gen_coords_in_direction(x,y,dx,dy,3)) == 'MAS'

# X is at x,y, find MAS in all directions
def number_of_MASes_from_position(grid, x,y):
  return sum(1 for dx, dy in DIRS if is_MAS_in_direction(grid, x,y, dx,dy))

def part_1(grid):
  # at each X, look in all directions to see if theres a MAS
  total = 0
  for y in range(grid.height):
    for x in range(grid.width):
      if grid.get(x,y) == 'X':
        total += number_of_MASes_from_position(grid, x,y)
  return total

def part_2(grid):
  pass

# Solution
print(part_1(grid_from_file(INPUT_FILE))) # 
# print(part_2(grid_from_file(INPUT_FILE)))

# Tests
assert part_1(Grid(TEST_INPUT)) == 18
# assert part_2(Grid(TEST_INPUT)) == 

