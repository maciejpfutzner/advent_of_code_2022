from collections import deque

grid = [[l for l in line.strip()] for line in open('input.txt')]

rr = len(grid)
cc = len(grid[0])

# find the starting position
for r in range(rr):
    for c in range(cc):
        if grid[r][c] == 'S':
            start = (r, c)
            break # Should do another but who cares

def compare(p1, p2):
    if p1 == 'S':
        p1 = 'a'
    if p2 == 'E':
        p2 = 'z'
    can_go = ord(p2) - ord(p1) <= 1
    #print(f'Comparing {p1} and {p2}: {"ok" if can_go else "not ok"}')
    return can_go

# search the grid with BFS
q = deque()
q.append(start)
visited = set()
cost = {start: 0}
while q:
    pos = q.popleft()
    pos_elev = grid[pos[0]][pos[1]]
    if pos_elev == 'E':
        end = pos # Mark the end for part 2
        print('Part 1:', cost[pos])
        break
    for i in range(4):
        dr = [1, 0, -1, 0][i]
        dc = [0, -1, 0, 1][i]
        newpos = (pos[0] + dr, pos[1] + dc)
        if (0 <= newpos[0] < rr and 0 <= newpos[1] < cc and newpos not in visited):
            newpos_elev = grid[newpos[0]][newpos[1]]
            if compare(pos_elev, newpos_elev):
                q.append(newpos)
                cost[newpos] = cost[pos]+1
                visited.add(newpos)

# part 2: walk down to an a
q = deque()
q.append(end)
visited = set()
cost = {end: 0}
while q:
    pos = q.popleft()
    pos_elev = grid[pos[0]][pos[1]]
    if pos_elev in ['S', 'a']:
        print('Part 2:', cost[pos])
        break
    for i in range(4):
        dr = [1, 0, -1, 0][i]
        dc = [0, -1, 0, 1][i]
        newpos = (pos[0] + dr, pos[1] + dc)
        if (0 <= newpos[0] < rr and 0 <= newpos[1] < cc and newpos not in visited):
            newpos_elev = grid[newpos[0]][newpos[1]]
            # Check the elevation difference in the other direction
            if compare(newpos_elev, pos_elev):
                q.append(newpos)
                cost[newpos] = cost[pos]+1
                visited.add(newpos)

