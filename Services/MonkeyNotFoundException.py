class MonkeyNotFoundException(Exception):
    def __init__(self, monkey_name: str):
        self.monkey_name = monkey_name
        super().__init__(f"Monkey '{monkey_name}' not found")