"""
"""

from .. import ureg
from .. import display_units
import numpy as np

class ImpellerBarske:
    def __init__(self, design_point,
                 diameter_inlet, diameter_hub, diameter_shaft,
                 flow_coefficient_suction, blockage_coefficient_suction,
                 head_recovery_coefficient, blockage_coefficient_discharge,
                 blade_count, material, length_hub, through_shaft):
        """
        """
        self.design_point  = design_point
        self.material      = material
        self.through_shaft = through_shaft

        self.d0  = diameter_inlet
        self.dh  = diameter_hub
        self.ds  = diameter_shaft
        self.phi = flow_coefficient_suction
        self.psi = head_recovery_coefficient
        self.kb1 = blockage_coefficient_suction
        self.kb2 = blockage_coefficient_discharge
        self.z   = blade_count
        self.l   = length_hub

        self.compute_head()
        self.compute_volume_flowrate()
        self.compute_dimensions_suction()
        self.compute_dimensions_discharge()
        self.compute_blade_thickness()
        self.format_units()
        self.compute_mass_and_inertia()

    def compute_head(self):
        """
        """
        density = self.design_point.fluid.rho
        delta_p = self.design_point.dp
        self.h  = delta_p / (density * ureg("g_n"))

    def compute_volume_flowrate(self):
        """
        """
        density = self.design_point.fluid.rho
        mdot    = self.design_point.mdot
        self.q  = mdot / density

    def compute_dimensions_suction(self):
        """
        """
        self.cm = self.q / (np.pi/4 * self.d0**2)
        if self.through_shaft:
            self.cm = self.q / (np.pi/4 * (self.d0**2 - self.ds**2))
        self.u1 = self.cm / self.phi
        self.d1 = 2*self.u1 / self.design_point.omega
        self.b1 = self.q / (np.pi * self.d1 * self.cm * self.kb1)

    def compute_dimensions_discharge(self):
        """
        """
        self.u2 = (1. / (1 + self.psi) *
                   np.sqrt((self.u1**2 + 2 * ureg("g_n") * self.h)))
        self.d2 = 2*self.u2 / self.design_point.omega
        self.b2 = self.q / (np.pi * self.d2 * self.cm * self.kb2)

    def compute_blade_thickness(self):
        """
        """
        self.t1 = np.pi * self.d1 * (1 - self.kb1) / self.z
        self.t2 = np.pi * self.d2 * (1 - self.kb2) / self.z

    def compute_mass_and_inertia(self):
        """
        """
        hub_volume   = self.l * (np.pi/4 * (self.dh**2 - self.ds**2))
        hub_mass     = self.material.rho * hub_volume
        hub_com_x    = self.l/2
        blade_volume = (self.b1 + self.b2)/2 * (self.t1 + self.t2)/2 * \
                       (self.d2 - self.d1)/2 # approximate
        blade_mass   = self.material.rho * blade_volume
        blade_com_y  = self.d2/2 + (self.d2/2 - self.d1/2) * (self.b2
                       + 2*self.b1) / 3 / (self.b1 + self.b2)
        fact = (blade_com_y - self.d1/2) / (self.d2/2 - self.d1/2)
        blade_com_x  = - (self.b1 - self.b2) + self.b1/2 * (1 - fact) \
                       + self.b2/2 * fact

        self.mass = hub_mass + self.z*blade_mass
        self.com  = (hub_com_x*hub_mass + blade_com_x*blade_mass*self.z) \
                    / self.mass
        
        self.ip = hub_mass/2 * ((self.d2/2)**2 - (self.d1/2)**2)
        self.ip += self.z * (1/12 * blade_mass * ((self.d2 - self.d1)/2)**2
                             + blade_mass * blade_com_y**2)

        # big approximation (placeholder)
        self.id = self.ip / 2

    def format_units(self):
        """
        """
        self.h.ito(display_units["head"])
        self.q.ito(display_units["volume_flow"])
        self.cm.ito(display_units["velocity"])
        self.u1.ito(display_units["velocity"])
        self.u2.ito(display_units["velocity"])
        self.ds.ito(display_units["length"])
        self.dh.ito(display_units["length"])
        self.d0.ito(display_units["length"])
        self.d1.ito(display_units["length"])
        self.d2.ito(display_units["length"])
        self.b1.ito(display_units["length"])
        self.b2.ito(display_units["length"])
        self.l.ito(display_units["length"])

    def print(self):
        """
        """
        self.format_units()
        data =   "Impeller Results\n"
        data +=  "================\n\n"
        data +=  "  Design Point  \n"
        data +=  "----------------\n"
        data += f"H:  {self.h:~.2f}\n"
        data += f"Q:  {self.q:~.4f}\n"
        data +=  "----------------\n"
        data +=  "   Velocities   \n"
        data +=  "----------------\n"
        data += f"Cm: {self.cm:~.2f}\n"
        data += f"U1: {self.u1:~.2f}\n"
        data += f"U2: {self.u2:~.2f}\n"
        data +=  "-----------------\n"
        data +=  "   Dimensions    \n"
        data +=  "-----------------\n"
        data += f"D0: {self.d0:~.2f}\n"
        data += f"D1: {self.d1:~.2f}\n"
        data += f"D2: {self.d2:~.2f}\n"
        data += f"b1: {self.b1:~.2f}\n"
        data += f"b2: {self.b2:~.2f}\n"

        print(data)
