from videoanalytics.models import Tracked
from videoanalytics.models.tracked_state_helpers import disappeared


def disappears(tracked: Tracked) -> bool:
    return disappeared(tracked)
