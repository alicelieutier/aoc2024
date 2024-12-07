import os
from functools import cache

TEST_INPUT = '''
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
'''
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse_line(line):
  value, numbers_string = line.split(': ')
  numbers = numbers_string.split(' ')
  return int(value), tuple(int(n) for n in numbers)

def parse_data(string):
  return [parse_line(line.strip()) for line in string.split('\n') if line != '']

def string_from_file(filename):
  with open(filename) as input:
    return input.read()

def is_possible(value, numbers):
  match numbers:
    case []: return False
    case [last]: return value == last
    case [*left, last]:
      if value % last != 0:
        return is_possible(value - last, left)
      return is_possible(value - last, left) or is_possible(value // last, left)

def ends_with(value, number):
  return value > number and str(value).endswith(str(number))

def remove_suffix(value, suffix_number):
  if ends_with(value, suffix_number):
    return int(str(value)[:-len(str(suffix_number))])
  raise Exception('Tried to remove an invalid suffix')

def is_possible_with_concat(value, numbers):
  match numbers:
    case []: return False
    case [last]: return value == last
    case [*left, last]:
      branches = []
      if value % last == 0:
        branches.append(is_possible_with_concat(value // last, left))
      if ends_with(value, last):
        branches.append(is_possible_with_concat(remove_suffix(value, last), left))
      if value > last:
        branches.append(is_possible_with_concat(value - last, left))
      return any(branches)

def part_1(string):
  equations = parse_data(string)
  return sum(value for value, numbers in equations if is_possible(value, numbers))

def part_2(string):
  equations = parse_data(string)
  return sum(value for value, numbers in equations if is_possible_with_concat(value, numbers))

# Solution
print(part_1(string_from_file(INPUT_FILE)))
print(part_2(string_from_file(INPUT_FILE)))

# Tests
assert is_possible(2, (1,1)) == True
assert is_possible(3, (1,1)) == False
assert is_possible(15, (5,3)) == True
assert is_possible(3267, (81,40,27)) == True
assert is_possible(15666, (15,6,6,6)) == False

assert is_possible_with_concat(2, (1,1)) == True
assert is_possible_with_concat(3, (1,1)) == False
assert is_possible_with_concat(15, (5,3)) == True
assert is_possible_with_concat(3267, (81,40,27)) == True
assert is_possible_with_concat(15666, (15,6,6,6)) == True
assert is_possible_with_concat(7290, (6,8,6,15)) == True
assert is_possible_with_concat(36, (1,2,3)) == True
assert is_possible_with_concat(103, (5,2,3)) == True
assert part_1(TEST_INPUT) == 3749
assert part_2(TEST_INPUT) == 11387
