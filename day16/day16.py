from copy import copy

indices = {}
flows, edges = [], []
#for i, line in enumerate(open('ex.txt')):
for i, line in enumerate(open('input.txt')):
    l, r = line.strip().split('; ')
    node = l.split(' ')[1]
    indices[node] = i
    flows.append( int(l.split('=')[-1]) )
    edges.append( [n.strip(',') for n in r.split(' ')[4:]] )

edges = [[indices[e] for e in ee] for ee in edges]
#print(indices)
#print(flows)
#print(edges)

# part 1
mem = {}
max_t = 30
def choose_action(pos, t, states):
    if (pos, t, states) in mem:
        return mem[(pos, t, states)]

    if t > max_t or all(states):
        #print(f'Reached the end of the game at time {t} and {sum(states.values())} valves open')
        return 0

    moves = edges[pos]
    scores = []

    # Get the scores for each destination
    for move in edges[pos]:
        score = choose_action(move, t+1, states)
        scores.append(score)

    # If the local valve isn't open, we can open it
    if states[pos] == 0:
        score = (max_t - t) * flows[pos] 
        states_new = tuple(states[i] if i!=pos else 1 for i in range(len(states)))
        score += choose_action(pos, t+1, states_new)
        scores.append(score)

    best_score = max(scores)
    mem[(pos, t, states)] = best_score
    return best_score

states = tuple(0 if flows[v] >0 else 1 for v in range(len(flows)))
total_score = choose_action(indices['AA'], 1, states)
print(total_score)

# part 2
max_t = 20
max_t = 14

mem = {} # For keeping memory of scored for a full state
state_mem = {} # Keep a memory of earliest time at a reduced state
pos_mem = {}

counters = [0, 0, 0, 0]
def choose_action2(pos, elpos, t, states):
    if t > max_t or all(states):
        #print(f'Reached the end of the game at time {t} and {sum(states)} valves open')
        return 0

    if (pos, elpos, t, states) in mem:
        #print('Found same state')
        #counters[1] += 1
        return mem[(pos, elpos, t, states)]
    if (elpos, pos, t, states) in mem:
        #print('Found flipped state')
        #ounters[1] += 1
        return mem[(elpos, pos, t, states)]

    # Check if we've been here at an earlier time step
    if (pos, elpos, states) in state_mem:
        if state_mem[(pos, elpos, states)] < t:
            #ounters[2] += 1
            #mem[(pos, elpos, t, states)] = 0
            return 0
    if (elpos, pos, states) in state_mem:
        if state_mem[(elpos, pos, states)] < t:
            #ounters[2] += 1
            #mem[(elpos, pos, t, states)] = 0
            return 0
    state_mem[(pos, elpos, states)] = t

    #if (pos, elpos) in pos_mem:
    #    mstates, mtime = pos_mem[(pos, elpos)]
    #    if mtime <= t and sum(mstates) > sum(states):
    #        if all([ms >= s for ms, s in zip(mstates, states)]):
    #            counters[3] += 1
    #            return 0
    #if (elpos, pos) in pos_mem:
    #    mstates, mtime = pos_mem[(elpos, pos)]
    #    if mtime <= t and sum(mstates) > sum(states):
    #        if all([ms >= s for ms, s in zip(mstates, states)]):
    #            counters[3] += 1
    #            return 0
    #pos_mem[(pos, elpos)] = states, t

    #counters[0] += 1
    scores = []

    # Get the scores for each destination
    for move in edges[pos]:
        for elmove in edges[elpos]:
            # You both move
            score = choose_action2(move, elmove, t+1, states)
            scores.append(score)

    if states[elpos] == 0:
        # You move, elephant opens a valve
        for move in edges[pos]:
            score = (max_t - t) * flows[elpos] 
            states_new = tuple(states[i] if i!=elpos else 1 for i in range(len(states)))
            score += choose_action2(move, elpos, t+1, states_new)
            scores.append(score)
        # You both open a valve
        if states[pos] == 0 and pos != elpos:
            score = (max_t - t) * (flows[pos] + flows[elpos])
            states_new = tuple(states[i] if i not in (pos, elpos) else 1
                               for i in range(len(states)))
            score += choose_action2(pos, elpos, t+1, states_new)
            scores.append(score)

    if states[pos] == 0:
        for elmove in edges[elpos]:
        # Elephant moves, you open a valve
            score = (max_t - t) * flows[pos] 
            states_new = tuple(states[i] if i!=pos else 1 for i in range(len(states)))
            score += choose_action2(pos, elmove, t+1, states_new)
            scores.append(score)

    best_score = max(scores)
    mem[(pos, elpos, t, states)] = best_score
    return best_score

states = tuple(0 if flows[v] >0 else 1 for v in range(len(flows)))
total_score = choose_action2(indices['AA'],indices['AA'], 1, states)
print(total_score)

#print(f'{counters[0]:,} total moves explored')
##print(f'{counters[1]:,} moves saved by direct memoization, {counters[2]:,} saved from flipped states')
#print(f'{counters[1]:,} moves saved by direct memoization, {counters[2]:,} saved from earlier position')
#print(f'And {counters[3]:,} moves saved by shenanigans')

