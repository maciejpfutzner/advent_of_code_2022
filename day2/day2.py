with open('input.txt') as infile:
    games = [l.strip() for l in infile]

#print(games)
scores = {'X': 1, 'Y': 2, 'Z': 3}
beats = {'A': 'Y', 'B': 'Z', 'C': 'X'}
beaten = {'A': 'Z', 'B': 'X', 'C': 'Y'}
draw = {'A': 'X', 'B': 'Y', 'C': 'Z'}

mapping = dict(zip('XYZ', 'ABC'))
print(mapping)

score = 0
for game in games:
    play, resp = game.split()
    game_score = scores[resp]
    if mapping[resp] == play:
        game_score += 3
    elif resp == beats[play]:
        game_score += 6
    # print(game, game_score)
    score += game_score

# part 1
print('Score:', score)

# part 2
score = 0
for game in games:
    gscore = 0
    play, result = game.split()
    if result == 'X':
        resp = beaten[play]
        gscore += scores[resp]
    elif result == 'Y':
        gscore = 3 + scores[draw[play]]
    else:
        gscore = 6 + scores[beats[play]]
    print(game, gscore)
    score += gscore

print('Score:', score)
