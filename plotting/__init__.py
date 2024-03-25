"""
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os.path

mpl.rcParams["font.family"] = ["sans-serif"]
mpl.rcParams["font.sans-serif"] = ["IBM Plex Mono"]

plt.style.use("dark_background")

def array(quantity_list, unit):
    """
    Homogenizes units within list of quantities.
    Returns array of magnitudes expressed in common unit.
    """
    array_mag = []
    for quantity in quantity_list:
        array_mag.append(quantity.to(unit).magnitude)

    return np.array(array_mag)

def plot_impeller(impeller, outdir):
    """
    """
    impeller.format_units()
    length_unit = impeller.d2.units
    length = impeller.l + (impeller.b1 - impeller.b2)
    width  = impeller.d2
    aspect_ratio = (length / width).to("dimensionless").magnitude
    fig_height   = 3
    plt.figure(figsize=(aspect_ratio*fig_height, fig_height))

    impeller_x = array([0 * length_unit,
                        0 * length_unit,
                        -(impeller.b1 - impeller.b2),
                        0 * length_unit,
                        impeller.b2,
                        impeller.b2,
                        impeller.l,
                        impeller.l,
                        0 * length_unit], length_unit)

    impeller_y = array([impeller.ds / 2,
                        impeller.d1 / 2,
                        impeller.d1 / 2,
                        impeller.d2 / 2,
                        impeller.d2 / 2,
                        impeller.dh / 2,
                        impeller.dh / 2,
                        impeller.ds / 2,
                        impeller.ds / 2], length_unit)

    plt.plot(impeller_x,  impeller_y, color="palegreen")
    plt.plot(impeller_x, -impeller_y, color="palegreen")

    plt.axis("equal")

    figpath = os.path.join(outdir, "impeller.png")
    plt.savefig(figpath, dpi=300, bbox_inches="tight")
    plt.close("all")

def plot_rotor(rotor, outdir):
    """
    """
    rotor.impeller["impeller"].format_units()
    length_unit = rotor.impeller["impeller"].d2.units

    length = sum(segment["l"] for segment in rotor.shaft.segments)
    width = max([bearing["model"].D for bearing in rotor.bearings])
    aspect_ratio = (length / width).to("dimensionless").magnitude * 0.8

    # shaft layout plot
    fig_height = 3
    plt.figure(figsize=(aspect_ratio*fig_height, fig_height))

    for segment in rotor.shaft.segments:
        x1, x2 = segment["x0"], segment["x0"]+segment["l"]
        y1, y2 = -segment["d"]/2, segment["d"]/2

        segment_x = array([x1, x1, x2, x2, x1], length_unit)
        segment_y = array([y1, y2, y2, y1, y1], length_unit)

        plt.plot(segment_x, segment_y, color="white")

    for bearing in rotor.bearings:
        x1, x2 = bearing["x1"], bearing["x2"]
        y1, y2 = bearing["model"].d/2, bearing["model"].D/2

        bearing_x = array([x1, x1, x2, x2, x1], length_unit)
        bearing_y = array([y1, y2, y2, y1, y1], length_unit)

        plt.plot(bearing_x,  bearing_y, color="lightskyblue")
        plt.plot(bearing_x, -bearing_y, color="lightskyblue")
        
        cross_x = array([x1, x2, x1, x2], length_unit)
        cross_y = array([y1, y2, y2, y1], length_unit)

        plt.plot(cross_x,  cross_y, color="lightskyblue")
        plt.plot(cross_x, -cross_y, color="lightskyblue")

        # plot contact angle lines
        axial_distance = bearing["model"].D/2 * np.sin(bearing["model"].alpha)
        end_point      = bearing["xc"] + axial_distance

        if bearing["orientation"] == "right":
            end_point = bearing["xc"] - axial_distance

        line_x = array([bearing["xc"], end_point], length_unit)
        line_y = array([0 * length_unit, bearing["model"].D/2], length_unit)

        plt.plot(line_x,  line_y, color="lavender",
                 linestyle="dashdot", linewidth=1)
        plt.plot(line_x, -line_y, color="lavender",
                 linestyle="dashdot", linewidth=1)

    # plot impeller
    impeller_x = array([0 * length_unit,
                        0 * length_unit,
                        -(rotor.impeller["impeller"].b1 - rotor.impeller["impeller"].b2),
                        0 * length_unit,
                        rotor.impeller["impeller"].b2,
                        rotor.impeller["impeller"].b2,
                        rotor.impeller["impeller"].l,
                        rotor.impeller["impeller"].l,
                        0 * length_unit], length_unit)

    impeller_y = array([rotor.impeller["impeller"].ds / 2,
                        rotor.impeller["impeller"].d1 / 2,
                        rotor.impeller["impeller"].d1 / 2,
                        rotor.impeller["impeller"].d2 / 2,
                        rotor.impeller["impeller"].d2 / 2,
                        rotor.impeller["impeller"].dh / 2,
                        rotor.impeller["impeller"].dh / 2,
                        rotor.impeller["impeller"].ds / 2,
                        rotor.impeller["impeller"].ds / 2], length_unit)


    if rotor.impeller["orientation"] == "left":
        impeller_x = impeller_x + rotor.impeller["x1"].to(length_unit).magnitude
    elif rotor.impeller["orientation"] == "right":
        impeller_x = rotor.impeller["x2"].to(length_unit).magnitude - impeller_x

    plt.plot(impeller_x,  impeller_y, color="palegreen")
    plt.plot(impeller_x, -impeller_y, color="palegreen")

    centerline_x = array([0 * length_unit, length], length_unit)
    centerline_y = array([0 * length_unit, 0 * length_unit], length_unit)

    plt.plot(centerline_x, centerline_y, color="darkgray",
             linestyle="dashdot", linewidth=1.0)

    plt.axis("equal")

    short_unit_string = f"{length_unit:~}"
    plt.xlabel(f"axial coordinate ({short_unit_string})")
    plt.ylabel(f"radial coordinate ({short_unit_string})")

    figpath = os.path.join(outdir, "rotor.png")
    plt.savefig(figpath, dpi=300, bbox_inches="tight")
    plt.close("all")
