import os

TEST_INPUT = '2333133121414131402'
INPUT_FILE = f'{os.path.dirname(__file__)}/input'

def string_from_file(filename):
  with open(filename) as input:
    return input.read()

def debug_print(memory):
  print(''.join(str(n)[0] for n in memory))

def parse_data(string):
  file = True
  file_id = 0
  memory_index = 0
  memory = []
  free_spaces = []
  files = []
  for char in string:
    if file:
      files.append((memory_index, int(char)))
      for _ in range(int(char)):
        memory.append(file_id)
        memory_index += 1
      file_id += 1
      file = False
    else:
      free_spaces.append((memory_index, int(char)))
      for _ in range(int(char)):
        memory.append(-1)
        memory_index += 1
      file = True
  return memory, free_spaces, files

def debug_print(memory):
  print(''.join(str(n)[0] for n in memory))

def checksum(memory):
  return sum(i*file_id for i, file_id in enumerate(memory) if file_id != -1)

def part_1(string):
  memory, _, _ = parse_data(string)
  left, right = 0, len(memory) - 1
  while left <= right:
    if memory[left] == -1:
      while memory[right] == -1:
        right -= 1
      memory[left], memory[right] = memory[right], memory[left]
      right -= 1
    left += 1
  return checksum(memory)

def part_2(string):
  memory, free_spaces, files = parse_data(string)
  for file_index, file_size in reversed(files):
    for free_space_i, (space_index, space_size) in enumerate(free_spaces):
      if space_index > file_index:
        break
      if space_size >= file_size:
        for i, j in zip(range(space_index, space_index + file_size), range(file_index, file_index + file_size)):
          memory[i], memory[j] = memory[j], memory[i]
        free_spaces[free_space_i] = space_index + file_size, space_size - file_size
        break
  return checksum(memory)


# Solution
print(part_1(string_from_file(INPUT_FILE))) # 6299243228569
print(part_2(string_from_file(INPUT_FILE))) # 6326952672104

# Tests
assert part_1(TEST_INPUT) == 1928
assert part_2(TEST_INPUT) == 2858
