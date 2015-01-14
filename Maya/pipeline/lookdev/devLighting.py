"""
    devLighting.py

    __author__ = 'cargoyle'

    description = setup three point lighting easily.

"""

import pymel.core as pm


def threePointlight( type):
    """
        description:

        inputs:

        outputs

    """
    l = ["keyLight", "rimLight", "fillLight"]

    if type == "directional":
        pm.rendering.directionalLight(n = l[0], i = 1.0, rgb = [1.0, 0.9, 0.8])
        pm.rendering.directionalLight(n = l[1], i = 2.0, rgb = [1.0, 0.9, 0.8])
        pm.rendering.directionalLight(n = l[2], i = 0.5, rgb = [0.6, 0.7, 0.8])

    elif type == "point":
        pm.rendering.pointLight(n = l[0])
        pm.rendering.pointLight(n = l[1])
        pm.rendering.pointLight(n = l[2])

    pm.rotate(l[0], [-44.5, 120, 0])
    pm.rotate(l[1], [-13, -55, 0])
    pm.scale(l[0], [4,4,4])
    pm.scale(l[1], [4,4,4])
    pm.scale(l[2], [4,4,4])
    return l