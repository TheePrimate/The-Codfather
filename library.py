import arcade
import random
from constants import *
from numpy.random import choice
import arcade.gui
from arcade.gui import UIManager, UITextureButton
from arcade import uicolor
import math


FISH_LIST = ("Northern Pike", "Cod", "Rainbow Trout",
             "Sockeye Salmon", "Snoek",
             "Marlin", "Bluefin Tuna", "Dumbo Octopus", "Immortal Jellyfish",
             "Ancient Mariner's Albatross", "Naval Bomb")

# Minigame type, Dollars, lower-bound difficulty, higher-bound difficulty, time limit, sprite name, column, count

fish_data = {
    "Northern Pike": ["Fishing Minigame", 100, DIFFICULTY_10, DIFFICULTY_10, 20, "assets/northern_pike.png", 1, 1],
    "Cod": ["Fishing Minigame", 150, DIFFICULTY_7_LOW, DIFFICULTY_9_HIGH, 20, "assets/codfish.png", 1, 1],
    "Rainbow Trout": ["Fishing Minigame", 200, DIFFICULTY_7_LOW, DIFFICULTY_8_HIGH, 20, "assets/rainbow_trout.png", 1, 1],
    "Sockeye Salmon": ["Fishing Minigame", 250, DIFFICULTY_7_LOW, DIFFICULTY_5_HIGH, 20, "assets/sockeye.png", 1, 1],
    "Snoek": ["Fishing Minigame", 1500, DIFFICULTY_6_LOW, DIFFICULTY_5_HIGH, 20, "assets/snoek.png", 1, 1],
    "Marlin": ["Fishing Minigame", 4800, DIFFICULTY_5_LOW, DIFFICULTY_5_HIGH, 20, "assets/marlin.png", 1, 1],
    "Bluefin Tuna": ["Fishing Minigame", 7350, DIFFICULTY_4_LOW, DIFFICULTY_4_HIGH, 20, "assets/bluefin_tuna.png", 1, 1],
    "Dumbo Octopus": ["Fishing Minigame", 99999, DIFFICULTY_1_LOW, DIFFICULTY_3_HIGH, 20, "assets/dumbo_octopus.png", 1, 1],
    "Immortal Jellyfish": ["Fishing Minigame", 0.3, DIFFICULTY_1_LOW, DIFFICULTY_2_HIGH, 20, "assets/immortal_jellyfish.png", 8, 8],
    "Ancient Mariner's Albatross": ["Fishing Minigame", 553000, DIFFICULTY_1_LOW, DIFFICULTY_1_HIGH, 20, "assets/albatross.png", 1, 1],
    "Naval Bomb": ["Naval Bomb Minigame", 10000, None, None, None, "assets/naval_bomb.png", 1, 1]
}
