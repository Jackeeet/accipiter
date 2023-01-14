from .tokenerror import TokenError
from .tokenkind import TokenKind


class Token:
    def __init__(self, kind: TokenKind, value: str, line: int, pos: int) -> None:
        self.kind = kind
        self.value = value
        self.line = line
        self.position = pos

    def __repr__(self) -> str:
        return f"Token({self.kind}, {self.value}, {self.line}, {self.position})"

    def __eq__(self, other):
        if isinstance(other, Token):
            return self.kind == other.kind and self.value == other.value \
                   and self.line == other.line and self.position == other.position
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    @staticmethod
    def check_raise_if_non_kinds(token, kinds: set[TokenKind]) -> None:
        if token.kind not in kinds:
            raise TokenError()
