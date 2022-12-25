board, instructions = open('input.txt').read().split('\n\n')

cbounds = []
map_ = []
for line in board.splitlines():
    minx, maxx = -1, -1
    for j, char in enumerate(line):
        if char != ' ' and minx == -1:
            minx = j
        if char in (' ', '\n') and minx != -1:
            maxx = j
    if maxx == -1:
        maxx = len(line)
    cbounds.append((minx, maxx))
    #map_.append(line[minx : maxx])
    map_.append(line.strip('\n'))

instructions = instructions.strip().replace('L', ' L ').replace('R', ' R ').split()
instructions = [int(i) if i not in ['L', 'R'] else i for i in instructions]

maxx = max([hb[1] for hb in cbounds])

rbounds = []
for i in range(maxx):
    miny, maxy = -1, -1
    for j, (l, r) in enumerate(cbounds):
        if l <= i < r and miny == -1:
            miny = j
        if (i < l or i >=r) and miny != -1:
            maxy = j
            break
    if maxy == -1:
        maxy = len(cbounds)
    rbounds.append((miny, maxy))

# up, right, down, left
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

pos = (0, cbounds[0][0])
dd = 1 # start facing right

for instr in instructions:
    if instr == 'L':
        dd = (dd - 1) %4
    elif instr == 'R':
        dd = (dd + 1) %4
    else:
        r, c = pos
        for i in range(instr):
            if dr[dd] != 0:
                r += dr[dd]
                if r < rbounds[c][0]:
                    r = rbounds[c][1] - 1
                elif r >= rbounds[c][1]:
                    r = rbounds[c][0]
            elif dc[dd] != 0:
                c += dc[dd]
                if c < cbounds[r][0]:
                    c = cbounds[r][1] - 1
                elif c >= cbounds[r][1]:
                    c = cbounds[r][0]
            if map_[r][c] == '#':
                break
            else:
                pos = r, c

print(pos, dd)
p1 = 1000 * (pos[0]+1) + 4 * (pos[1]+1) + (dd - 1)%4
print(p1)
