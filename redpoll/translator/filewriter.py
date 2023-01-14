from typing import TextIO


class FileWriter:
    _path: str
    _file: TextIO | None

    def __init__(self, file_path: str) -> None:
        # todo implement a file path wrapper or find a library or something
        self._path = file_path
        self._file = None

    def __enter__(self):
        self._file = open(self._path, 'w', encoding="utf8")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()

    def write(self, line: str) -> None:
        self._file.write(line)

    def writeln(self, line: str = "") -> None:
        self._file.write(line)
        self._file.write("\n")
