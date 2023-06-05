import json
import queue
from datetime import datetime

from videoanalytics.models import Tracked


def alert(message: str, output_queue: queue.Queue, tracked: Tracked = None) -> None:
    output_queue.put(json.dumps(
        {
            "timestamp": datetime.now(),
            "object": tracked.obj.name,
            "message": message
        },
        default=str
    ))
    print(json.dumps(
        {
            "timestamp": datetime.now(),
            "object": tracked.obj.name,
            "message": message
        },
        default=str
    ))
