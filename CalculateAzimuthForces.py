def CalculateAzimuthForces(azimuthAngle):
    c = [azimuthAngle ** 5, azimuthAngle ** 4, azimuthAngle ** 3, azimuthAngle ** 2, azimuthAngle, 1]
    xTable = [
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000]
    ]
    yTable = [
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000]
    ]
    zTable = [
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000],
        [0.000000000,0.000000000,0.000000000,0.000000000,0.000000000,0.000000000]
    ]
    xForces = []
    yForces = []
    zForces = []
    for i in range(len(xTable)):
        xForce = 0
        yForce = 0
        zForce = 0
        for j in range(len(c)):
            xForce = xForce + xTable[i][j] * c[j]
            yForce = yForce + yTable[i][j] * c[j]
            zForce = zForce + zTable[i][j] * c[j]
        xForces.append(xForce)
        yForces.append(yForce)
        zForces.append(zForce)
    return xForces, yForces, zForces