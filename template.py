import os

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse_line(line):
  a, b = line.split()
  return int(a), int(b)

def gen_lines_from_string(string):
  return (line.strip() for line in string.split('\n') if line != '')

def gen_lines(filename):
  with open(filename) as input:
    return (line.strip() for line in input.readlines())

def part_1(filename):
  # data = [parse_line(line) for line in gen_lines(filename)]
  # return
  pass

def part_2(filename):
  pass

# Solution
print(part_1(INPUT_FILE))
# print(part_2(INPUT_FILE))

# Tests
assert part_1(TEST_FILE) == -1
# assert part_2(TEST_FILE) == -1
