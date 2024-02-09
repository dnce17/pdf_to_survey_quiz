import pytest
from main import remove_unrelated, combine_frag
from quiz import Quiz

# main.py test
def test_remove_unrelated():
    test_arr = [
        ["filler", "FILLER", "---questions---", "something"],
        ["filler", "  ---questions---  ", "something"],
        ["filler", "FILLER", "filLER", "something"]
    ]
    assert remove_unrelated(test_arr[0]) == test_arr[0][3:]
    assert remove_unrelated(test_arr[1]) == test_arr[1][2:]

    with pytest.raises(SystemExit) as error:
       remove_unrelated(test_arr[2])
    assert error.type == SystemExit  

def test_combine_frag():
    test_arr = [
        ["• How are you?", "o Good", "▪ Positive"],
        ["• I am going to go", "home to sleep", "but brush first", "o Good,", "happy to hear that", "▪ Positive", "I say"],
        ["• I will", "open the door"],
        ["• I will", "oh oh open the door"],
        ["• edge case o", "~o o o o on new line"],
    ]
    assert combine_frag(test_arr[0]) == ["• How are you?", "o Good", "▪ Positive"]
    assert combine_frag(test_arr[1]) == [
        "• I am going to go home to sleep but brush first", "o Good, happy to hear that", "▪ Positive I say",
    ]
    assert combine_frag(test_arr[2]) == ["• I will open the door"]
    assert combine_frag(test_arr[3]) == ["• I will oh oh open the door"]
    assert combine_frag(test_arr[4]) == ["• edge case o o o o o on new line"]

# quiz.py test
@pytest.fixture
def q():
    return Quiz()

def test_valid_ans(q):
    total_choices = 5
    assert q._validate_ans("1", total_choices) == True
    assert q._validate_ans("5", total_choices) == True
    assert q._validate_ans("3", total_choices) == True
    assert q._validate_ans("   3   ", total_choices) == True

def test_invalid_ans(q):
    total_choices = 8
    tests = ["-5", "0", "9", "15", "3.5", "9.0", "bob", "@#", "", "   ", "   3    p", "p    3"]
    for t in tests:
        assert q._validate_ans(t, total_choices) == False