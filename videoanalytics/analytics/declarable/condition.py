from .actions import Action
from .events import BinaryEventChain


class Condition:
    def __init__(self, condition: BinaryEventChain, actions: list[Action]) -> None:
        self.condition = condition
        self.actions = actions
