from videoanalytics.analytics.actions import Action
from videoanalytics.interfaces.evaluable import Evaluable
from videoanalytics.models import EvalTree


class Condition:
    def __init__(
            self, condition: Evaluable | EvalTree, actions: list[Action]
    ) -> None:
        self.condition = condition
        self.actions = actions
