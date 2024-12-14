import os
import re
from collections import Counter
from PIL import Image

INPUT_FILE = f'{os.path.dirname(__file__)}/input'

LINE_PATTERN = re.compile(r'p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)')
def parse_line(line):
  match = LINE_PATTERN.search(line)
  px, py, vx, vy = [int(n) for n in match.groups()]
  return (px,py),(vx,vy)

def parse_data(string):
  return [parse_line(line) for line in string.split('\n') if line != '']

def string_from_file(filename):
  with open(filename) as input:
    return input.read()
  
def move(robots, width, height):
  new_robots = []
  for (x,y), (dx,dy) in robots:
    new_x = (2*width + x + dx) % width
    new_y = (2*height + y + dy) % height
    new_robots.append(((new_x, new_y),(dx,dy)))
  return new_robots

def create_image(robots, width, height, n):
  img = Image.new('RGB', (width,height), "black")
  for (x,y), _ in robots:
    img.putpixel((x,y), (255,255,255))
  img.save(f'{os.path.dirname(__file__)}/{n}.jpg')

def safety_factor(robots, width , height):
  q1,q2,q3,q4 = 0,0,0,0
  for (x,y), _ in robots:
    if x < width // 2 and y < height // 2:
      q1 += 1
    if x > width // 2 and y < height // 2:
      q2 += 1
    if x < width // 2 and y > height // 2:
      q3 += 1
    if x > width // 2 and y > height // 2:
      q4 += 1
  return q1*q2*q3*q4

def part_1(string, width =101, height=103):
  robots = parse_data(string)
  for _ in range(100):
    robots = move(robots, width, height)
  return safety_factor(robots, width , height)

def part_2(string, width =101, height=103):
  robots = parse_data(string)
  tick = 0
  # stop when no robot overlap
  while True:
    robots = move(robots, width, height)
    tick += 1
    if len(set([pos for pos, _ in robots])) == len(robots):
      create_image(robots, width, height, tick)
      return tick

# Solution
print(part_1(string_from_file(INPUT_FILE))) # 
print(part_2(string_from_file(INPUT_FILE))) # 

# Tests
TEST_INPUT = '''
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
'''

assert part_1(TEST_INPUT, width=11, height=7) == 12
