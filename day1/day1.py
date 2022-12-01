elves = []
with open('input.txt') as ifile:
    calories = 0
    for line in ifile:
        line = line.strip()
        #print(line)
        if line == '':
            elves.append(calories)
            calories = 0
        else:
            calories += int(line)

#print(elves)
print(len(elves))
# part 1
print('Calories carried by the elf with the most snacks: ', max(elves))

#part 2
top3 = sorted(elves)[-3:]
print(top3)
print('Calories carried by top 3 elves', sum(top3))
