from model import Model
BasePosition = type("BasePosition", (Model,), {})

class Position(BasePosition):
    def __init__(self, json: dict) -> None:
        super().__init__(json)