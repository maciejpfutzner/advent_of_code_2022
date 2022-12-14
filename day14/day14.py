#paths_txt = [l.strip() for l in open('ex.txt')]
paths_txt = [l.strip() for l in open('input.txt')]

#C = 1_000
#R = 1_000
minr, maxr, minc, maxc = 1000, -1000, 1000, -1000

paths = []
for path in paths_txt:
    pairs = [[int(n) for n in p.split(',')] for p in path.split(' -> ')]
    paths.append(pairs)
    for c,r in pairs:
        #minr = min(r, minr)
        maxr = max(r, maxr)
        minc = min(c, minc)
        maxc = max(c, maxc)

#minr = min(0, minr)
minr = 0
maxr = max(0, maxr)
minc = min(500, minc)
maxc = max(500, maxc)

#print(minr, maxr)
#print(minc, maxc)
R = maxr - minr + 1
C = maxc - minc + 1
grid = [['.' for _ in range(C)] for _ in range(R)]

def plot(grid):
    for row in grid:
        print(''.join(row))

for path in paths:
    #print(path)
    for i in range(0, len(path)-1):
        (c1, r1), (c2, r2) = path[i: i+2]
        assert c2-c1 == 0 or r2-r1 == 0
        dc = list(range( min(c1, c2), max(c1,c2)+1 ))
        dr = list(range( min(r1, r2), max(r1,r2)+1 ))
        for rr in dr:
            for cc in dc:
                grid[rr - minr][cc - minc] = '#'
        #print(dc, len(dc))
        #print(dr, len(dr))
        #print()

is_full = False
counter = 0
while not is_full:
    counter += 1
    # Make a new grain of sand at (500, 0) corrected for the grid
    sc, sr = 500 - minc, 0 - minr
    while True:
        # Check if we're in bounds
        if not (0 <= sc < C and 0 <= sr < R-1):
            # If not - or we're on the bottom row - this is the end state
            is_full = True
            print('Out of bounds, end of the game')
            break

        # Try to fall down
        if grid[sr+1][sc] == '.':
            sr += 1
        # Try to fall left diagonal
        elif grid[sr+1][sc-1] == '.':
            sr += 1
            sc -= 1
        # Try to fall right diagonal
        elif grid[sr+1][sc+1] == '.':
            sr += 1
            sc += 1
        # If all is blocked
        else:
            # Settle here
            grid[sr][sc] = 'o'
            #plot(grid)
            break

plot(grid)
print(counter-1)

# part 2
minc -= 500
maxc += 500
maxr += 2

R = maxr - minr + 1
C = maxc - minc + 1
grid = [['.' for _ in range(C)] for _ in range(R)]

for path in paths:
    #print(path)
    for i in range(0, len(path)-1):
        (c1, r1), (c2, r2) = path[i: i+2]
        assert c2-c1 == 0 or r2-r1 == 0
        dc = list(range( min(c1, c2), max(c1,c2)+1 ))
        dr = list(range( min(r1, r2), max(r1,r2)+1 ))
        for rr in dr:
            for cc in dc:
                grid[rr - minr][cc - minc] = '#'
        #print(dc, len(dc))
        #print(dr, len(dr))
        #print()
grid[-1] = ['#'] * C

startc, startr = 500 - minc, 0 - minr

is_full = False
counter = 0
while grid[startr][startc] != 'o':
    counter += 1
    # Make a new grain of sand at (500, 0) corrected for the grid
    sc, sr = startc, startr
    while True:
        # Assert we're in bounds
        assert 0 <= sc < C

        # Try to fall down
        if grid[sr+1][sc] == '.':
            sr += 1
        # Try to fall left diagonal
        elif grid[sr+1][sc-1] == '.':
            sr += 1
            sc -= 1
        # Try to fall right diagonal
        elif grid[sr+1][sc+1] == '.':
            sr += 1
            sc += 1
        # If all is blocked
        else:
            # Settle here
            grid[sr][sc] = 'o'
            #plot(grid)
            break

#plot(grid)
print(counter)
