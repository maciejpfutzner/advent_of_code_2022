from functools import cmp_to_key

pairs = [p.splitlines() for p in open('input.txt').read().split('\n\n')]
pairs = [[eval(l) for l in p] for p in pairs]

def compare(l1, l2):
    for v1, v2 in zip(l1,l2):
        if isinstance(v1, int) and isinstance(v2, int):
            if v1 < v2:
                return True
            elif v1 > v2:
                return False
        elif isinstance(v1, int) and isinstance(v2, list):
            comp = compare([v1], v2)
            if comp is not None:
                return comp
        elif isinstance(v1, list) and isinstance(v2, int):
            comp = compare(v1, [v2])
            if comp is not None:
                return comp
        elif isinstance(v1, list) and isinstance(v2, list):
            comp = compare(v1, v2)
            if comp is not None:
                return comp

    if len(l1) < len(l2):
        return True
    elif len(l1) > len(l2):
        return False
    else:
        return None

p1 = 0
for i, (l1, l2) in enumerate(pairs):
    if compare(l1, l2):
        p1 += i+1
print(p1)


packets = [eval(p.strip()) for p in open('input.txt').readlines() if p != '\n']
packets.extend([ [[2]], [[6]] ])

def cmp(l1, l2):
    if compare(l1, l2):
        return -1
    else:
        return 1

packets.sort(key=cmp_to_key(cmp))
p2 = 1
for i in range(len(packets)):
    if packets[i] in ([[2]], [[6]]):
        p2 *= (i+1)
print(p2)


