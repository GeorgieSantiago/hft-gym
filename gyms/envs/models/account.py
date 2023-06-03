from gyms.envs.models.model import Model
from gyms.envs.models.position import Position

BaseAccount = type("BaseAccount", (Model,), {
    'positions': Position
})

class Account(BaseAccount):
    def __init__(self, json: dict):
        super().__init__(json)