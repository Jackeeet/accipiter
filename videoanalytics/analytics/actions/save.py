import queue
from datetime import datetime

from logmanager.logmanager import LogManager
from videoanalytics.models import Tracked


def save(tracked: Tracked, output_queue: queue.Queue, logger: LogManager) -> None:
    logger.log_event(f"[{datetime.now()}] класс объекта: {tracked.obj.name}")