from typing import Callable, Any

from videoanalytics.models import Tracked


class Event:
    def __init__(self, event: Callable, object_kind: str, params: dict[str, Any]) -> None:
        self._check_event = event
        self._object_kind = object_kind
        self._params = params

    def check(self, tracked: Tracked) -> bool:
        if tracked.obj.name != self._object_kind:
            return False
        return self._check_event(tracked, **self._params)
