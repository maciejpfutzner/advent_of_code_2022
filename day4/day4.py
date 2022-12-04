pairs = []
for line in open('input.txt'):
    l, r = line.strip().split(',')
    l = [int(n) for n in l.split('-')]
    r = [int(n) for n in r.split('-')]
    pairs.append((l, r))

#print(pairs[0])

fo_count = 0
po_count = 0
for (llo, lhi), (rlo, rhi) in pairs:
    assert lhi >= llo
    assert rhi >= rlo
    if (llo <= rlo and lhi >= rhi) or (rlo <= llo and rhi >= lhi):
        fo_count += 1
    if lhi >= rlo and rhi >= llo:
        po_count += 1
    
#print(len(pairs))
print('Part 1:', fo_count)
print('Part 2:', po_count)
