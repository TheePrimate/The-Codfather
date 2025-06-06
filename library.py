import arcade
import random
from constants import *
from numpy.random import choice

# Dollars, lower-bound difficulty, higher-bound difficulty, time limit, sprite name, column, count

fish_data = {
    "Northern Pike": [100, DIFFICULTY_1_LOW, DIFFICULTY_1_HIGH, 20, "assets/northern_pike.png", 1, 1],
    "Cod": [150, DIFFICULTY_1_LOW, DIFFICULTY_2_HIGH, 20, "assets/cod.png", 1, 1],
    "Rainbow Trout": [200, DIFFICULTY_1_LOW, DIFFICULTY_3_HIGH, 20, "assets/rainbow_trout.png", 1, 1],
    "Sockeye Salmon": [250, DIFFICULTY_4_LOW, DIFFICULTY_4_HIGH, 20, "assets/sockeye.png", 1, 1],
    "Snoek": [1500, DIFFICULTY_5_LOW, DIFFICULTY_5_HIGH, 20, "assets/snoek.png", 1, 1],
    "Marlin": [4800, DIFFICULTY_6_LOW, DIFFICULTY_5_HIGH, 20, "assets/marlin.png", 1, 1],
    "Bluefin Tuna": [7350, DIFFICULTY_7_LOW, DIFFICULTY_5_HIGH, 20, "assets/bluefin_tuna.png", 1, 1],
    "Dumbo Octopus": [99999, DIFFICULTY_7_LOW, DIFFICULTY_8_HIGH, 20, "assets/dumbo_octopus.png", 1, 1],
    "Immortal Jellyfish": [0.3, DIFFICULTY_7_LOW, DIFFICULTY_9_HIGH, 20, "assets/immortal_jellyfish.png", 8, 8],
    "Ancient Mariner's Albatross": [553000, DIFFICULTY_10, DIFFICULTY_10, 20, "assets/albatross.png", 1, 1],
    "Naval Bomb": [10000, DIFFICULTY_5_LOW, DIFFICULTY_5_HIGH, 20, "assets/naval_mine.png", 1, 1]
}
