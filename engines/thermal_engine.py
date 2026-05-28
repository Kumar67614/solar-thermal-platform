import math

CP = 4186

def thermal_load(
    lpd,
    tin,
    tout
):

    q = (
        lpd *
        CP *
        (tout-tin)
    ) / 3600000

    return q


def collector_efficiency(
    eta0,
    a1,
    a2,
    tm,
    ta,
    g
):

    x = (tm-ta)/g

    eta = (
        eta0 -
        a1*x -
        a2*(x**2)
    )

    return max(0,eta)


def collector_output(
    area,
    eta,
    irradiance
):

    q = (
        area *
        eta *
        irradiance
    )

    return q


def collectors_required(
    load,
    collector_output
):

    n = math.ceil(
        load /
        collector_output
    )

    return n