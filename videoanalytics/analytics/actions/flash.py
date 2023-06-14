import queue

from logmanager.logmanager import LogManager
from videoanalytics.models import Tracked


def flash(drawable: str, output_queue: queue.Queue,  logger: LogManager, colour: tuple[int, int, int], tracked: Tracked) -> None:
    tracked.event_colour = colour
