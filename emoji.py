import random

# helper file to manage emojis to show in a tweet
excitement_index = [-3,-2,0,1,2,3]
dict_default_values = [[],[],[],[],[],[]] 
emoji_dict = dict(zip(excitement_index,dict_default_values)) # stores the different emojis mapped to the excitement index


def load_emoji_data(fname):
    # loads in emoji data from file
    # first value is the excitement index
    # second value represents a unicode character of an emoji
    file_in = open(fname, "r")
    for line in file_in:
        emoji_details = line.split(',')
        index = int(emoji_details[0])
        emoji = emoji_details[1].rstrip('\n')
        emoji_dict[index].append(emoji)

    file_in.close()

def get_random_emoji(index):
    # chooses a random emoji based on the supplied value
    # this will be a string
    emoji = "" # return empty string if no value is present
    if index in excitement_index and len(emoji_dict[index]) > 0:
        emoji = random.choice(emoji_dict[index])

    return emoji