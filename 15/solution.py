import os

INPUT_FILE = f'{os.path.dirname(__file__)}/input'
TEST_FILE = f'{os.path.dirname(__file__)}/test_input'

def parse_warehouse(block):
  lines = block.split('\n')
  robot = None
  walls = set()
  boxes = set()
  for y, line in enumerate(lines):
    for x, char in enumerate(line):
      if char == '@':
        robot = (x,y)
      elif char == '#':
        walls.add((x,y))
      elif char == 'O':
        boxes.add((x,y))
  if not robot:
    print('ROBOT NOT FOUND!')
  return robot, walls, boxes

def parse_data(string):
  warehouse, movements = string.split('\n\n')
  return parse_warehouse(warehouse), ''.join(movements.split('\n'))

def string_from_file(filename):
  with open(filename) as input:
    return input.read()
  
def direction_from_move(move):
  match move:
    case '<': return (-1,0)
    case 'v': return (0,1)
    case '>': return (1,0)
    case '^': return (0,-1)
    case _ : print("Unknown move!")

def debug_print(robot, walls, boxes, size=50):
  for y in range(size):
    line = []
    for x in range(size):
      if (x,y) == robot:
        line.append('@')
      elif (x,y) in walls:
        line.append('#')
      elif (x,y) in boxes:
        line.append('O')
      else:
        line.append('.')
    print(''.join(line))

def move_box(pos, direction, walls, boxes, initial_box=None):
  if initial_box is None:
    initial_box = pos
  (x,y), (dx,dy) = pos, direction
  next_pos = (x+dx, y+dy)
  if next_pos in walls:
    return boxes
  if next_pos not in boxes:
    return (boxes - {initial_box}) | {next_pos}
  return move_box(next_pos, direction, walls, boxes, initial_box)

def move_if_possible(warehouse, move):
  dx, dy = direction_from_move(move)
  (x,y), walls, boxes = warehouse
  next_pos = (x+dx, y+dy)
  if next_pos in boxes:
    boxes = move_box(next_pos, (dx,dy), walls, boxes)
  if next_pos not in walls and next_pos not in boxes:
    return next_pos, walls, boxes
  return (x,y), walls, boxes

def part_1(string):
  warehouse, movements = parse_data(string)
  for move in movements:
    warehouse = move_if_possible(warehouse, move)
  _,_, boxes = warehouse
  return sum(100*y+x for x,y in boxes)
  

def part_2(string):
  pass

# Solution
print(part_1(string_from_file(INPUT_FILE))) # 
# print(part_2(string_from_file(INPUT_FILE))) # 

# Tests
SMALL_TEST = '''
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
'''
# part_1(SMALL_TEST)

assert part_1(string_from_file(TEST_FILE)) == 10092
# assert part_2(TEST_INPUT) ==


