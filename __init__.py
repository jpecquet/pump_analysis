"""
Set up unit registry (see https://pint.readthedocs.io/en/stable/).
Define display units (U.S. / S.I.).
"""

from pint import UnitRegistry

ureg = UnitRegistry()

display_units = {}

def set_display_units(unit_system):
    """
    """
    if unit_system == "freedom":
        display_units["length"]      = ureg("inch")
        display_units["head"]        = ureg("feet")
        display_units["pressure"]    = ureg("psi")
        display_units["temperature"] = ureg("degF")
        display_units["velocity"]    = ureg.parse_units("ft/s")
        display_units["mass_flow"]   = ureg.parse_units("lb/s")
        display_units["volume_flow"] = ureg.parse_units("gal/min")
    elif unit_system == "metric":
        display_units["length"]      = ureg("mm")
        display_units["head"]        = 1 * ureg("m")
        display_units["pressure"]    = ureg("bar")
        display_units["temperature"] = ureg("kelvin")
        display_units["velocity"]    = ureg.parse_units("m/s")
        display_units["mass_flow"]   = ureg.parse_units("kg/s")
        display_units["volume_flow"] = ureg.parse_units("litre/s")
    return None

set_display_units("metric")

class DesignPoint:
    def __init__(self, fluid, pressure_rise, mass_flowrate, rotational_speed):
        self.fluid = fluid
        self.dp    = pressure_rise
        self.mdot  = mass_flowrate
        self.omega = rotational_speed

from . import plotting
from . import parts
from . import fluids
from . import materials
from . import analyses
from . import rotor

from . import examples
