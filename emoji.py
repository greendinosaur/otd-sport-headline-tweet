""" helper file to manage emojis to show in a tweet
"""
import random

EXCITEMENT_INDEX = [-3, -2, 0, 1, 2, 3, 4]
DATA_FILE = "data/emoji.csv"  # data file containing emojis
DICT_DEFAULT_VALUES = [[], [], [], [], [], [], []]
# stores the different emojis mapped to the excitement index
emoji_dict = dict(zip(EXCITEMENT_INDEX, DICT_DEFAULT_VALUES))


def empty_emoji_dict():
    """ empties out the values inside the emoji_dict
    """
    global emoji_dict
    for key in emoji_dict.keys():
        emoji_dict[key] = []


def load_emoji_data(fname=DATA_FILE):
    """
        loads in emoji data from file
        first value in file is the excitement index
        second value in file represents a unicode character of an emoji

        fname - the name of the file, if not provided defaults to DATA_FILE
    """
    global emoji_dict
    empty_emoji_dict()

    file_in = open(fname, "r")
    for line in file_in:
        emoji_details = line.split(',')
        index = int(emoji_details[0])
        emoji = emoji_details[1].rstrip('\n')
        emoji_dict[index].append(emoji)

    file_in.close()


def get_random_emoji(index):
    """ chooses a random emoji based on the supplied value
        ensure the data has been loaded prior to calling this function

        index - the index to look up
        returns a string representing the emoji unicode character
    """
    global emoji_dict
    emoji = ""  # return empty string if no value is present
    if index in EXCITEMENT_INDEX and len(emoji_dict[index]) > 0:
        emoji = random.choice(emoji_dict[index])

    return emoji


def generate_emoji(index):
    """ generates an emoji string based on the provided index

        index - the index to lookup and randomly select an appropriate emoji
    """
    emoji = get_random_emoji(index)
    return chr(int(emoji, base=16))
