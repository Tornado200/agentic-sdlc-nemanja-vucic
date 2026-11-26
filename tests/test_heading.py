from mars_rover.heading import turn_left, turn_right


def test_turn_left_from_north_faces_west():
    assert turn_left("N") == "W"


def test_turn_right_from_north_faces_east():
    assert turn_right("N") == "E"


def test_four_left_turns_return_to_start():
    heading = "N"
    for _ in range(4):
        heading = turn_left(heading)
    assert heading == "N"
