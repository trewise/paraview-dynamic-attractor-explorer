from math import sin, cos, pi

def spiral_position(frame, total):
    t = frame / float(total - 1)

    radius = 120.0 - 70.0 * t
    theta = 6.0 * pi * t

    x = radius * cos(theta)
    y = radius * sin(theta)
    z = 20.0 + 50.0 * t

    return (x, y, z)
