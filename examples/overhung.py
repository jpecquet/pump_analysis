"""
"""

from .. import ureg
from ..fluids import liquid_oxygen
from ..materials import steel_304l
from ..parts.impeller import ImpellerBarske
from ..parts.bearing import Bearing
from ..parts.shaft import Shaft
from ..rotor import Rotor
from .. import DesignPoint

bearing_large = Bearing(name                = "BearingLarge",
                        bore_diameter       = 12.0 * ureg("mm"),
                        outer_diameter      = 32.0 * ureg("mm"),
                        width               = 10.0 * ureg("mm"),
                        load_center         = 7.9  * ureg("mm"),
                        contact_angle       = 15.0 * ureg("deg"),
                        factor              = 12.5,
                        static_load_rating  = 3.85 * ureg("kilonewton"),
                        dynamic_load_rating = 7.90 * ureg("kilonewton"),
                        kxx = [1e7], 
                        kyy = [1e7],
                        cxx = [1e4],
                        frequency = None)

design_point = DesignPoint(fluid =            liquid_oxygen,
                           mass_flowrate =    1.3 * ureg("kg/s"),
                           pressure_rise =    600.0 * ureg("psi"),
                           rotational_speed = 30000. * ureg("rpm"))

impeller = ImpellerBarske(design_point =                   design_point,
                          diameter_inlet =                 1.1 * ureg("inch"),
                          diameter_hub =                   16 * ureg("mm"),
                          diameter_shaft =                 10 * ureg("mm"),
                          flow_coefficient_suction =       0.06,
                          blockage_coefficient_suction =   0.8,
                          head_recovery_coefficient =      0.35,
                          blockage_coefficient_discharge = 0.92,
                          blade_count =                    6,
                          material =                       steel_304l,
                          length_hub =                     15 * ureg("mm"),
                          through_shaft =                  False)
shaft_segments = [
        {"diameter": 10.0 * ureg("mm"),  "length": 14.0 * ureg("mm")},
        {"diameter": 11.0 * ureg("mm"), "length": 20.0 * ureg("mm")},
        {"diameter": 12.0 * ureg("mm"), "length": 10.0 * ureg("mm")},
        {"diameter": 16.0 * ureg("mm"), "length": 20.0 * ureg("mm")},
        {"diameter": 12.0 * ureg("mm"), "length": 12.0 * ureg("mm")},
        {"diameter": 10.0 * ureg("mm"), "length": 12.0 * ureg("mm")},
    ]

shaft = Shaft(material = steel_304l,
              segments = shaft_segments)

rotor = Rotor(shaft)

rotor.addBearing(model       = bearing_large,
                 segment_id  = 2,
                 side        = "right",
                 orientation = "right")

rotor.addBearing(model       = bearing_large,
                 segment_id  = 4,
                 side        = "left",
                 orientation = "left")

rotor.addImpeller(impeller_data = impeller,
                  segment_id    = 0,
                  side          = "right",
                  orientation   = "left")
