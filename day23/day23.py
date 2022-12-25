from collections import deque, Counter
from itertools import count

elves = set()
lines = open('input.txt').readlines()
#lines = open('ex2.txt').readlines()
max_y = len(lines) - 1

for neg_y, line in enumerate(lines):
    for x, char in enumerate(line.strip()):
        if char == '#':
            elves.add((x, max_y - neg_y))

def get_bounds(elves):
    xs = [e[0] for e in elves]
    ys = [e[1] for e in elves]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    return minx, miny, maxx, maxy

def plot(elves):
    minx, miny, maxx, maxy = get_bounds(elves)
    for y in range(maxy, miny-1, -1):
        line = ['#' if (x,y) in elves else '.'  for x in range(minx, maxx+1)]
        print(''.join(line))

#plot(elves)
directions = deque(( (0, 1), (0, -1), (-1, 0), (1, 0) ))

for i in count(1, 1):
    #print(f'\nRound {i}')

    # Find proposals
    proposed = {}
    for x, y in elves:
        #print(x, y)
        # Check if there are any elves around us
        neighbour = False
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if not (dx == 0 and dy == 0) and (x+dx, y+dy) in elves:
                    neighbour = True
        # If there's no one around us, we don't have to move at all
        if not neighbour:
            #print('No one around us, stay put')
            continue

        # If we do move, let's consider directions in order
        for dx, dy in directions:
            if dx == 0:
                # We're going north or south, check west and east of it
                if all((x+dx, y+dy) not in elves for dx in [-1, 0, 1]):
                    #print("No one North/South, we're going there")
                    proposed[(x,y)] = (x+dx, y+dy)
                    break
            else:
                # We're going east or west, check north and south of it
                if all((x+dx, y+dy) not in elves for dy in [-1, 0, 1]):
                    proposed[(x,y)] = (x+dx, y+dy)
                    #print("No one East/West, we're going there")
                    break
        #if (x,y) in proposed:
        #    print(f'Going to {proposed[(x,y)]}')
        #else:
        #    print(f"We're staying at {x,y}")

    if not proposed:
        print(f'No one has to move in round {i}')
        break
    proposed_counts = Counter(proposed.values())

    # Execute moves
    new_elves = set()
    for old in elves:
        if old in proposed:
            # If more elves wanted to move there, stay put
            if proposed_counts[proposed[old]] > 1:
                new_elves.add(old)
            # If we were the only one, let's go
            else:
                new_elves.add(proposed[old])
        # If we didn't have to move, stay
        else:
            new_elves.add(old)
    elves = new_elves

    # Rotate the preferred direction
    directions.rotate(-1)
    #plot(elves)

minx, miny, maxx, maxy = get_bounds(elves)
n_fields = (maxy - miny + 1) * (maxx - minx + 1)
n_elves = len(elves)
print(f'{n_fields - n_elves} empty fields')
