from otd import emoji


def test_empty_emoji_dict():
    my_emoji = emoji.Emoji("tests/test_emoji.csv")
    assert my_emoji.emoji_dict is not None
    my_emoji.empty_emoji_dict()
    assert len(my_emoji.emoji_dict) == len(emoji.EXCITEMENT_INDEX)
    assert my_emoji.emoji_dict[0] == []


def test_get_random_emoji_invalidindex():
    my_emoji = emoji.Emoji("tests/test_emoji.csv")
    assert my_emoji.get_random_emoji(5) == ""


def test_get_random_emoji_withdata():
    my_emoji = emoji.Emoji("tests/test_emoji.csv")
    assert my_emoji.get_random_emoji(0) == "1F636"


def test_load_emoji_data():
    my_emoji = emoji.Emoji("tests/test_emoji.csv")
    assert len(my_emoji.emoji_dict[-3]) == 4
    assert len(my_emoji.emoji_dict[-2]) == 6
    assert len(my_emoji.emoji_dict[0]) == 1
    assert len(my_emoji.emoji_dict[1]) == 2
    assert len(my_emoji.emoji_dict[2]) == 3
    assert len(my_emoji.emoji_dict[3]) == 4
    assert "1F632" in my_emoji.emoji_dict[-3]
    assert "1F644" in my_emoji.emoji_dict[-2]
    assert "1F636" in my_emoji.emoji_dict[0]
    assert "1F610" in my_emoji.emoji_dict[1]
    assert "1F600" in my_emoji.emoji_dict[2]
    assert "1F601" in my_emoji.emoji_dict[3]
