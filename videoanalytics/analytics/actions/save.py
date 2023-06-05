import queue

from videoanalytics.models import Tracked


def save(tracked: Tracked, output_queue: queue.Queue,) -> None:
    print(f"saving: {tracked.obj.name} ({tracked.obj.box})")
