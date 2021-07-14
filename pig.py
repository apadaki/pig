import random
import pig_ai

TARGET = 100
f = pig_ai.load_probabilities('probabilities.txt')

def roll():
    return random.randint(1,6)

def turn(player, isAI, score, other_score):
    round = 0
    hold = 0
    bust = 0
    while score + round < TARGET and not hold and not bust:
        r = roll()
        round += r
        print('[{} turn | round total: {} | overall total: {}]'.format(player, round, score+round))
        if r == 1:
            bust = 1
            print('\toh no! {} rolled a 1!'.format(player))
        if not bust and score + round < TARGET:
            if isAI:
                hold = pig_ai.hold(f, score, other_score, round)
            else:
                hold = 1 if input('\t{} rolled a {}!\n\troll again (y/n)? '.format(player, r)) == 'n' else 0
    if not bust:
        score += round
    if score >= TARGET:
        return player, player, score
    return 0, player, score

def game(AI_A=False, AI_B=False):
    random.seed()
    playerA, playerB = 'Alice', 'Bob'
    scoreA,scoreB = 0,0
    winner = 0
    t = 0
    while not winner:
        print('\n-----CURRENT SCORE: [{}: {} | {}: {}]-----'.format(playerA, scoreA, playerB, scoreB))
        if t == 0:
            winner, playerA, scoreA = turn(playerA, AI_A, scoreA, scoreB)
            t = 1
        else:
            winner, playerB, scoreB = turn(playerB, AI_B, scoreB, scoreA)
            t = 0
    print('\n-----FINAL SCORE: [{}: {} | {}: {}]-----\nWINNER: {}'.format(playerA, scoreA, playerB, scoreB, winner))
    return


game(AI_A = True, AI_B = True)