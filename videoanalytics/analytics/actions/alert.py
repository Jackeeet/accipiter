import json
import queue
from datetime import datetime

from logmanager.logmanager import LogManager
from videoanalytics.models import Tracked


def alert(
        message: str, output_queue: queue.Queue, logger: LogManager, tracked: Tracked = None
) -> None:
    alert_obj = json.dumps({"timestamp": datetime.now(), "object": tracked.obj.name, "message": message}, default=str)
    output_queue.put(alert_obj)
    logger.log_alert(alert_obj)
