"""Heading rotation for the Mars Rover."""

HEADINGS = ["N", "E", "S", "W"]


def turn_left(heading: str) -> str:
    return HEADINGS[(HEADINGS.index(heading) - 1) % 4]


def turn_right(heading: str) -> str:
    return HEADINGS[(HEADINGS.index(heading) + 1) % 4]
