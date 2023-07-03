class SymbolTable:
    def __init__(self) -> None:
        self.table = {}
        self.parent = None

    def get(self, name: str) -> "SymbolTable":
        value = self.table.get(name, None)
        if value is None and self.parent:
            return self.parent.get(name)
        return value

    def set(self, name: str, value: any) -> None:
        self.table[name] = value

    def remove(self, name: str) -> None:
        del self.table[name]
