from math import sin, cos, pi

def flythrough_position(frame, total):
    t = frame / float(total - 1)

    theta = 4.0 * pi * t

    radius = 60.0 - 30.0 * t

    x = radius * cos(theta)
    y = radius * sin(theta)

    z = 15.0 + 55.0 * t

    return (x, y, z)
