from videoanalytics.analytics.tools import Area
from videoanalytics.models import Tracked


def enters(tracked: Tracked, area: Area) -> bool:
    return area.contains(tracked.obj.box)
    pass
