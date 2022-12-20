from copy import copy
from collections import deque

indices, names = {}, {}
flows, edges = [], []
#for i, line in enumerate(open('ex.txt')):
for i, line in enumerate(open('input.txt')):
    l, r = line.strip().split('; ')
    node = l.split(' ')[1]
    indices[node] = i
    names[i] = node
    flows.append( int(l.split('=')[-1]) )
    edges.append( [n.strip(',') for n in r.split(' ')[4:]] )

edges = [[indices[e] for e in ee] for ee in edges]

path_mem = {}
def find_path(start, end):
    if (start, end) not in path_mem:
        #print(f'Finding a path from {start} to {end}')
        q = deque()
        q.append((start, []))
        
        visited = set()
        while q:
            p, path = q.popleft()
            if p in visited:
                continue
            visited.add(p)
            path_mem[(start, p)] = path
            for n in edges[p]:
                q.append((n, path+[n]))
    return tuple(path_mem[(start, end)])


# part 1
mem = {}
def choose_action(pos, t, states):
    if (pos, t, states) in mem:
        return mem[(pos, t, states)]

    if t < 0 or all(states):
        #print(f'Reached the end of the game at time {t} and {sum(states)} valves open')
        return 0
    
    closed_valves = [i for i in range(len(states)) if states[i]==0]

    scores = []
    for valve in closed_valves:
        path = find_path(pos, valve)
        new_t = t - len(path)
        # do we have enough time?
        if new_t - 1 < 0:
            continue
        score = (new_t - 1) * flows[valve]
        new_states = tuple(states[i] if i!=valve else 1 for i in range(len(states)))
        score += choose_action(valve, new_t-1, new_states)
        scores.append(score)

    best_score = max(scores) if scores else 0
    mem[(pos, t, states)] = best_score
    return best_score

states = tuple(0 if flows[v] >0 else 1 for v in range(len(flows)))
part1 = choose_action(indices['AA'], 30, states)
print(part1)

# part 2

# first find all partitions of the open valves into two sets
def partition(collection):
    if len(collection) == 1:
        return [[collection, []]]

    results = []
    first = collection[0]
    for left, right in partition(collection[1:]):
        results.append([left + [first], right])
        results.append([left, right + [first]])

    return results

closed_valves = [i for i in range(len(states)) if states[i]==0]
splits = partition(closed_valves)
#print(len(splits))

p2 = 0
for valves1, valves2 in splits:
    #print(f'My valves {valves1}')
    #print(f'Elephants valves {valves2}')
    states1 = tuple(0 if flows[v] >0 and v in valves1 else 1 for v in range(len(flows)))
    states2 = tuple(0 if flows[v] >0 and v in valves2 else 1 for v in range(len(flows)))
    score1 = choose_action(indices['AA'], 26, states1)
    score2 = choose_action(indices['AA'], 26, states2)
    p2 = max(p2, score1 + score2)
    #print(f'Total score: {score1 + score2}')
    #print()

print(p2)
