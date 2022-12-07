lines = [l.strip() for l in open('input.txt').readlines()]

class Dir:
    def __init__(self, name):
        self.name = name
        self.file_size = 0
        self.subdirs = []

    def __repr__(self):
        return f'<{self.name}>'
    
    def add_file(self, size):
        self.file_size += size

    def add_subdir(self, name):
        if name not in {s.name for s in self.subdirs}:
            self.subdirs.append(Dir(name))

    def get_subdir(self, name):
        for subdir in self.subdirs:
            if subdir.name == name:
                return subdir
                                
root = Dir('/')
curdir = root
path = [] # Directories above us

for line in lines:
    cmds = line.split()
    #print(cmds)
    if cmds[0] == '$':
        if cmds[1] == 'cd':
            nextdir = cmds[2] 
            if nextdir == '/':
                curdir == root
                path = []
            elif nextdir == '..':
                curdir = path.pop()
                #print(f'Going up to {curdir}')
            else:
                path.append(curdir)
                curdir = curdir.get_subdir(nextdir)
                #print(f'Going down to {curdir}')
        #elif cmds[1] == 'ls':
        #    continue
    elif cmds[0] == 'dir':
        # Is this necessary?
        newdir = cmds[1]
        curdir.add_subdir(newdir)
    else:
        size, file = cmds
        curdir.add_file(int(size))

# Determine total sizes of each directory recursively
sizes = {}
def find_size(root, verbose=True):
    if root in sizes:
        return sizes[root]

    file_size = root.file_size
    if verbose:
        print(f'Total file size in {root.name} is {file_size}')
    
    subdir_size = 0
    if verbose:
        print(f'Subdirs are: {[root.subdirs]}')
    for subdir in root.subdirs:
        if verbose:
            print(f'Checking subdir {subdir}')
        subdir_size += find_size(subdir, verbose)

    total_size = file_size + subdir_size
    sizes[root] = total_size
    return total_size

total_size = find_size(root, False)
print('Total size:', total_size)
pure_sizes = sorted([sizes[dir_] for dir_ in sizes])

print('Part 1 answer:', sum([s for s in pure_sizes if s <= 100000]))

total_disk = 70000000
needed = 30000000

free_space = total_disk - total_size
to_free = needed - free_space
print('Need to free:', to_free)
print('Part 2 answer:', [s for s in pure_sizes if s > to_free][0])

