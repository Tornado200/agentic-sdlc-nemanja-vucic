from mars_rover.grid import Grid
from mars_rover.navigation import Rover


def test_rover_be_001_2_s1_four_left_turns_cycle_to_north_and_keep_position():
    # GIVEN the rover is at (2, 2) facing N
    rover = Rover(x=2, y=2, heading="N")

    # WHEN TurnLeft is applied four times
    headings = []
    for _ in range(4):
        rover.turn_left()
        headings.append(rover.heading)

    # THEN the heading cycles N -> W -> S -> E -> N
    assert headings == ["W", "S", "E", "N"]
    # AND the position remains (2, 2) throughout
    assert (rover.x, rover.y) == (2, 2)


def test_rover_be_001_2_s2_four_right_turns_cycle_to_north_and_keep_position():
    # GIVEN the rover is at (2, 2) facing N
    rover = Rover(x=2, y=2, heading="N")

    # WHEN TurnRight is applied four times
    headings = []
    for _ in range(4):
        rover.turn_right()
        headings.append(rover.heading)

    # THEN the heading cycles N -> E -> S -> W -> N
    assert headings == ["E", "S", "W", "N"]
    # AND the position remains (2, 2) throughout
    assert (rover.x, rover.y) == (2, 2)


def test_rover_be_001_2_s3_rotation_never_changes_coordinates():
    # GIVEN a rover at any position and heading
    rover = Rover(x=1, y=3, heading="E")

    # WHEN any L or R operation is applied
    for turn in (rover.turn_left, rover.turn_right, rover.turn_left):
        turn()

    # THEN (x, y) is unchanged and only the heading is updated
    assert (rover.x, rover.y) == (1, 3)
    assert rover.heading == "N"


def test_rover_be_001_3_s1_forward_movement_follows_heading_arithmetic():
    # GIVEN a rover at (1, 2) on a 5x5 grid
    expected = {"N": (1, 3), "S": (1, 1), "E": (2, 2), "W": (0, 2)}

    for heading, position in expected.items():
        rover = Rover(x=1, y=2, heading=heading)

        # WHEN MoveForward is applied facing each heading
        rover.move_forward()

        # THEN the position changes by one unit on the correct axis
        assert (rover.x, rover.y) == position


def test_rover_be_001_3_s2_grid_validation_precedes_state_commit():
    # GIVEN a rover at (0, 2) facing W on a 3x3 grid
    rover = Rover(x=0, y=2, heading="W", grid=Grid(width=3, height=3))

    # WHEN MoveForward would leave the grid
    moved = rover.move_forward()

    # THEN the move is rejected and the state is unchanged
    assert moved is False
    assert (rover.x, rover.y, rover.heading) == (0, 2, "W")


def test_rover_be_001_3_s3_interior_moves_are_always_legal():
    # GIVEN a 5x5 grid with no obstacles and a rover at (2, 2)
    grid = Grid(width=5, height=5)

    for heading, position in {
        "N": (2, 3),
        "S": (2, 1),
        "E": (3, 2),
        "W": (1, 2),
    }.items():
        rover = Rover(x=2, y=2, heading=heading, grid=grid)

        # WHEN MoveForward is applied in any heading
        moved = rover.move_forward()

        # THEN the move is accepted and one axis changes by one unit
        assert moved is True
        assert (rover.x, rover.y) == position
