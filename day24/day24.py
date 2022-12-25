from collections import deque
from math import gcd
lines = open('ex2.txt').readlines()
lines = open('input.txt').readlines()

# up, right, down, left
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

walls = set()
blizzard_pos = []
directions = []
for r, line in enumerate(lines):
    for c, symbol in enumerate(line.strip()):
        if symbol == '#':
            walls.add((r, c))
        elif symbol == '^':
            # Direction is the index in the dr,dc arrays
            blizzard_pos.append((r,c))
            directions.append(0)
        elif symbol == '>':
            blizzard_pos.append((r,c))
            directions.append(1)
        elif symbol == 'v':
            blizzard_pos.append((r,c))
            directions.append(2)
        elif symbol == '<':
            blizzard_pos.append((r,c))
            directions.append(3)

R = len(lines) - 2
C = len(lines[0].strip()) - 2
period = int(C*R / gcd(C, R))
print(R, C, period)

# Pre-calculate all the possible blizzard states
blizzards = [set(blizzard_pos)]
for t in range(1, period):
    for i, (r,c) in enumerate(blizzard_pos):
        dd = directions[i]
        r = (r + dr[dd] - 1) % R + 1
        c = (c + dc[dd] - 1) % C + 1
        blizzard_pos[i] = (r, c)
    blizzards.append(set(blizzard_pos))


def bfs(start, end, t0):
    q = deque([(start, t0)])
    visited = set()
    while q:
        p, t = q.popleft()
        if (p, t%period) in visited:
            continue
        else:
            visited.add((p, t%period))

        if p == end:
            return t

        for dd in range(4):
            new = p[0] + dr[dd], p[1] + dc[dd]
            # Only move if not a wall or not a blizzard in the next step
            if (new not in walls and new not in blizzards[(t+1)%period]
                and 0 <= new[0] <= C):
                q.append((new, t+1))
        # We can also wait, if there won't be a blizzard here
        if p not in blizzards[(t+1)%period]:
            q.append((p, t+1))

start = (0, 1)
end = (R+1, C)
assert start not in walls
assert end not in walls

p1 = bfs(start, end, 0)
print(p1)

p2 = bfs(end, start, p1)
print(p2)
p2 = bfs(start, end, p2)
print(p2)
