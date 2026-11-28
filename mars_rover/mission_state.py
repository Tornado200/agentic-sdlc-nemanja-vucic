"""In-memory mission state for the Mars Rover."""

_current_position: tuple[int, int, str] | None = None


def set_current_position(position: tuple[int, int], heading: str) -> None:
    """Store the rover's committed position and heading."""
    global _current_position
    _current_position = (position[0], position[1], heading)


def get_current_position() -> tuple[int, int, str] | None:
    """Return the rover's last committed position and heading."""
    return _current_position
