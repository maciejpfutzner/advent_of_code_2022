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
max_t = 26
def choose_action(pos, t, states):
    if (pos, t, states) in mem:
        return mem[(pos, t, states)]

    if t > max_t or all(states):
        #print(f'Reached the end of the game at time {t} and {sum(states)} valves open')
        return 0
    
    closed_valves = [i for i in range(len(states)) if states[i]==0]

    scores = []
    for valve in closed_valves:
        path = find_path(pos, valve)
        new_t = t + len(path)
        # do we have enough time?
        if new_t + 1 > max_t:
            continue
        score = (max_t - new_t) * flows[valve]
        new_states = tuple(states[i] if i!=valve else 1 for i in range(len(states)))
        score += choose_action(valve, new_t+1, new_states)
        scores.append(score)

    best_score = max(scores) if scores else 0
    mem[(pos, t, states)] = best_score
    return best_score

states = tuple(0 if flows[v] >0 else 1 for v in range(len(flows)))
part1 = choose_action(indices['AA'], 1, states)
print(part1)
assert False


############################################################
# part 2
max_t = 26

def get_moves(pos1, path1, t, states):
    score = 0
    if path1:
        # If on a mission, continue
        new_p1s = [(path1[0], path1[1:])]
    elif states[pos1] == 0:
        # Open the valve
        score = (max_t - t) * flows[pos1]
        states = tuple(states[i] if i!=pos1 else 1 for i in range(len(states)))
        new_p1s = [(pos1, tuple())]
    else:
        new_p1s = []
        # We opened the valve last turn
        closed_valves = [i for i in range(len(states)) if states[i]==0]
        for v in closed_valves:
            path = find_path(pos1, v)
            # do we have enough time?
            if len(path) + t + 1 <= max_t:
                new_p1s.append((path[0], path[1:]))
        if not new_p1s:
            # If there are no more closed valves for you, just stay put
            new_p1s = [(pos1, tuple())]
    return new_p1s, states, score

mem = {} # For keeping memory of scored for a full state
def choose_action2(p1, p2, t, states):
    if t > max_t or all(states):
        #print(f'Reached the end of the game at time {t} and {sum(states)} valves open')
        return 0
        #return 0, [(p1[0], p2[0])]

    if (p1, p2, t, states) in mem:
        return mem[(p1, p2, t, states)]
    if (p2, p1, t, states) in mem:
        return mem[(p2, p1, t, states)]

    pos1, path1 = p1#[0], deque(p1[1])
    pos2, path2 = p2#[0], deque(p2[1])

    scores = []
    #print(pos1, path1, pos2, path2)
    new_p1s, new_states1, s1 = get_moves(pos1, path1, t, states)
    assert len(new_p1s) == 1 or s1 == 0
    new_p2s, new_states, s2 = get_moves(pos2, path2, t, new_states1)
    assert len(new_p2s) == 1 or s2 == 0

    for new_p1 in new_p1s:
        for new_p2 in new_p2s:
            if new_p1 != new_p2:
                score = choose_action2(new_p1, new_p2, t+1, new_states)
                scores.append(score + s1 + s2)
                #score, hist = choose_action2(new_p1, new_p2, t+1, new_states)
                #scores.append((score + s1 + s2, hist))

    #if len(scores) == 0:
    #    score = choose_action2(new_p1s[0], new_p2s[0], t+1, new_states)
    #    scores = [score + s1 + s2]
        #score, hist = choose_action2(new_p1s[0], new_p2s[0], t+1, new_states)
        #scores = [(score + s1 + s2, hist)]

    best_score = max(scores) if scores else s1+s2
    #best_score = 0
    #for s,h in scores:
    #    if s >= best_score:
    #        best_score = s
    #        best_hist = h + [(pos1, pos2)]

    mem[(p1, p2, t, states)] = best_score
    #mem[(p1, p2, t, states)] = best_score, best_hist
    return best_score #, best_hist

states = tuple(0 if flows[v] >0 else 1 for v in range(len(flows)))
p1 = p2 = (indices['AA'], tuple())
part2 = choose_action2(p1, p2, 1, states)
print(part2)
#print([[names[i] for i in pos] for pos in hist])

#print(get_moves(2, deque([1]), 1, deque([]), 2, states))
