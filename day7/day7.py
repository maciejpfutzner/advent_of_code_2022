import sys
from collections import defaultdict
sys.setrecursionlimit(2000)

lines = [l.strip() for l in open('input.txt').readlines()]
print(lines[:5])


#dirtree = {'/': []}
dirtree = defaultdict(set)
#filetree = {'/': []}
filetree = defaultdict(set)

tree = {'/': {}}

curdir = '/'
subtree = tree['/']

path = [] # Directories above us
cursize = 0

def get_subtree(path):
    subtree = tree
    for d in path:
        subtree = subtree[d]
    return subtree

class Dir:
    def __init__(self, name):
        self.name = name
        self.files_size = 0
        self.subdirs = []
    
    def add_file(self, size):
        self.file_size += size

    def add_subdir(self, name):
        self.subdirs.append(Dir(name))

    def get_subdir(self, name):
        for subdir in self.subdirs:
            if subdir.name == name:
                return subdir


for line in lines:
    cmds = line.split()
    print(cmds)
    if cmds[0] == '$':
        # flush the sizes
        subtree 
        if cmds[1] == 'cd':
            nextdir = cmds[2] 
            #if nextdir == '/':
            #    path = []
            #    curdir = '/'
            #    print('Going all the way to /')
            #elif nextdir == '..':
            if nextdir == '..':
                curdir = path.pop()
                subtree = get_subtree(path)[curdir]
                print(f'Going up to {curdir}')
            else:
                curdir = nextdir
                path.append(curdir)
                subtree = get_subtree(path)[curdir]

                print(f'Going down to {curdir}')
        #elif cmds[1] == 'ls':
        #    continue
    elif cmds[0] == 'dir':
        # Is this necessary?
        newdir = cmds[1]
        dirtree[curdir].add(newdir)
    else:
        size, file = cmds
        filetree[curdir].add(( file, int(size) ))
        cursize += int(size)

print(dirtree)
print()
print(filetree)

counter = 0
sizes = {}
def find_size(dir_):
    global counter
    counter += 1
    if counter > 20:
        raise RuntimeError()
    if dir_ in sizes:
        return sizes[dir_]

    files = list(filetree[dir_])
    file_size = sum([f[1] for f in files])
    print(f'Total file size in {dir_} is {file_size}')
    
    subdir_size = 0
    print(f'Subdirs are {dirtree[dir_]}')
    for subdir in dirtree[dir_]:
        print(f'Checking subdir {subdir}')
        subdir_size += find_size(subdir)

    total_size = file_size + subdir_size
    sizes[dir_] = total_size
    return total_size

find_size('/')
#find_size('wlmtj')
#print(sizes)
                    
