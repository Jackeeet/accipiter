from videoanalytics.models import Tracked


def set_colour(colour: tuple[int, int, int], tracked: Tracked) -> None:
    tracked.obj.colour = colour
