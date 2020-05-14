""" helper file to manage emojis to show in a tweet
"""
import random

EXCITEMENT_INDEX = [-3, -2, 0, 1, 2, 3, 4]
DATA_FILE = "data/emoji.csv"  # data file containing emojis
DICT_DEFAULT_VALUES = [[], [], [], [], [], [], []]

class Emoji:

    def __init__(self, data_file=DATA_FILE):
        self.emoji_dict = dict(zip(EXCITEMENT_INDEX, DICT_DEFAULT_VALUES))
        self.fname = data_file
        self.load_emoji_data()

    def empty_emoji_dict(self):
        """ empties out the values inside the emoji_dict
        """
        for key in self.emoji_dict.keys():
            self.emoji_dict[key] = []

    def load_emoji_data(self):
        """
        loads in emoji data from file
        first value in file is the excitement index
        second value in file represents a unicode character of an emoji

        fname - the name of the file, if not provided defaults to DATA_FILE
        """
        self.empty_emoji_dict()

        file_in = open(self.fname, "r")
        for line in file_in:
            emoji_details = line.split(',')
            index = int(emoji_details[0])
            emoji_code = emoji_details[1].rstrip('\n')
            self.emoji_dict[index].append(emoji_code)

        file_in.close()

    def get_random_emoji(self, index):
        """ chooses a random emoji based on the supplied value
            ensure the data has been loaded prior to calling this function

            index - the index to look up
            returns a string representing the emoji unicode character
        """
        emoji_code = ""  # return empty string if no value is present
        if index in EXCITEMENT_INDEX and self.emoji_dict[index]:
            emoji_code = random.choice(self.emoji_dict[index])

        return emoji_code

    def generate_emoji(self, index):
        """ generates an emoji string based on the provided index

        index - the index to lookup and randomly select an appropriate emoji
        """
        emoji_code = self.get_random_emoji(index)
        return chr(int(emoji_code, base=16))
