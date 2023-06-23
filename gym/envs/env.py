class Env(object):
    KEY: str
    SECRET: str
    def __init__(self) -> None:
        super().__init__()
        with open("alpaca.txt") as env_file:
            for line in env_file:
                name, val = line.partition("=")[::2]
                setattr(self, name.strip(), str(val.strip()))
env = Env()