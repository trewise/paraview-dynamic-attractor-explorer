from math import sin, cos, pi

def orbit_position(frame, total):
    theta = 2.0 * pi * frame / total

    return (
        85.0 * cos(theta),
        85.0 * sin(theta),
        45.0
    )
