from pig import PigGame
import pig_ai # for generating contour plots

""" Game User Arguments (see defaults above):
        - die               number of sides on game die
        - target            how many points one must obtain to win
        - turn_time         time buffer between turns
        - generate_new      whether to automatically generate a new probabilities file
    -----------------------
        - AI_A, AI_B        determines which player(s) are controlled by the AI
        - log               determines whether game information is logged to the console
        - turn_buffer       determines whether logging pauses between turns
        - playerA, playerB  are player names
"""
pg = PigGame(die=20, target=1000, turn_time=0.5, generate_new = True)

pg.game(AI_A = True, AI_B = True, turn_buffer = True)

""" short script to get win percentage by first player when both play optimally
    NUM_TRIALS = 10000
    wins_first = 0
    for i in range(NUM_TRIALS):
        if i%10 == 0:
            print(i)
        wins_first += pig.game(AI_A = True, AI_B = True, log = False)
    print('win probability for first player: {:.3f}'.format(wins_first/NUM_TRIALS))
"""
