"""
"""

from .. import ureg

class Material:
    """
    """
    def __init__(self, name, density, modulus, poisson):
        """
        """
        self.name = name
        self.rho  = density
        self.e    = modulus
        self.nu   = poisson

steel_304l = Material(name = "Steel_304L",
                      density = 7830.0 * ureg("kg/m**3"),
                      modulus = 28.0e6 * ureg("psi"),
                      poisson = 0.3)
