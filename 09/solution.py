import os
# from itertools import

TEST_INPUT = '2333133121414131402'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def take_two(max):
  a,b = 0,1
  while b < max:
    yield a,b
    a, b = b+1, b+2
    

def parse_data(string):
  file = True
  file_id = 0
  memory = []
  for char in string:
    if file:
      for _ in range(int(char)):
        memory.append(file_id)
      file = False
      file_id += 1
    else:
      for _ in range(int(char)):
        memory.append(-1)
      file = True
  # debug_print(memory)
  return memory

def debug_print(memory):
  print(''.join(str(n)[0] for n in memory))

def string_from_file(filename):
  with open(filename) as input:
    return input.read()

def part_1(string):
  memory = parse_data(string)
  checksum = 0
  left, right = 0, len(memory) - 1
  while left <= right:
    if memory[left] == -1:
      while memory[right] == -1:
        right -= 1
      memory[left], memory[right] = memory[right], memory[left]
      right -= 1
    checksum += memory[left] * left
    left += 1
  # debug_print(memory)
  return checksum

def part_2(string):
  pass

# Solution
print(part_1(string_from_file(INPUT_FILE))) # 
# print(part_2(string_from_file(INPUT_FILE))) # 

# Tests
assert part_1(TEST_INPUT) == 1928
# assert part_2(TEST_INPUT) ==
