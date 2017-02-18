"""
model.Record
"""


class Record:
    def __init__(self, **kwargs):
        """
        just make all attributes to NULL.
        """
        self.value = kwargs["value"]
        self.time = kwargs["time"]
        pass

    def __iter__(self):
        yield 'value', self.value
        yield 'time', self.time

    def __str__(self):
        string = "value: " + str(self.value) + ", Time: " + str(self.time)
        return string

    pass
