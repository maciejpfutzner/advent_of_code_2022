import re

def load_stacks(fname='stacks.txt'):
    stacks_txt = open(fname).readlines()[::-1]
    n_stacks = max([int(n.strip()) for n in stacks_txt[0].split('   ')])

    #print(n_stacks)
    stacks = {}
    for i in range(n_stacks):
        stacks[i+1] = []
        for j in range(1, len(stacks_txt)):
            col = i*4 + 1
            crate = stacks_txt[j][col]
            if crate != ' ':
                stacks[i+1].append(crate)
    return stacks

def print_top_crate(stacks):
    # Order is preserved in python dictionaries now
    print(''.join([s[-1] for n,s in stacks.items()]))

# part 1
stacks = load_stacks()
print(stacks)
print()
for instruction in open('instructions.txt'):
    _, num, _, start, _, dest = instruction.split(' ') 
    num, start, dest = map(lambda x: int(x), [num, start, dest])
    for i in range(num):
        crate = stacks[start].pop()
        stacks[dest].append(crate)

print_top_crate(stacks)

# part 2
stacks = load_stacks()
for instruction in open('instructions.txt'):
    _, num, _, start, _, dest = instruction.split(' ') 
    num, start, dest = map(lambda x: int(x), [num, start, dest])
    crates = stacks[start][-num:]
    stacks[start] = stacks[start][:-num]
    stacks[dest].extend(crates)

print_top_crate(stacks)
