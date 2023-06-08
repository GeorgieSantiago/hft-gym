from gym.envs.models.model import Model
BasePosition = type("BasePosition", (Model,), {})

class Position(BasePosition):
    symbol: str
    count: int
    def __init__(self, json: dict) -> None:
        super().__init__(json)