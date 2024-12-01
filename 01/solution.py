import os
from collections import Counter

TEST_FILE = '''
3   4
4   3
2   5
1   3
3   9
3   3
'''

INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse_line(line):
  a, b = line.split()
  return int(a), int(b)

def lines(filename_or_string, file=True):
  if not file:
    return (line.strip() for line in filename_or_string.split('\n') if line != '')
  with open(filename_or_string) as input:
    return (line.strip() for line in input.readlines())

def part_1(lines):
  list1, list2 = zip(*[parse_line(line) for line in lines])
  return sum(abs(a - b) for a, b in zip(sorted(list1), sorted(list2)))

def part_2(lines):
  list1, list2 = zip(*[parse_line(line) for line in lines])
  counter = Counter(list2)
  return sum(n * counter[n] for n in list1)

# Solution
print(part_1(lines(INPUT_FILE))) # 1765812
print(part_2(lines(INPUT_FILE))) # 20520794

# Tests
assert part_1(lines(TEST_FILE, False)) == 11
assert part_2(lines(TEST_FILE, False)) == 31
