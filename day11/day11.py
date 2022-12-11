import sys
from collections import Counter, defaultdict
monkeys_txt = open('input.txt').read().split('\n\n')

inspected = Counter()
divs = [2, 3, 5, 7, 11, 13, 17, 19, 23]

class Monkey:
    def __init__(self, input_):
        #print(input_)
        lines = input_.splitlines()
        self.name = lines[0].split()[1][:-1]

        items_offset = len('  Starting items: ')
        items = [int(it) for it in lines[1][items_offset:].split(', ')]
        self.items = [[it%d for d in divs] for it in items]

        op_offset = len('  Operation: new = old')
        operator, operand = lines[2][op_offset:].split()
        self.operation = self._parse_op(operator, operand)
        
        self.test_div = int(lines[3].split()[-1])
        self.test_idx = [i for i in range(len(divs)) if divs[i] == self.test_div][0]
        self.true_dest = int(lines[4].split()[-1])
        self.false_dest = int(lines[5].split()[-1])

    def _parse_op(self, operator, operand):
        def func(old):
            if operator == '*':
                if operand == 'old':
                    new = [(n*n) % d for n,d in zip(old, divs)]
                else:
                    new = [(n * int(operand)) % d for n,d in zip(old, divs)]
            else:
                new = [(n + int(operand)) % d for n,d in zip(old, divs)]
            #print(old, new)
            return new
        return func

    def do_turn(self, monkeys):
        for i in range(len(self.items)):
            item = self.items.pop(0)
            inspected[self.name] += 1
            score = self.operation(item) 
            #score = [(s//3) %d for (s,d) in zip(score, divs)]

            #if score % self.test_div == 0:
            if score[self.test_idx] == 0:
                monkeys[self.true_dest].items.append(score)
            else:
                monkeys[self.false_dest].items.append(score)
        

# store them in a list - indices should correspond to their names
monkeys = [Monkey(mon) for mon in monkeys_txt]

#divs = sorted([m.test_div for m in monkeys])
#print(divs)

for i in range(10_000):
    for monkey in monkeys:
        monkey.do_turn(monkeys)

top2 = [c[1] for c in inspected.most_common(2)]
p2 = top2[0] * top2[1]
print(p2)
