"""
"""

from .. import ureg

class Shaft:
    """
    """
    def __init__(self, material, segments=[]):
        """
        """
        self.material = material
        self.segments = []

        for segment in segments:
            self.addSegment(segment["diameter"], segment["length"])

    def addSegment(self, diameter, length):
        """
        """
        segment = dict()
        segment["d"] = diameter
        segment["l"] = length
        if len(self.segments) == 0:
            segment["x0"] = 0 * ureg("m")
        else:
            segment["x0"] = sum(segment["l"] for segment in self.segments)

        self.segments.append(segment)


