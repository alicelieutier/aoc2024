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

# dx, dy
UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)

def next_direction(prev_direction):
  if prev_direction == UP: return RIGHT
  if prev_direction == RIGHT: return DOWN
  if prev_direction == DOWN: return LEFT
  return UP

def guard_walker(obstacles):
  def next_state(guard_position, guard_direction):
    x, y = guard_position
    dx, dy = guard_direction
    if (x+dx, y+dy) in obstacles:
      return guard_position, next_direction(guard_direction)
    return (x+dx, y+dy), guard_direction
  return next_state

def walk_guard(height, width, obstacles, guard_position, guard_direction=UP):
  visited = set()
  next_state = guard_walker(obstacles)
  while inside_map(height, width, guard_position):
    visited.add(guard_position)
    guard_position, guard_direction = next_state(guard_position, guard_direction)
  return visited

def will_guard_loop(height, width, obstacles, guard_position, guard_direction=UP):
  visited = set()
  next_state = guard_walker(obstacles)
  while inside_map(height, width, guard_position):
    if (guard_position, guard_direction) in visited:
      return True
    visited.add((guard_position, guard_direction))
    guard_position, guard_direction = next_state(guard_position, guard_direction)
  return False

def string_from_file(filename):
  with open(filename) as input:
    return input.read()

def part_1(string):
  height, width, obstacles, guard_initial_position = parse_data(string)
  return len(walk_guard(height, width, obstacles, guard_initial_position))

def part_2(string):
  height, width, obstacles, guard_initial_position = parse_data(string)
  possible_obstacle_locations = walk_guard(height, width, obstacles, guard_initial_position)
  counter = 0
  for x,y in possible_obstacle_locations - {guard_initial_position}:
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
