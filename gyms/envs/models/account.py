from model import Model
from position import Position

BaseAccount = type("BaseAccount", (Model,), {
    'positions': Position
})

class Account(BaseAccount):
    def __init__(self, json: dict):
        super().__init__(json)