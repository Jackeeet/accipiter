from videoanalytics.models import Tracked


def disappears(tracked: Tracked) -> bool:
    # первым ключом в словаре состояний всегда является обьект сцены, его нужно достать
    # scene = next(iter(tracked.states))
    pass

