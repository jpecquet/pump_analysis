"""
"""

import ross as rs
import numpy as np
from operator import itemgetter

def create_ross_rotor(rotor, element_dx):
    """
    Acts as an interface between PyPump and ROSS, automating shaft
    discretization and placement of bearing and disk (mass) elements.
    """
    #rotor_speed = rotor.impeller.design_point.omega

    # set material
    material = rs.Material(name    = rotor.shaft.material.name,
                           rho     = rotor.shaft.material.rho,
                           E       = rotor.shaft.material.e,
                           Poisson = rotor.shaft.material.nu)

    # discretize_shaft
    shaft_elements   = []
    disk_elements    = []
    bearing_elements = []

    node_id = 0
    for i in range(len(rotor.shaft.segments)):
        segment = rotor.shaft.segments[i]
        x_left  = segment["x0"]
        x_right = segment["x0"] + segment["l"]
        special_nodes = []
        for j in range(len(rotor.bearings)):
            bearing = rotor.bearings[j]
            if (x_left < bearing["xc"] < x_right):
                bearing_x = bearing["xc"] - segment["x0"]
                special_nodes.append({"x":     bearing_x,
                                      "index": j,
                                      "kind":  "bearing"})

        if (x_left < rotor.impeller["xc"] < x_right):
            mass_x = rotor.impeller["xc"] - segment["x0"]
            special_nodes.append({"x":     mass_x,
                                  "index": None,
                                  "kind":  "impeller"})
        
        # sort nodes by ascending x location to build subsegments
        special_nodes.sort(key=itemgetter("x"))

        special_nodes.append({"x":     x_right - x_left,
                              "index": None,
                              "kind":  "segment_end"})

        x_ref = 0
        for node in special_nodes:
            sub_length     = node["x"] - x_ref
            x_ref          = node["x"]
            length_ratio   = (sub_length / element_dx)
            length_ratio   = length_ratio.to("dimensionless")
            n_elements     = int(np.ceil(length_ratio))
            element_length = sub_length / n_elements

            for i in range(n_elements):
                shaft_elements.append(
                        rs.ShaftElement(
                            L              = element_length,
                            idl            = 0.0,
                            odl            = segment["d"],
                            material       = material,
                            shear_effects  = True,
                            rotary_inertia = True,
                            gyroscopic     = True
                            )
                        )

            node_id += n_elements
            
            if node["kind"] == "bearing":
                bearing = rotor.bearings[node["index"]]["model"]
                bearing_elements.append(
                        rs.BearingElement(
                            n         = node_id,
                            kxx       = bearing.kxx,
                            kyy       = bearing.kyy,
                            cxx       = bearing.cxx,
                            frequency = bearing.frequency
                            )
                        )

            if node["kind"] == "impeller":
                disk_elements.append(
                        rs.DiskElement(
                            n   = node_id,
                            m   = rotor.impeller["mass"],
                            Ip  = rotor.impeller["polar_inertia"],
                            Id  = rotor.impeller["diametral_inertia"],
                            tag = "Disk"
                            )
                        )

    return rs.Rotor(shaft_elements   = shaft_elements,
                    bearing_elements = bearing_elements,
                    disk_elements    = disk_elements)

