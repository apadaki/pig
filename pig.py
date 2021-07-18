import random, time
import numpy as np
import pig_ai

# USER PARAMS
DIE, TARGET = 6, 100
TURN_TIME = 0.5

ai_probs = pig_ai.get_probabilities(TARGET)
pig_ai.save_probabilities(ai_probs, 'probabilities_{}_{}.txt'.format(DIE, TARGET))
# ai_probs = pig_ai.load_probabilities('probabilities_{}_{}.txt'.format(DIE, TARGET))

# END USER PARAMS

def roll():
    return random.randint(1,DIE)

def turn(player, isAI, score, other_score, log = True):
    round = 0
    hold = 0
    bust = 0
    while score + round < TARGET and not hold and not bust:
        r = roll()
        if r != 1:
            round += r
        else:
            round = 0
        if log:
            print('[{} turn | round total: {} | tentative total: {}]'.format(player, round, score+round))
        if r == 1:
            bust = 1
            if isAI:
                if log:
                    print('\toh no, {} rolled a 1! SCORE RESET TO {}.'.format(player, score))
            else:
                if log:
                    input('\toh no, {} rolled a 1! SCORE RESET TO {}. (press ENTER to continue)'.format(player, score))

        if not bust and score + round < TARGET:
            if isAI:
                hold, hold_val, roll_val = pig_ai.hold(ai_probs, score, other_score, round, DIE)
                if log:
                    print('\t{} rolled a {}! {} with confidence {:.4f}.'.format(player, r, 'HOLDING' if hold else 'ROLLING AGAIN', max(hold_val, roll_val)/(hold_val+roll_val)))
            else:
                if log:
                    hold = 1 if input('\t{} rolled a {}!\n\troll again (y/n)? '.format(player, r)) == 'n' else 0
        if log:
            time.sleep(TURN_TIME)
    score += round
    if score >= TARGET:
        if log:
            print('\t{} rolled a {}!'.format(player, r))
        return player, player, score
    return 0, player, score

def game(AI_A=False, AI_B=False, log=True, turn_buffer=False, playerA = 'Alice', playerB = 'Bob'):
    if not (AI_A and AI_B):
        log = True
        turn_buffer = False
    if log:
        print('NEW GAME [{}-sided die | first to {} wins]'.format(DIE, TARGET))
    random.seed()
    scoreA,scoreB = 0,0
    winner = 0
    t = 0
    while not winner:
        if log:
            print('\n-----TURN {}{}: [{} ({}): {} | {} ({}): {}]-----'.format((t+2)//2, 'A' if t%2 == 0 else 'B', playerA, 'AI' if AI_A else 'HUMAN', scoreA, playerB, 'AI' if AI_B else 'HUMAN', scoreB), end='')
        if turn_buffer:
            input()
        else:
            print()
        if t%2 == 0:
            winner, playerA, scoreA = turn(playerA, AI_A, scoreA, scoreB, log)
        else:
            winner, playerB, scoreB = turn(playerB, AI_B, scoreB, scoreA, log)
        t+=1

    if log:
        print('\n------FINAL SCORE: [{} ({}): {} | {} ({}): {}]------\nWINNER: {}'.format(playerA, 'AI' if AI_A else 'HUMAN', scoreA, playerB, 'AI' if AI_B else 'HUMAN', scoreB, winner))
    return playerA == winner



if __name__ == '__main__':
    """ User Arguments (see defaults above):
            - AI_A, AI_B        determines which player(s) are controlled by the AI
            - log               determines whether game information is logged to the console
            - turn_buffer       determines whether logging pauses between turns
            - playerA, playerB  are player names
    """
    game(AI_A = True, AI_B = True, turn_buffer = True)
    """ short script to get win percentage by first player when both play optimally
        NUM_TRIALS = 10000
        wins_first = 0
        for i in range(NUM_TRIALS):
            if i%10 == 0:
                print(i)
            wins_first += game(AI_A = True, AI_B = True, log = False)
        print('win probability for first player: {:.3f}'.format(wins_first/NUM_TRIALS))
    """
