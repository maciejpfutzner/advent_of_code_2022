monkeys = {}
for line in open('input.txt'):
    name, expr = line.strip().split(': ')
    try:
        expr = int(expr)
    except:
        pass
    monkeys[name] = expr

max_depth = 0
def solve(name, depth=0):
    global max_depth
    max_depth = max(depth, max_depth)
    val = monkeys[name]
    if isinstance(val, int):
        return val
    else:
        l, op, r = val.split()
        l = solve(l, depth+1)
        r = solve(r, depth+1)
        return int(eval(f'l {op} r'))

p1 = solve('root')
print(p1)

# find all monkeys inheriting from the human
def find_human(name, ancestors):
    if name == 'humn':
        ancestors.append(name)
        return True

    val = monkeys[name]
    if isinstance(val, int):
        return False
    else:
        l, op, r = val.split()
        if find_human(l, ancestors) or find_human(r, ancestors):
            ancestors.append(name)
            return True
    return False

# if expression is lval + rval = value
#   lval = value - rval
#   rval = value - lval
# if expression is lval * rval = value
#   lval = value / rval
#   rval = value / lval
# if expression is lval - rval = value
#   lval = value + rval
#   rval = lval - value
# if expression is lval / rval = value
#   lval = value * rval
#   rval = lval / value
reverse = {'+': {'r': 'value - lval', 'l':  'value - rval'},
           '*': {'r': 'value / lval', 'l':  'value / rval'},
           '-': {'r': 'lval - value', 'l':  'value + rval'},
           '/': {'r': 'lval / value', 'l':  'value * rval'},
           }

def find_match(name, value, ancestors):
    if name == 'humn':
        return int(value)
    l, op, r = monkeys[name].split()
    if l in ancestors:
        rval = solve(r)
        lval = eval(reverse[op]['l'])
        return find_match(l, lval, ancestors)
    elif r in ancestors:
        lval = solve(l)
        rval = eval(reverse[op]['r'])
        return find_match(r, rval, ancestors)
    else:
        print(name, value)
        assert False

ancestors = []
find_human('root', ancestors)

l, _, r = monkeys['root'].split()
assert r not in ancestors
rval = solve(r)

p2 = find_match(l, rval, ancestors)
print(p2)
