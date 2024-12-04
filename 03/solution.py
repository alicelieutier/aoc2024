import os
import re

TEST_INPUT_PART_1 = 'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))'
TEST_INPUT_PART_2 = '''xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))'''
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def content(filename):
  with open(filename) as input:
    return input.read()

MUL_PATTERN = re.compile(r'mul\((\d{1,3}),(\d{1,3})\)')
def find_and_process_multiplications(string):
  matches = re.findall(MUL_PATTERN, string)
  return sum(int(a) * int(b) for a, b in matches)

def part_1(input):
  return find_and_process_multiplications(input)

# The do() instruction enables future mul instructions.
# The don't() instruction disables future mul instructions.
# /!\  . does not match \n
DO_PATTERN = re.compile(r'do\(\)((.|\n)*?)don\'t\(\)')
def part_2(input):
  # bookend the string with do() and dont()
  input = f'''do(){input}don't()'''
  # find all areas within do and dont
  dos = re.finditer(DO_PATTERN, input)
  # process each one and add them together
  return sum(find_and_process_multiplications(do.groups()[0]) for do in dos)

# Solution
print(part_1(content(INPUT_FILE))) # 170807108
print(part_2(content(INPUT_FILE))) # 74838033

# Tests
assert part_1(TEST_INPUT_PART_1) == 161
assert part_2(TEST_INPUT_PART_2) == 48


assert part_2('''mul(1,2)do()mul(1,3)don't()do()mul(1,5)don't()mul(1,7)''') == 10
assert part_2('''mul(1,2)mul(1,7)''') == 9

multiline_testcase = '''
mul(1,2)
mul(1,2)don't()mul(1,7)
do()
mul(1,34)
do()mul(1,13)don't()
mul(1,11)
'''
assert part_2(multiline_testcase) == 2+2+34+13