import numpy as np

def project_cost(area):

    return area*12000


def annual_savings(
    energy,
    fuel_cost
):

    return energy*fuel_cost


def payback(
    cost,
    savings
):

    return cost/savings


def npv(
    initial,
    cashflow,
    years,
    rate
):

    flows = []

    for y in range(
        1,
        years+1
    ):

        pv = (
            cashflow /
            ((1+rate)**y)
        )

        flows.append(pv)

    return -initial+sum(flows)