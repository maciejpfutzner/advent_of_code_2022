trees = []

for line in open('input.txt'):
#for line in open('ex.txt'):
    trees.append([int(t) for t in line.strip()])

def tprint(trees):
    for l in trees:
        print(l)

def visible_left(row):
    n = len(row)
    visible = [0]*n
    maxh = -1
    for i in range (n):
        if row [i] > maxh:
            maxh = row[i]
            visible[i] = 1
    return visible

def visible_rows(trees):
    visibles = []
    for i, row in enumerate(trees):
        visl = visible_left(row)
        visr = visible_left(row[::-1])[::-1]
        vis = [vl or vr for vl,vr in zip(visl, visr)]
        visibles.append(vis)
    return visibles

vis_rows = visible_rows(trees)
trees_t = list(zip(*trees))
vis_cols = list(zip(*visible_rows(trees_t)))

vis_tot = []
cc = len(trees)
rr = len(trees[0])

for r in range(cc):
    vis_tot.append([0]*cc)
    for c in range(rr):
        vis_tot[r][c] = vis_rows[r][c] or vis_cols[r][c]

#tprint(trees)

n_vis = sum([sum(r) for r in vis_tot])
print('Part 1:', n_vis)

# part 2
def scenic_score(r, c):
    height = trees[r][c]
    left = trees[r][:c:][::-1]
    right = trees[r][c+1:]
    top = trees_t[c][:r:][::-1]
    bottom = trees_t[c][r+1:]
    views = [left, right, top, bottom]

    score = 1
    for v in views:
        vscore = 0
        for t in v:
            vscore +=1
            if t >= height:
                break
        score *= vscore
    return score

max_score = 0
for r in range(rr):
    for c in range(cc):
        max_score = max(max_score, scenic_score(r, c))
print('Part 2:', max_score)
