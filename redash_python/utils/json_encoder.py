from json import JSONEncoder


class ModelEncoder(JSONEncoder):
    """Simple JSON encoder that converts model objects to dicts."""

    def default(self, o):
        return o.__dict__
