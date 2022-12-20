from collections import deque

pixels = set(tuple(int(n) for n in line.strip().split(',')) for line in open('input.txt'))
#print(pixels)

coords = [[p[i] for p in pixels] for i in range(3)]
mins = tuple(min(coords[i])-1 for i in range(3))
maxs = tuple(max(coords[i])+1 for i in range(3))
print(mins, maxs)

outside = set()
q = deque((mins,))
while q:
    p = q.popleft()
    if p in outside:
        continue

    outside.add(p)
    for sgn in [1, -1]:
        for d in [(1,0,0), (0,1,0), (0,0,1)]:
            new = (p[0] + sgn*d[0],
                   p[1] + sgn*d[1],
                   p[2] + sgn*d[2],
                   )
            if (mins[0] <= new[0] <= maxs[0] and
                mins[1] <= new[1] <= maxs[1] and
                mins[2] <= new[2] <= maxs[2] and
                new not in pixels
                ):
                q.append(new)

#print(len(outside))

p1 = p2 = 0
for pixel in pixels:
    for sgn in [1, -1]:
        for d in [(1,0,0), (0,1,0), (0,0,1)]:
            new = (pixel[0] + sgn*d[0],
                   pixel[1] + sgn*d[1],
                   pixel[2] + sgn*d[2],
                   )
            if new not in pixels:
                p1 += 1
            if new in outside:
                p2 += 1

print(p1)
print(p2)

