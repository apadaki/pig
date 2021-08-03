# Pig AI

## Description
This is a simple console application to play the dice game [pig](https://en.wikipedia.org/wiki/Pig_(dice_game)).
You can play with combination of human/AI players, with different die sizes and target values.

The AI uses a primitive strategy, and is dynamically generated. Utilize the `pig_ai.save_probabilities` and `pig_ai.load_probabilities` commands to load the AI for different game setups. The AI is not currently optimal.

You can also generate different contour plots relating to the AI with `pig_ai.generate_prob_contour`, which plots the approximate win probability for each pair of scores, and `pig_ai.generate_cutoff_contour`, which plots the number of points one should obtain in a round before holding.

## Usage
Clone this repository, edit the user parameters in `pig.py`, and run `python pig.py` in a terminal.
