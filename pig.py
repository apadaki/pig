import random, time, os
import pig_ai

class PigGame:
    def __init__(self, die=6, target=100, turn_time = 0.5, generate_new = False):
        self.DIE = die
        self.TARGET = target
        self.TURN_TIME = turn_time
        if os.path.isfile('probabilities_{}_{}.txt'.format(self.DIE, self.TARGET)) and not generate_new:
            self.ai_probs = pig_ai.load_probabilities('probabilities_{}_{}.txt'.format(self.DIE, self.TARGET))
        else:
            self.ai_probs = pig_ai.get_probabilities(self.TARGET)
            pig_ai.save_probabilities(self.ai_probs, 'probabilities_{}_{}.txt'.format(self.DIE, self.TARGET))

    def __roll(self):
        return random.randint(1,self.DIE)

    def __turn(self, player, isAI, score, other_score, log = True):
        round = 0
        hold = 0
        bust = 0
        while score + round < self.TARGET and not hold and not bust:
            r = self.__roll()
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

            if not bust and score + round < self.TARGET:
                if isAI:
                    hold, hold_val, roll_val = pig_ai.hold(self.ai_probs, score, other_score, round, self.DIE)
                    if log:
                        print('\t{} rolled a {}! {} with confidence {:.4f}.'.format(player, r, 'HOLDING' if hold else 'ROLLING AGAIN', max(hold_val, roll_val)/(hold_val+roll_val)))
                else:
                    if log:
                        hold = 1 if input('\t{} rolled a {}!\n\troll again (y/n)? '.format(player, r)) == 'n' else 0
            if log:
                time.sleep(self.TURN_TIME)
        score += round
        if score >= self.TARGET:
            if log:
                print('\t{} rolled a {}!'.format(player, r))
            return player, player, score
        return 0, player, score

    def game(self, AI_A=False, AI_B=False, log=True, turn_buffer=False, playerA = 'Alice', playerB = 'Bob'):
        if not (AI_A and AI_B):
            log = True
            turn_buffer = False
        if log:
            print('NEW GAME [{}-sided die | first to {} wins]'.format(self.DIE, self.TARGET))
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
                winner, playerA, scoreA = self.__turn(playerA, AI_A, scoreA, scoreB, log)
            else:
                winner, playerB, scoreB = self.__turn(playerB, AI_B, scoreB, scoreA, log)
            t+=1

        if log:
            print('\n------FINAL SCORE: [{} ({}): {} | {} ({}): {}]------\nWINNER: {}'.format(playerA, 'AI' if AI_A else 'HUMAN', scoreA, playerB, 'AI' if AI_B else 'HUMAN', scoreB, winner))
        return playerA == winner