from videoanalytics.models import Tracked


def flash(drawable: str, colour: tuple[int, int, int], tracked: Tracked) -> None:
    tracked.obj.colour = colour
