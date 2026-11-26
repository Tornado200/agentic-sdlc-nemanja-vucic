from mars_rover.command_parser import (
    MoveForward,
    TurnLeft,
    TurnRight,
    parse_command_string,
)


def test_rover_be_001_1_s1_mixed_valid_sequence_maps_to_operations_in_order():
    # GIVEN
    commands = "LMLMLMLMM"

    # WHEN
    result = parse_command_string(commands)

    # THEN
    assert result == [
        TurnLeft,
        MoveForward,
        TurnLeft,
        MoveForward,
        TurnLeft,
        MoveForward,
        TurnLeft,
        MoveForward,
        MoveForward,
    ]


def test_rover_be_001_1_s2_single_character_sequences_map_correctly():
    # GIVEN
    inputs = {"L": [TurnLeft], "R": [TurnRight], "M": [MoveForward]}

    # WHEN
    results = {commands: parse_command_string(commands) for commands in inputs}

    # THEN
    assert results == inputs
