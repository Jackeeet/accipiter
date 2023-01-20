from videoanalytics.analytics.declarable.events import EventChain
from videoanalytics.analytics.declarable.actions import Action


class Condition:
    def __init__(self, condition: EventChain, actions: list[Action]) -> None:
        self.condition = condition
        self.actions = actions
