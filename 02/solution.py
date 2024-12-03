import os
from itertools import pairwise

TEST_INPUT = '''
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
'''

INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse_line(line):
  return [int(n) for n in line.split()]  

def lines(string):
  return (line.strip() for line in string.split('\n') if line != '')
  
def lines_from_file(filename):
  with open(filename) as input:
    return (line.strip() for line in input.readlines())
  
def within_interval(low, high, number):
  return number >= low and number <= high

# The levels are either all increasing or all decreasing.
# Any two adjacent levels differ by at least one and at most three
def is_safe(report):
  differences = [a - b for a, b in pairwise(report)]
  return (all([within_interval(-3, -1, difference) for difference in differences])
       or all([within_interval(1, 3, difference) for difference in differences]))

def part_1(lines):
  reports = [parse_line(line) for line in lines]
  safe_reports = [report for report in reports if is_safe(report)]
  return len(safe_reports)

def iter_skip_n(collection, n):
  for i, item in enumerate(collection):
    if i != n:
      yield item

# Now, the same rules apply as before, except if removing a single level
# from an unsafe report would make it safe, the report instead counts as safe.

# Definitely not the most efficient solution, but for sure the fastest to write
def is_safe_with_dampener(report):
  return any(is_safe(iter_skip_n(report, n)) for n in range(len(report)))

def part_2(lines):
  reports = [parse_line(line) for line in lines]
  safe_reports = [report for report in reports if is_safe_with_dampener(report)]
  return len(safe_reports)

# Solution
print(part_1(lines_from_file(INPUT_FILE))) # 299
print(part_2(lines_from_file(INPUT_FILE))) # 364

# Tests
assert part_1(lines(TEST_INPUT)) == 2
assert part_2(lines(TEST_INPUT)) == 4

