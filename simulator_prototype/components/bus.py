"""
    Bus instances used as conduits of numerical data of fixed size. Expectation
    is that a bus will be written to by one component but can be read by many
"""

from components.abstract.hooks import OutputHook
from components.abstract.ibus import iBusRead, iBusWrite

class Bus(OutputHook, iBusRead, iBusWrite):
    """

    """

    def __init__(self, name, size, default_value=0):
        "Constructor will cause exception on invalid parameters"
        if not isinstance(name,str) or size <= 0 or default_value < 0 or default_value >= 2**size:
            raise ValueError('Initialization parameters invalid')

        self._name = name
        self._size = size
        self._value = default_value

    def inspect(self):
        "Returns a dictionary message to application caller defining state of bus"
        return { 'name' : self._name, 'type' : 'logic', 'size' : self._size, 'state' : self._value}

    def read(self):
        "Returns last valid value written to bus object"
        return self._value

    def write(self, value):
        "Writes parameter to bus, if out of bus' bounds then exception occurs"
        if value < 0 or value >= 2**self._size:
            raise ValueError('Value out of range for bus')
        self._value = value
