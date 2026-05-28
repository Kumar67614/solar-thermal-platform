import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def efficiency_plot(
    eta0,
    a1,
    a2,
    irradiance
):

    x = np.linspace(
        0,
        0.25,
        100
    )

    y = (
        eta0 -
        a1*x -
        a2*(x**2)
    )*100

    y = np.clip(y,0,100)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode='lines'
        )
    )

    return fig


def monthly_yield_plot():

    months = [
        "Jan","Feb","Mar",
        "Apr","May","Jun",
        "Jul","Aug","Sep",
        "Oct","Nov","Dec"
    ]

    y = [
        1200,1400,1500,
        1700,1800,1500,
        1200,1100,1300,
        1500,1600,1400
    ]

    df = pd.DataFrame({
        "Month":months,
        "Yield":y
    })

    fig = px.bar(
        df,
        x="Month",
        y="Yield"
    )

    return fig


def payback_plot():

    years = np.arange(1,11)

    payback = [
        8,7,6,5,
        4,4,3,3,
        2,2
    ]

    df = pd.DataFrame({
        "Years":years,
        "Payback":payback
    })

    fig = px.line(
        df,
        x="Years",
        y="Payback"
    )

    return fig