ifile = open('input.txt')
#ifile = open('ex2.txt')
lines = [line.split() for line in ifile.readlines()]

visited = set()
hpos = [0, 0]
tpos = [0, 0]

dirs = dict(zip('URDL', ((1,0), (0,1), (-1,0), (0,-1))))

def update_tpos(hpos, tpos):
    if abs(hpos[0] - tpos[0]) > 1 or abs(hpos[1] - tpos[1]) > 1:
        if hpos[1] > tpos[1]:
            tpos[1] += 1
        elif hpos[1] < tpos[1]:
            tpos[1] -= 1

        if hpos[0] > tpos[0]:
            tpos[0] += 1
        elif hpos[0] < tpos[0]:
            tpos[0] -= 1
    return tpos

# part 1
for dir, n in lines:
  for i in range (int(n)):
    hpos[0] += dirs[dir][0]
    hpos[1] += dirs[dir][1]
    tpos = update_tpos(hpos, tpos)
    visited.add(tuple(tpos))
    #print(hpos, tpos)

print('Part 1:', len(visited))

# part 2
visited = set()
positions = [list(t) for t in [(0,0)]*10]

for dir, n in lines:
    for i in range (int(n)):
        hpos = positions[0]
        hpos[0] += dirs[dir][0]
        hpos[1] += dirs[dir][1]
        for j in range(1, 10):
            positions[j] = update_tpos(positions[j-1], positions[j])
        visited.add(tuple(positions[-1]))
        #print(positions)

print(len(visited))
