from videoanalytics.analytics.declarable.actions import Action
from videoanalytics.analytics.declarable.interfaces import Evaluable


class Condition:
    def __init__(self, condition: Evaluable, actions: list[Action]) -> None:
        self.condition = condition
        self.actions = actions
