import math

def pipe_velocity(flow):

    q = flow/3600/1000

    d = 0.04

    area = (
        math.pi*d*d
    )/4

    v = q/area

    return v


def reynolds_number(v):

    rho = 1000

    mu = 0.001

    d = 0.04

    re = (
        rho*v*d
    )/mu

    return re


def pump_head(flow):

    h = (
        flow/100
    )*2

    return h