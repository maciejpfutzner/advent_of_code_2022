import math

blueprints = []
for line in open('input.txt'):
#for line in open('ex.txt'):
    parts = line.strip().split() 
    blueprint = {}
    blueprint['ore'] = {'ore': int(parts[6])}
    blueprint['clay'] = {'ore': int(parts[12])}
    blueprint['obsidian'] = {'ore': int(parts[18]), 'clay': int(parts[21])}
    blueprint['geode'] = {'ore': int(parts[27]), 'obsidian': int(parts[30])}
    blueprints.append(blueprint)


# ore, clay, obsidian, geodes
resources = (0, 0, 0, 0)
robots = (1, 0, 0, 0)

#max_orebots = 5
#max_claybots = 6
#max_ore = 10
#max_clay = 20
def move(resources, robots, t, blueprint, mem):
    #print(f"At time {t} we have {robots} robots and {resources} resources")

    if any(r < 0 for r in resources):
        print(resources)
        assert False, "negative resources"

    if t == 0:
        #print(robots, resources)
        return resources[3]

    if t in mem:
        if (resources, robots) in mem[t]:
            return mem[t][(resources, robots)]
        elif t<3 and max(mem[t].values()) > t*(t+1)/2:
            return 0
    else:
        mem[t] = {}

    o, c, b, g = resources
    ro, rc, rb, rg = robots
    
    outcomes = []
    max_ro = max([cost['ore'] for cost in blueprint.values()])
    max_c = blueprint['obsidian']['clay']
    max_b = blueprint['geode']['obsidian']

    if o >= blueprint['geode']['ore'] and b >= blueprint['geode']['obsidian']:
        # We can build a geode robot next
        new_resources = (o + ro - blueprint['geode']['ore'], c + rc,
                         b + rb - blueprint['geode']['obsidian'], g + rg)
        new_robots = (ro, rc, rb, rg +1)
        outcomes.append( move(new_resources, new_robots, t-1, blueprint, mem) )

    else:
        if b < max_b and o >= blueprint['obsidian']['ore'] and c >= blueprint['obsidian']['clay']:
            # We can build an obsidian robot next
            new_resources = (o + ro - blueprint['obsidian']['ore'], c + rc - blueprint['obsidian']['clay'],
                            b + rb, g + rg)
            new_robots = (ro, rc, rb +1, rg)
            outcomes.append( move(new_resources, new_robots, t-1, blueprint, mem) )

        else:
            if ro < max_ro and o >= blueprint['ore']['ore']:
            # We can build an ore robot this turn
                new_resources = (o + ro - blueprint['ore']['ore'], c + rc, b + rb, g + rg)
                new_robots = (ro+1, rc, rb, rg)
                outcomes.append( move(new_resources, new_robots, t-1, blueprint, mem) )

            if c < max_c and o >= blueprint['clay']['ore']:
            # We can build a clay robot this turn
                new_resources = (o + ro - blueprint['clay']['ore'], c + rc, b + rb, g + rg)
                new_robots = (ro, rc+1, rb, rg)
                outcomes.append( move(new_resources, new_robots, t-1, blueprint, mem) )

        # You can also just skip this turn, but not when you can build anything
        new_resources = (o + ro, c + rc, b + rb, g + rg)
        outcomes.append( move(new_resources, robots, t-1, blueprint, mem) )

    best_outcome = max(outcomes)
    mem[t][(resources, robots)] = best_outcome
    return best_outcome


resources = (0, 0, 0, 0)
robots = (1, 0, 0, 0)

p1 = 0
for i, bp in enumerate(blueprints):
    score = move(resources, robots, 24, bp, {})
    print(f'Blueprint {i+1} got {score} geodes')
    p1 += (i+1) * score
print(p1)

p2 = 1
for bp in blueprints[:3]:
    score = move(resources, robots, 32, bp, {})
    print(f'Blueprint got {score} geodes')
    p2 *= score
print(p2)
