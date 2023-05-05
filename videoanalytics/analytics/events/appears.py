from videoanalytics.models import Tracked, TrackedState


def appears(tracked: Tracked) -> bool:
    # первым ключом в словаре состояний всегда является обьект сцены, его нужно достать
    scene = next(iter(tracked.states))
    return (tracked.states[scene] & TrackedState.NEW) == TrackedState.NEW
