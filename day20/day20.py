numbers = [int(n.strip()) for n in open('input.txt')]
numbers2 = [n* 811589153 for n in numbers]

def print_list(numbers, positions):
    slist = sorted(zip(numbers, positions), key=lambda x: x[1])
    print(', '.join([str(n[0]) for n in slist]))


def mix_numbers(numbers, positions):
    nn = len(numbers)
    for i, n in enumerate(numbers):
        if n == 0:
            zero_idx = i
            continue
    
        old_pos = positions[i]
        new_pos = (old_pos + n) % (nn-1)
        if new_pos == 0:
            new_pos = nn-1
            
        # update positions between old and new
        if new_pos - old_pos > 0:
            to_update = set(range(old_pos+1, new_pos+1))
            positions = [p - 1 if p in to_update else p for p in positions]
        else:
            to_update = set(range(old_pos-1, new_pos-1, -1))
            positions = [p + 1 if p in to_update else p for p in positions]

        # Update the position of the number itself
        positions[i] = new_pos
    return numbers, positions, zero_idx

def find_coordinates(numbers, positions, zero_idx):
    zero_pos = positions[zero_idx]
    nn = len(numbers)
    ans = 0
    check_positions = {(1000 + zero_pos) % nn, (2000 + zero_pos) % nn, (3000 + zero_pos) % nn}
    for i, pos in enumerate(positions):
        if pos in check_positions:
            #print(f'In position {pos} is number {numbers[i]}')
            ans += numbers[i]
    return ans


# part 1
positions = list(range(len(numbers)))
#print_list(numbers, positions)
numbers, positions, zero_idx = mix_numbers(numbers, positions)
print(find_coordinates(numbers, positions, zero_idx))

# part 2
positions = list(range(len(numbers)))
for _ in range(10):
    numbers2, positions, zero_idx = mix_numbers(numbers2, positions)
print(find_coordinates(numbers2, positions, zero_idx))
