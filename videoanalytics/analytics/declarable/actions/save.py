from videoanalytics.models import Tracked


def save(tracked: Tracked) -> None:
    print(f"saving: {tracked.obj.name} ({tracked.obj.box})")
