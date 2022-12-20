from collections import deque

directions = open('input.txt').read().strip()
#directions = open('ex.txt').read().strip()

class Shape:
    types = [
            {(0, 0), (1, 0), (2, 0), (3, 0)}, # -
            {(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)}, # +
            {(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)}, # inverted L
            {(0, 0), (0, 1), (0, 2), (0, 3)}, # |
            {(0, 0), (0, 1), (1, 0), (1, 1)}, # square
            ]

    def __init__(self, type_n, ypos):
        shape = Shape.types[type_n % 5]
        self.shape = {(x + 2, y + ypos) for x,y in shape}
        #print(self.shape)

    def move(self, tower, direction):
        """Move the shape, return new tower if settled, otherwise None"""
        # first try to move to the side
        dx = 1 if direction == '>' else -1
        new = {(x + dx, y) for x, y in self.shape}
        # only update position if there won't be a collision
        if not (min((p[0] for p in new)) < 0 or
                max((p[0] for p in new)) >= 7 or
                (new & tower)):
            self.shape = new

        # try to move down
        new = {(x, y-1) for x, y in self.shape}
        if not (new & tower):
            self.shape = new
            return None
        else:
            tower = tower | self.shape
            return tower

def plot(tower, shape=None):
    if shape is None:
        shape = set()
    else:
        shape = shape.shape
    max_y = max(p[1] for p in tower | shape)
    #min_y = min(p[1] for p in tower | shape) -1
    for y in range(max_y, -1, -1):
        pixels = []
        for x in range(7):
            if (x,y) in tower:
                pixels.append('#')
            elif (x,y) in shape:
                pixels.append('@')
            else:
                pixels.append('.')
        print('|' + ''.join(pixels) + '|')
    print('---------')

def reduce_tower(tower):
    # flood-fill empty spaces from the top
    outside = set()
    border = set()
    q = deque()
    max_y = max(p[1] for p in tower)
    q.append((0, max_y+2))
    while q:
        p = q.popleft()
        if p in outside:
            continue

        outside.add(p)
        for i in range(4):
            dx = [-1, 0, 1, 0][i]
            dy = [0, -1, 0, 1][i]
            new = (p[0] + dx, p[1] + dy)
            if new in tower:
                border.add(new)
            elif (0 <= new[0] < 7 and 0 < new[1] <= max_y+2):
                q.append(new)

    min_y = min(p[1] for p in border)
    border = set((p[0], p[1] - min_y) for p in border)
    return border, min_y


def run_sim(tower, max_rocks, reduce_every=20, step=0, n_rocks=0, reps=None):
    reduced_towers = set()
    max_y = max(p[1] for p in tower)
    min_y = 0
    s = Shape(n_rocks, max_y+4)
    n_rocks += 1

    while n_rocks <= max_rocks:
        direction = directions[step % len(directions)]
        result = s.move(tower, direction)
        if result is not None:
            # If the rock just settled down, start another one
            tower = result
            if n_rocks % reduce_every == 0:
                tower, y = reduce_tower(tower)
                min_y += y
                if reps is not None:
                    if (tuple(tower), step % len(directions)) in reduced_towers:
                        print(f'Found a repetition at step {step}, rock {n_rocks}')
                        reps.append((n_rocks, step % len(directions), min_y))
                        reduced_towers = set()
                        if len(reps) == 2:
                            return min_y, tower
                    reduced_towers.add(( tuple(tower), step % len(directions) ))

            max_y = max(p[1] for p in tower)
            s = Shape(n_rocks, max_y +4)
            n_rocks += 1
        step +=1
    return min_y, tower

# Initial tower is just the floor
tower = {(i, 0) for i in range(7)}

# part 1
min_y, tower = run_sim(tower, 2022)
max_y = max(p[1] for p in tower)
print(min_y + max_y)

# part 2
# What are we trying to do?
# 1) Run for as long as it takes to find a repeated state of (tower, instruction)
# 2) Note down the rock number and the instruction step
# 3) Run again until a repetition - this is the easiest way to get the period
# 4) Calculate the period in rocks and the corresponding height
# 5) How many more times do we have to repeat the cycle to get to million millions?
# 6) Add the cycle height times full cycles -1 to the current height
# 7) Set the current rock number and instruction step to the end of last cycle
# 8) Run the simulation until we reach the actual million million rocks

# Initial tower is just the floor
tower = {(i, 0) for i in range(7)}

reps = []
min_y, tower = run_sim(tower, 5*len(directions), reduce_every=5, reps=reps)
n1, s1, y1 = reps[0]
n2, s2, y2 = reps[1]
period = n2 - n1
height = y2 - y1
big_number = 1_000_000_000_000
rocks_needed = big_number - n2

n_cycles = rocks_needed // period #-1
n_extra_rocks = rocks_needed % period #+ period
base_y = min_y + n_cycles * (y2 - y1)

# Need to start with last step +1
min_y, tower = run_sim(tower, n_extra_rocks, step=s2+1)
max_y = max(p[1] for p in tower)

print(base_y + min_y + max_y)

