from ..base.position import Position


class BaseError:
    def __init__(
        self,
        position_start: "Position",
        position_end: "Position",
        name: str,
        details: str,
    ) -> None:
        self.position_start = position_start
        self.position_end = position_end
        self.name = name
        self.details = details

    def as_string(self) -> str:
        result = f"{self.name}: {self.details}\n"
        result += (
            f"File {self.position_start.file_name}, line {self.position_start.line + 1}"
        )
        result += "\n\n" + self.string_with_arrows(
            self.position_start.file_text, self.position_start, self.position_end
        )
        return result

    def string_with_arrows(
        self, text: str, position_start: "Position", position_end: "Position"
    ) -> str:
        result = ""
        index_start = max(text.rfind("\n", 0, position_start.index), 0)
        index_end = text.find("\n", index_start + 1)
        if index_end < 0:
            index_end = len(text)
        line_count = position_end.line - position_start.line + 1
        for i in range(line_count):
            line = text[index_start:index_end]
            col_start = position_start.column if i == 0 else 0
            col_end = position_end.column if i == line_count - 1 else len(line) - 1
            result += line + "\n"
            result += " " * col_start + "^" * (col_end - col_start)
            index_start = index_end
            index_end = text.find("\n", index_start + 1)
            if index_end < 0:
                index_end = len(text)
        return result.rstrip()
