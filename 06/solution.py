import os

TEST_INPUT = '''
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
'''
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

# dx, dy
UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)

def parse_data(string):
  grid = [line.strip() for line in string.split('\n') if line != '']
  height = len(grid)
  width = len(grid[0])
  obstacles = set()
  guard_initial_position = (0,0)
  for y in range(height):
    for x in range(width):
      if grid[y][x] == '#':
        obstacles.add((x,y))
      elif grid[y][x] == '^':
        guard_initial_position = (x,y)
  return height, width, obstacles, guard_initial_position

def inside_map(height, width, pos):
  x,y = pos
  return 0 <= x < width and 0 <= y < height

# Guard always start going up
def cycle_directions():
  while True:
    yield UP
    yield RIGHT
    yield DOWN
    yield LEFT

def walk_guard(height, width, obstacles, guard_initial_position):
  x, y = guard_initial_position
  direction_gen = cycle_directions()
  direction = next(direction_gen)
  visited = set()
  while inside_map(height, width, (x,y)):
    visited.add((x,y))
    dx, dy = direction
    if (x+dx, y+dy) in obstacles:
      direction = next(direction_gen)
      dx, dy = direction
    else:
      x,y = x+dx, y+dy
  return len(visited)

def will_guard_loop(height, width, obstacles, guard_initial_position):
  x, y = guard_initial_position
  direction_gen = cycle_directions()
  direction = next(direction_gen)
  visited = set()
  while inside_map(height, width, (x,y)):
    dx, dy = direction
    if (x,y,dx,dy) in visited:
      return True
    visited.add((x,y,dx,dy))
    if (x+dx, y+dy) in obstacles:
      direction = next(direction_gen)
      dx, dy = direction
    else:
      x,y = x+dx, y+dy
  return False

def string_from_file(filename):
  with open(filename) as input:
    return input.read()

def part_1(string):
  height, width, obstacles, guard_initial_position = parse_data(string)
  return walk_guard(height, width, obstacles, guard_initial_position)

def part_2(string):
  height, width, obstacles, guard_initial_position = parse_data(string)
  # lets brute force this !
  counter = 0
  for y in range(height):
    for x in range(width):
      if (x,y) == guard_initial_position: continue
      if will_guard_loop(height, width, obstacles|{(x,y)}, guard_initial_position):
        counter += 1
  return counter

# Solution
print(part_1(string_from_file(INPUT_FILE))) # 4982
print(part_2(string_from_file(INPUT_FILE))) # 1663

# Tests
assert part_1('#.\n^.') == 2
assert part_1(TEST_INPUT) == 41
assert part_2(TEST_INPUT) == 6

TEST_U_TURN = '''
.#....
.....#
....#.
.^....
'''
assert part_1(TEST_U_TURN) == 7
assert part_2(TEST_U_TURN) == 1 # (0,1)
