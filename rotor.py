"""
"""

from .plotting import plot_rotor
from .analyses.rotordynamics import create_ross_rotor

class Rotor:
    """
    """
    def __init__(self, shaft):
        """
        """
        self.shaft = shaft
        self.impeller = None
        self.bearings = []
        self.shaft_seal = None
        self.shaft_coupling = None

    def addBearing(self, model, segment_id, side, orientation):
        """
        """
        if (segment_id < 0 or segment_id >= len(self.shaft.segments)):
            raise ValueError("Shaft segment does not exist")
        if side not in ["left", "right"]:
            raise ValueError("Bearing side should be 'left' or 'right'")
        if orientation not in ["left", "right"]:
            raise ValueError("Bearing orientation should be 'left' or 'right'")
        if model.d != self.shaft.segments[segment_id]["d"]:
            raise ValueError("Mismatch between shaft diameter and " + \
                             "bearing inner diameter.")

        bearing = dict()
        bearing["segment"]     = segment_id
        bearing["side"]        = side
        bearing["orientation"] = orientation
        bearing["model"]       = model

        offset = 0
        if bearing["side"] == "right":
            offset = self.shaft.segments[segment_id]["l"] - model.B
        bearing["x1"] = self.shaft.segments[segment_id]["x0"] + offset
        bearing["x2"] = bearing["x1"] + model.B

        # bearing load center
        bearing["xc"] = bearing["x1"] + model.a
        if orientation == "left":
            bearing["xc"] = bearing["x2"] - model.a

        self.bearings.append(bearing)

    def addImpeller(self, impeller_data, segment_id, side, orientation):
        """
        """
        if (segment_id < 0 or segment_id >= len(self.shaft.segments)):
            raise ValueError("Shaft segment does not exist")
        if side not in ["left", "right"]:
            raise ValueError("Impeller side should be 'left' or 'right'")
        if orientation not in ["left", "right"]:
            raise ValueError("Impeller orientation should be 'left' or 'right'")
        if impeller_data.ds != self.shaft.segments[segment_id]["d"]:
            raise ValueError("Mismatch between shaft diameter and " + \
                             "impeller bore diameter.")

        impeller = dict()
        impeller["segment"]     = segment_id
        impeller["side"]        = side
        impeller["orientation"] = orientation
        impeller["impeller"]    = impeller_data

        offset = 0
        if impeller["side"] == "right":
            offset = self.shaft.segments[segment_id]["l"] - impeller_data.l
        impeller["x1"] = self.shaft.segments[segment_id]["x0"] + offset
        impeller["x2"] = impeller["x1"] + impeller_data.l

        # impeller center of mass
        impeller["xc"] = impeller["x1"] + impeller_data.com
        if orientation == "right":
            impeller["xc"] = impeller["x2"] - impeller_data.com
        
        impeller["mass"] = impeller_data.mass
        impeller["polar_inertia"] = impeller_data.ip
        impeller["diametral_inertia"] = impeller_data.id

        self.impeller = impeller

    def plotRotor(self, outdir="."):
        """
        """
        plot_rotor(self, outdir)

    def rossRotor(self, element_dx):
        """
        """
        return create_ross_rotor(self, element_dx)
