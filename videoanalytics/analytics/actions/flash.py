import queue

from videoanalytics.models import Tracked


def flash(drawable: str, output_queue: queue.Queue, colour: tuple[int, int, int], tracked: Tracked) -> None:
    tracked.event_colour = colour
