import numpy as np
from matplotlib.patches import Arc, RegularPolygon
from numpy import radians as rad


def get_arrow(radius, centX, centY, angle_, theta2_, color_="black"):
    """
    Get circular arrow for visualizing motir torque.

    Parameters
    ----------
    radius : float
        radius, unit=[m]
    centX : float
        arrow center x-coordintate
    centY : float
        arrow center y-coordintate
    angle_ : float
        orientation of the arrow
    theta2_ : float
        the arrow does extend over this angle
    color_ : string or matplotlib color object
        color of the arrow
         (Default value = 'black')

    Returns
    -------
    matplotlib.patches.Arc
        Arrow arc
    matplotlib.patches.RegularPolygon
        Arrow head
    """
    arc = Arc(
        [centX, centY],
        radius,
        radius,
        angle=angle_,
        theta1=0,
        theta2=theta2_,
        capstyle="round",
        linestyle="-",
        lw=2,
        color=color_,
    )

    endX = centX + (radius / 2) * np.cos(rad(theta2_ + angle_))
    endY = centY + (radius / 2) * np.sin(rad(theta2_ + angle_))

    head = RegularPolygon(
        (endX, endY),  # (x,y)
        3,  # number of vertices
        radius / 20,  # radius
        rad(angle_ + theta2_),  # orientation
        color=color_,
    )
    return arc, head


def set_arrow_properties(arc, head, tau, x, y):
    """
    Set arrow properties

    Changes are made directly in the provided arc and head objects

    Parameters
    ----------
    arc : matplotlib.patches.Arc
        Arrow arc
    head : matplotlib.patches.RegularPolygon
        Arrow head
    tau : float
        motor torque the arrow is supposed to visualize
    x : float
        x-coordinate
    y : float
        y-coordinate
    """
    tau_rad = np.clip(0.1 * np.abs(tau) + 0.2, -1, 1)
    if tau > 0:
        theta2 = -40
        arrow_angle = 110
        endX = x + (tau_rad / 2) * np.cos(rad(theta2 + arrow_angle))
        endY = y + (tau_rad / 2) * np.sin(rad(theta2 + arrow_angle))
        orientation = rad(arrow_angle + theta2)
    else:
        theta2 = 320
        arrow_angle = 110
        endX = x + (tau_rad / 2) * np.cos(rad(arrow_angle))
        endY = y + (tau_rad / 2) * np.sin(rad(arrow_angle))
        orientation = rad(-arrow_angle - theta2)
    arc.center = [x, y]
    arc.width = tau_rad
    arc.height = tau_rad
    arc.angle = arrow_angle
    arc.theta2 = theta2

    head.xy = [endX, endY]
    head.radius = tau_rad / 20
    head.orientation = orientation

    if np.abs(tau) <= 0.01:
        arc.set_visible(False)
        head.set_visible(False)
    else:
        arc.set_visible(True)
        head.set_visible(True)
