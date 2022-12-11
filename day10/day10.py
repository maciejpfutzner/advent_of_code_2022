#lines = [l.strip() for l in open('ex.txt').readlines()]
lines = [l.strip() for l in open('input.txt').readlines()]

X = [1]
pixels = ['█'] # Using special character for visibility

def draw(i, x):
    if x-1 <= i%40 <= x+1:
        return '█'
    else:
        return ' '

i = 1
for line in lines:
    x = X[-1]
    if line == 'noop':
        pixels.append(draw(i, x))
        X.append(x)
        i += 1
    else:
        pixels.append(draw(i, x))
        X.append(x)
        x += int(line.split()[1])
        pixels.append(draw(i+1, x))
        X.append(x)
        i += 2

steps = list(range(20, 221, 40))

acc = 0
print('Part 2:')
for step in steps:
    #print(f"x at step {step} is {X[step]}")
    acc += step * X[step-1]
    print(''.join(pixels[step-20 : step+20]))

print('Part 1:', acc)


