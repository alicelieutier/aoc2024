import os
import re

INPUT_FILE = f'{os.path.dirname(__file__)}/input'

BLOCK_PATTERN = re.compile(r'Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)')
def parse_block(block):
  match = BLOCK_PATTERN.search(block)
  ax, ay, bx, by, px, py = [int(n) for n in match.groups()]
  return (ax,ay),(bx,by),(px,py)

def parse_data(string):
  return (parse_block(block.strip()) for block in string.split('\n\n'))

def string_from_file(filename):
  with open(filename) as input:
    return input.read()

# it costs 3 tokens to push the A button and 1 token to push the B button
# find m,n so that m*ax + n*bx == px and m*ay + n*by == py
# while minimizing 3m + n
def minimum_tokens(machine):
  (ax,ay),(bx,by),(px,py) = machine
  possible_prices = []
  for m in range(101):
    for n in range(101):
      if m*ax + n*bx == px and m*ay + n*by == py:
        possible_prices.append(3*m+n)
  if len(possible_prices) > 0:
    return min(possible_prices)
  return 0

# find m,n so that m*ax + n*bx == px and m*ay + n*by == py
# base change of a vector system
# none of the vectors given are colinear
def minimum_tokens_2(machine):
  (ax,ay),(bx,by),(px,py) = machine
  px, py = px + 10000000000000, py + 10000000000000
  # invert the matrix https://www.youtube.com/watch?v=kWorj5BBy9k
  d = ax*by-ay*bx # matrix determinant
  m = (px*by-py*bx)//d
  n = (py*ax-px*ay)//d
  if m*ax + n*bx == px and m*ay + n*by == py:
    return 3*m+n
  return 0

# You estimate that each button would need to be
# pressed no more than 100 times to win a prize.
def part_1(string):
  machines = parse_data(string)
  return sum(minimum_tokens(machine) for machine in machines)

def part_2(string):
  machines = parse_data(string)
  return sum(minimum_tokens_2(machine) for machine in machines)

# Solution
print(part_1(string_from_file(INPUT_FILE))) # 31761
print(part_2(string_from_file(INPUT_FILE))) # 90798500745591

# Tests
TEST_INPUT = '''
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
'''

# assert part_1(TEST_INPUT) == 480
# assert part_2(TEST_INPUT) == 4
