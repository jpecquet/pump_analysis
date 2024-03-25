"""
"""

from .. import ureg

class Fluid:
    def __init__(self, name, density, vapor_pressure, viscosity):
        """
        """
        self.name = name
        self.rho  = density
        self.pv   = vapor_pressure
        self.mu   = viscosity

liquid_oxygen = Fluid(name           = "LOX",
                      density        = 1140.0 * ureg("kg/m**3"),
                      vapor_pressure = 1.0 * ureg("atm"),
                      viscosity      = 1.7e-7 * ureg("newton*s/m**2"))
