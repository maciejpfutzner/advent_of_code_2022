board, instructions = open('input.txt').read().split('\n\n')

faces = {}
lines = [line.strip('\n') for line in board.splitlines()]
faces['a'] = [line[50 : 100] for line in lines[0 : 50]]
faces['c'] = [line[100 : 150] for line in lines[0 : 50]]
faces['b'] = [line[50 : 100] for line in lines[50 : 100]]
faces['f'] = [line[0 : 50] for line in lines[100 : 150]]
faces['d'] = [line[50 : 100] for line in lines[100 : 150]]
faces['e'] = [line[0 : 50] for line in lines[150 : 200]]

# direction is an index from 0-3
# up, right, down, left
dr = [-1, 0, 1, 0]
dc = [0, 1, 0, -1]

# The mapping will returni face, row, column, direction
mapping = {'a': {'u': lambda r, c: ('e', c, 0, 1),
                 'd': lambda r, c: ('b', 0, c, 2),
                 'l': lambda r, c: ('f', R-r-1, 0, 1),
                 'r': lambda r, c: ('c', r, 0, 1)
                 },
           'f': {'u': lambda r, c: ('b', c, 0, 1),
                 'd': lambda r, c: ('e', 0, c, 2),
                 'l': lambda r, c: ('a', R-1-r, 0, 1),
                 'r': lambda r, c: ('d', r, 0, 1)
                 },
           'c': {'u': lambda r, c: ('e', 49, c, 0),
                 'd': lambda r, c: ('b', c, 49, 3),
                 'l': lambda r, c: ('a', r, 49, 3),
                 'r': lambda r, c: ('d', R-r-1, 49, 3)
                 },
           'd': {'u': lambda r, c: ('b', 49, c, 0),
                 'd': lambda r, c: ('e', c, 49, 3),
                 'l': lambda r, c: ('f', r, 49, 3),
                 'r': lambda r, c: ('c', R-1-r, 49, 3)
                 },
           'b': {'u': lambda r, c: ('a', 49, c, 0),
                 'd': lambda r, c: ('d', 0, c, 2),
                 'l': lambda r, c: ('f', 0, r, 2),
                 'r': lambda r, c: ('c', 49, r, 0)
                 },
           'e': {'u': lambda r, c: ('f', 49, c, 0),
                 'd': lambda r, c: ('c', 0, c, 2),
                 'l': lambda r, c: ('a', 0, r, 2),
                 'r': lambda r, c: ('d', 49, r, 0)
                 },
           }

R, C = 50, 50
assert all(len(lines) == R for lines in faces.values())
assert all(len(lines[0]) == C for lines in faces.values())

instructions = instructions.strip().replace('L', ' L ').replace('R', ' R ').split()
instructions = [int(i) if i not in ['L', 'R'] else i for i in instructions]

# face, row, column, direction
# start facing right
pos = ('a', 0, 0, 1)

for i, instr in enumerate(instructions):
    print(i, pos, instr)
    face, r, c, dd = pos
    if instr == 'L':
        dd = (dd - 1) %4
        pos = face, r, c, dd
    elif instr == 'R':
        dd = (dd + 1) %4
        pos = face, r, c, dd
    else:
        for i in range(instr):
            if dr[dd] != 0:
                r += dr[dd]
                if r < 0:
                    face, r, c, dd = mapping[face]['u'](r, c)
                elif r >= R:
                    face, r, c, dd = mapping[face]['d'](r, c)
            elif dc[dd] != 0:
                c += dc[dd]
                if c < 0:
                    face, r, c, dd = mapping[face]['l'](r, c)
                elif c >= C:
                    face, r, c, dd = mapping[face]['r'](r, c)
            if faces[face][r][c] == '#':
                break
            else:
                pos = face, r, c, dd

face, r, c, dd = pos
print(face, r, c, dd)
if face == 'a':
    c += 50
elif face == 'e':
    r += 150
else:
    raise NotImplementedError
p2 = 1000 * (r+1) + 4 * (c+1) + (dd - 1)%4
print(p2)
