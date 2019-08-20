from . import strings


class Expression:
    def __init__(self):
        self.cache = list()

    def field(self, v):
        self.cache.append(v)

    def operator(self, v):
        self.cache.append(v)

    def value(self, v):
        v = strings.get_sql_str(v)
        self.cache.append(v)

    def __str__(self):
        return " ".join(self.cache)
