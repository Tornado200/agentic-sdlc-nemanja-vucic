"""Command parser for Mars Rover operation sequences."""

TurnLeft = "TurnLeft"
TurnRight = "TurnRight"
MoveForward = "MoveForward"

_COMMAND_MAP = {
    "L": TurnLeft,
    "R": TurnRight,
    "M": MoveForward,
}


def parse_command_string(commands: str) -> list[str]:
    return [_COMMAND_MAP[ch] for ch in commands]
