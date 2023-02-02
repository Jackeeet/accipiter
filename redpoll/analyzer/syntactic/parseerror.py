from redpoll.analyzer.token import Token


class ParseError(Exception):
    def __init__(self, token: Token, message: str) -> None:
        self.token = token
        self.message = f"[{token.line}:{token.position}] {message}"
        super().__init__(self.message)
