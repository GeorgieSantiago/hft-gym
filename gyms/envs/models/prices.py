from gyms.envs.models.model import Model

BasePrice = type("BasePrice", (Model,), {
    'open': None,
    'high': None,
    'low': None,
    'close': None
})

class Price(BasePrice):
    def __init__(self, json: dict) -> None:
        super().__init__(json)