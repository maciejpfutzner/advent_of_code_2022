sensors, beacons = [], []
for line in open('input.txt'):
#for line in open('ex.txt'):
    _, sx, sy, bx, by = line.strip().split('=')
    sx = int(sx.split(',')[0])
    sy = int(sy.split(':')[0])
    bx = int(bx.split(',')[0])
    by = int(by)
    sensors.append((sx, sy))
    beacons.append((bx, by))

def dist(pos1, pos2):
    return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])

closest_dists = [dist(s, b) for s,b in zip(sensors, beacons)]

def find_xranges(y):
    ranges = []
    for sensor, min_dist in zip(sensors, closest_dists):
        dy = abs(sensor[1] - y)
        dx = min_dist - dy
        if dx > 0:
            ranges.append((sensor[0] - dx, sensor[0] + dx))
    #print(ranges)

    final_ranges = []
    while ranges:
        l1, r1 = ranges.pop()
        found = False
        for i in range(len(ranges)):
            l2, r2 = ranges[i]
            if l1 <= r2 and l2 <= r1:
                new = (min(l1, l2), max(r1, r2))
                ranges[i] = new
                found = True
                break
        if not found:
            final_ranges.append((l1, r1))
    #print(final_ranges)
    return final_ranges

#y1 = 10
y1 = 2000000

final_ranges = find_xranges(y1)
range_sum = sum([r - l + 1 for l, r in final_ranges])
n_beacons = sum([1 for b in set(beacons) if b[1] == y1])
print(range_sum - n_beacons)

ymax = xmax = 4000000
for y in range(0, ymax):
    xranges = find_xranges(y)
    if len(xranges) > 1 or xranges[0][0] > 0 or xranges[0][1] < xmax:
        print(y, xranges)
        break

x = sorted(xranges)[0][1] + 1
print(x*4000000 + y)
