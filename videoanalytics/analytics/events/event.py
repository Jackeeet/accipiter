from typing import Callable, Any

from videoanalytics.analytics.interfaces import Evaluable
from videoanalytics.models import Tracked


class Event(Evaluable):
    def __init__(self, event: Callable, object_kind: str, params: dict[str, Any]) -> None:
        self._check_event = event
        self._object_kind = object_kind
        self._params = params

    def evaluate(self, **values) -> bool:
        if 'tracked' not in values:
            raise ValueError()  # todo add message
        tracked: Tracked = values['tracked']
        if tracked.obj.name != self._object_kind:
            return False
        return self._check_event(tracked, **self._params)
