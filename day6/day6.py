from collections import deque
stream = open("input.txt").read().strip()

def find_marker(n_chars):
    buffer = deque('_' + stream[:n_chars-1])
    for i in range(n_chars-1, len(stream)):
        buffer.popleft()
        buffer.append(stream[i])
        if len(set(buffer)) == n_chars:
            break
    return i+1

print(find_marker(4))
print(find_marker(14))

