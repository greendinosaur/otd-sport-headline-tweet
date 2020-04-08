import pytest
import emoji

def test_get_random_emoji_invalidindex():
    assert emoji.get_random_emoji(5) == ""

def test_get_random_emoji_emptyindex():
    assert emoji.get_random_emoji(3) == ""

def test_get_random_emoji_withdata():
    emoji.emoji_dict[3].append("1F615")
    assert emoji.get_random_emoji(3) == "1F615"
    emoji.emoji_dict[3].clear() # reset the dictionary

def test_load_emoji_data():
    emoji.load_emoji_data("tests/test_emoji.csv")
    assert len(emoji.emoji_dict[-3]) == 4
    assert len(emoji.emoji_dict[-2]) == 6
    assert len(emoji.emoji_dict[0]) == 1
    assert len(emoji.emoji_dict[1]) == 2
    assert len(emoji.emoji_dict[2]) == 3
    assert len(emoji.emoji_dict[3]) == 4
    
    assert "1F632" in emoji.emoji_dict[-3]
    assert "1F644" in emoji.emoji_dict[-2]
    assert "1F636" in emoji.emoji_dict[0]
    assert "1F610" in emoji.emoji_dict[1]
    assert "1F600" in emoji.emoji_dict[2]
    assert "1F601" in emoji.emoji_dict[3]



