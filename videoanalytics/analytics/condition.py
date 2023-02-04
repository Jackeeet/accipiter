from videoanalytics.analytics.actions import Action
from videoanalytics.analytics.interfaces import Evaluable


class Condition:
    def __init__(self, condition: Evaluable, actions: list[Action]) -> None:
        self.condition = condition
        self.actions = actions
