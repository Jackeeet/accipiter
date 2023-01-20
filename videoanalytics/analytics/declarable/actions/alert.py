from videoanalytics.models import Tracked


def alert(message: str, tracked: Tracked = None) -> None:
    print(f"alert: {message}")
