import os
from functools import cmp_to_key

TEST_FILE = f'{os.path.dirname(__file__)}/test_input'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def parse_rule(rule_line):
  a,b = rule_line.split('|')
  return int(a), int(b)

def parse_update(update_line):
  return [int(update) for update in update_line.split(',')]

def data_from_file(filename):
  with open(filename) as input:
    rules, updates = input.read().split('\n\n')
    rules = {parse_rule(line) for line in rules.split('\n') if line != ''}
    updates = (parse_update(line) for line in updates.split('\n') if line != '')
    return rules, updates

def middle_page_number(update):
  return update[len(update) // 2]

def is_ordered_function(rules):
  must_follow_map = {}
  for before, after in rules:
    if before not in must_follow_map:
      must_follow_map[before] = set()
    must_follow_map[before].add(after)

  def is_ordered(update):
    seen = set()
    for page in update:
      if must_follow_map.get(page, set()) & seen:
        return False
      seen.add(page)
    return True
  return is_ordered


def sorted_function(rules):
  def compare(a, b):
    # nonlocal rules
    if (a,b) in rules: return -1
    if (b,a) in rules: return 1
    print("Incomplete order!")

  def custom_sorted(update):
    return sorted(update, key=cmp_to_key(compare))
  
  return custom_sorted


# The notation X|Y means that if both page number X and page
# number Y are to be produced as part of an update,
# page number X must be printed at some point before page number Y.
def part_1(rules, updates):
  is_ordered = is_ordered_function(rules)
  return sum(middle_page_number(update) for update in updates if is_ordered(update))

def comparison_function(rules):
  def compare(a, b):
    nonlocal rules
    if (a,b) in rules: return -1
    if (b,a) in rules: return 1
    print("Incomplete order!")
  return compare

def part_2(rules, updates):
  custom_sorted = sorted_function(rules)
  total = 0
  for update in updates:
    new_update = custom_sorted(update)
    if update != new_update:
      total += middle_page_number(new_update)
  return total


# Solution
print(part_1(*data_from_file(INPUT_FILE))) # 5268
print(part_2(*data_from_file(INPUT_FILE))) # 5799

# Tests
assert part_1(*data_from_file(TEST_FILE)) == 143
assert part_2(*data_from_file(TEST_FILE)) == 123
