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

def process_rules(rules):
  must_follow_map = {}
  for before, after in rules:
    if before not in must_follow_map:
      must_follow_map[before] = set()
    must_follow_map[before].add(after)
  return must_follow_map

def is_ordered(must_follow_map, update):
  seen = set()
  for page in update:
    if must_follow_map.get(page, set()) & seen:
      return False
    seen.add(page)
  return True

def middle_page_number(update):
  return update[len(update) // 2]

# The notation X|Y means that if both page number X and page
# number Y are to be produced as part of an update,
# page number X must be printed at some point before page number Y.
def part_1(rules, updates):
  must_follow_map = process_rules(rules)
  return sum(middle_page_number(update) for update in updates if is_ordered(must_follow_map, update))

def comparison_function(rules):
  def compare(a, b):
    nonlocal rules
    if (a,b) in rules: return -1
    if (b,a) in rules: return 1
    print("Incomplete order!")
  return compare

def part_2(rules, updates):
  total = 0
  compare = comparison_function(rules)
  for update in updates:
    new_update = sorted(update, key=cmp_to_key(compare))
    if update != new_update:
      total += middle_page_number(new_update)
  return total


# Solution
print(part_1(*data_from_file(INPUT_FILE))) # 5268
print(part_2(*data_from_file(INPUT_FILE))) # 5799

# Tests
assert part_1(*data_from_file(TEST_FILE)) == 143
assert part_2(*data_from_file(TEST_FILE)) == 123
