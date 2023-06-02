class Model(object):
    def __init__(self, json: dict) -> None:
        for key in json.keys():
            setattr(self, key, json[key])