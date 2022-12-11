import sys
from collections import Counter, defaultdict
monkeys_txt = open('input.txt').read().split('\n\n')

inspected = Counter()

class Monkey:
    def __init__(self, input_):
        print(input_)
        lines = input_.splitlines()
        self.name = lines[0].split()[1][:-1]

        items_offset = len('  Starting items: ')
        self.items = [int(it) for it in lines[1][items_offset:].split(', ')]

        op_offset = len('  Operation: new = old')
        operator, operand = lines[2][op_offset:].split()
        self.operation = self._parse_op(operator, operand)
        
        self.test_div = int(lines[3].split()[-1])
        self.true_dest = int(lines[4].split()[-1])
        self.false_dest = int(lines[5].split()[-1])

    def _parse_op(self, operator, operand):
        def func(old):
            return eval('old' + operator + operand)
        return func

    def do_turn(self, monkeys):
        #print(f'Monkey {self.name} has items {self.items}')
        for i in range(len(self.items)):
            item = self.items.pop(0)
            inspected[self.name] += 1
            score = self.operation(item) //3

            if score % self.test_div == 0:
                #print(f'Monkey {self.name} throws item {score} to monkey {self.true_dest}')
                monkeys[self.true_dest].items.append(score)
            else:
                #print(f'Monkey {self.name} throws item {score} to monkey {self.false_dest}')
                monkeys[self.false_dest].items.append(score)
        

# store them in a list - indices should correspond to their names
monkeys = [Monkey(mon) for mon in monkeys_txt]

#divs = [m.test_div for m in monkeys]
#print(sorted(divs))

for i in range(20):
    for monkey in monkeys:
        monkey.do_turn(monkeys)

top2 = [c[1] for c in inspected.most_common(2)]
p1 = top2[0] * top2[1]
print(p1)
