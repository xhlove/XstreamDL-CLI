class MPDItem(object):
    def __init__(self, name: str = "MPDItem"):
        self.name = name
        self.childs = []

    def addattr(self, name: str, value):
        self.__setattr__(name, value)

    def addattrs(self, attrs: dict):
        for attr_name, attr_value in attrs.items():
            attr_name: str
            attr_name = attr_name.replace(":", "_")
            self.addattr(attr_name, attr_value)

    def find(self, name: str):
        return [child for child in self.childs if child.name == name]

    def generate(self):
        pass

    def to_int(self):
        pass