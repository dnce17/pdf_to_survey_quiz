import pytest
from main import remove_unrelated

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