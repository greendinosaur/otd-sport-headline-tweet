import random

# helper file to manage emojis to show in a tweet
EXCITEMENT_INDEX = [-3,-2,0,1,2,3,4]
DATA_FILE = "data/emoji.csv" # data file containing emojis
dict_default_values = [[],[],[],[],[],[],[]] 
emoji_dict = dict(zip(EXCITEMENT_INDEX,dict_default_values)) # stores the different emojis mapped to the excitement index


def load_emoji_data(fname=DATA_FILE):
    """
        loads in emoji data from file
        first value in file is the excitement index
        second value in file represents a unicode character of an emoji
    """
    file_in = open(fname, "r")
    for line in file_in:
        emoji_details = line.split(',')
        index = int(emoji_details[0])
        emoji = emoji_details[1].rstrip('\n')
        emoji_dict[index].append(emoji)

    file_in.close()

def get_random_emoji(index):
    """ chooses a random emoji based on the supplied value
        this will be a string
    """
    emoji = "" # return empty string if no value is present
    if index in EXCITEMENT_INDEX and len(emoji_dict[index]) > 0:
        emoji = random.choice(emoji_dict[index])

    return emoji

def generate_emoji(index):
    """ generates an emoji string based on the excitement index
    """
    emoji = get_random_emoji(index)
    return chr(int(emoji,base=16))
