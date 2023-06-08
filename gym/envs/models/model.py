from decimal import Decimal


class Model(object):
    json: dict
    def __init__(self, json: dict) -> None:
        for key in json.keys():
            setattr(self, key, json[key])
            self.json = json
    def to_array(self, fields: list = None) -> list:
        attrs = list()
        if fields == None:
            fields = self.json.keys()
        for field in fields:
            if field in self.json.keys():
                val = getattr(self, field)
                if type(val) == float:
                    val = round(val, 2)
                attrs.append(val)
        return attrs
