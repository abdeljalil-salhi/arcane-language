class Context:
    def __init__(
        self,
        display_name: str,
        parent: "Context" = None,
        parent_entry_position: int = None,
    ) -> None:
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_position = parent_entry_position
        self.symbol_table = None
