from string import ascii_lowercase, ascii_uppercase

with open('input.txt') as infile:
    rucksacks = [l.strip() for l in infile]

test = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""
#rucksacks = test.split()

#print(rucksacks[:6])

def priority(item):
    if item in ascii_lowercase:
        score = ord(item) - ord('a') + 1
    else:
        score = ord(item) - ord('A') + 27
    #print(item, score)
    return score

# part 1 - find common items per rucksack
items = []
total_score = 0
for i, rs in enumerate(rucksacks):
    l, r = rs[: len(rs)/2], rs[len(rs)/2: ]
    item = set(l) & set(r)
    if len(item) != 1:
        print(i, l, r, item)
    item = list(item)[0]
    items.append(item)
    total_score += priority(item)

print(total_score)


# part 2 - find common item in each group of 3
score2 = 0
for i in range(0, len(rucksacks), 3):
    #print(i)
    r1, r2, r3 = rucksacks[i: i+3]
    #print(r1, r2, r3)
    item = set(r1) & set(r2) & set(r3)
    assert len(item) == 1
    score2 += priority(list(item)[0])

print(score2)
