import pytest
from main import check_argv_len, confirm_name, remove_unrelated, combine_frag
from quiz import Quiz, Quizzee

# main.py test
def test_check_argv_len():
    valid_tests = [
        ["main.py", "path_to_file.pdf"],
        ["main.py", "path_to_file.pdf", "csv_file.csv"] 
    ]
    invalid_tests = [
        ["main.py"],
        ["main.py", "path_to_file.pdf", "csv_file.csv", "filler"]
    ]

    for test in valid_tests:
        assert check_argv_len(test) is not False
    for test in invalid_tests:
        assert check_argv_len(test) == False

def test_confirm_name(monkeypatch):
    for test in ["y", "yes", "  y ", " yES"]:
        monkeypatch.setattr('builtins.input', lambda _: test)
        assert confirm_name("some name") == True

    for test in ["n", "no", "  N ", "nO  "]:
        monkeypatch.setattr('builtins.input', lambda _: test)
        assert confirm_name("some name") == False

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

@pytest.fixture
def q():
    user = Quizzee()
    quiz = Quiz("test/test_files/test.json", user)
    return [quiz, user]

def test_valid_ans(q):
    q = q[0]
    total_choices = 5
    assert q._validate_ans("1", total_choices) == True
    assert q._validate_ans("5", total_choices) == True
    assert q._validate_ans("3", total_choices) == True
    assert q._validate_ans("   3   ", total_choices) == True

def test_invalid_ans(q):
    total_choices = 8
    tests = ["-5", "0", "9", "15", "3.5", "9.0", "bob", "@#", "", "   ", "   3    p", "p    3"]
    for t in tests:
        assert q[0]._validate_ans(t, total_choices) == False

def test_get_max_traits_total(q):
    desired_results = {"high risk": 3, "low risk": 2, "moderate risk": 3, "no risk": 3, "filler 1 2 5   fill3r": 1}
    assert q[0].get_max_traits_total() == dict(sorted(desired_results.items()))

def test_traits_to_track(q):
    q[1].traits_to_track(q[0].get_all_traits())
    assert vars(q[1]) == {"_high_risk": 0, "_low_risk": 0, "_moderate_risk": 0, "_no_risk": 0, "_filler_1_2_5___fill3r": 0}

def test_add_trait_pts(q):
    tests = [
        "high risk",
        "moderate risk",
        "   hiGH riSk   ",
        " lOw Risk",
        "no risk",
        " LOW RISK",
        "   filler 1 2 5   fill3r    ",
        " LoW RISK "
    ]
    q[1].traits_to_track(q[0].get_all_traits())
    q[1]._add_trait_pts(*tests)
    assert vars(q[1]) == {"_high_risk": 2, "_low_risk": 3, "_moderate_risk": 1, "_no_risk": 1, "_filler_1_2_5___fill3r": 1}