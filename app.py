import streamlit as st
import pandas as pd
import numpy as np

from engines.thermal_engine import *
from engines.layout_engine import *
from engines.financial_engine import *
from engines.pid_engine import *
from engines.plotting_engine import *
from engines.integration_engine import *
from engines.installation_engine import *
from engines.literature_engine import *
from engines.hydraulic_engine import *

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Industrial Solar Thermal Platform",
    layout="wide"
)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("Customer Inputs")

industry = st.sidebar.selectbox(
    "Industry",
    [
        "Dairy",
        "Textile",
        "Pharmaceutical",
        "Chemical",
        "Food"
    ]
)

daily_water = st.sidebar.number_input(
    "Daily Water Requirement (LPD)",
    value=5000
)

tin = st.sidebar.number_input(
    "Inlet Temperature °C",
    value=25
)

tout = st.sidebar.number_input(
    "Outlet Temperature °C",
    value=80
)

ambient = st.sidebar.number_input(
    "Ambient Temperature °C",
    value=30
)

irradiance = st.sidebar.slider(
    "Solar Irradiance",
    200,
    1200,
    800
)

peak_hours = st.sidebar.slider(
    "Peak Sun Hours",
    1.0,
    10.0,
    5.5
)

latitude = st.sidebar.number_input(
    "Latitude",
    value=19.1
)

# =====================================================
# COLLECTOR INPUTS
# =====================================================

st.sidebar.header("Collector Parameters")

collector_type = st.sidebar.selectbox(
    "Collector Type",
    [
        "Flat Plate Collector",
        "ETC"
    ]
)

aperture_area = st.sidebar.number_input(
    "Aperture Area m²",
    value=2.0
)

gross_area = st.sidebar.number_input(
    "Gross Area m²",
    value=2.2
)

collector_width = st.sidebar.number_input(
    "Collector Width",
    value=1.0
)

collector_height = st.sidebar.number_input(
    "Collector Height",
    value=2.0
)

eta0 = st.sidebar.number_input(
    "η0",
    value=0.78
)

a1 = st.sidebar.number_input(
    "a1",
    value=3.5
)

a2 = st.sidebar.number_input(
    "a2",
    value=0.015
)

flow_per_collector = st.sidebar.number_input(
    "Flow Per Collector LPH",
    value=50
)

fuel_cost = st.sidebar.number_input(
    "Fuel Cost ₹/kWh",
    value=8
)

# =====================================================
# THERMAL CALCULATION
# =====================================================

load = thermal_load(
    daily_water,
    tin,
    tout
)

tm = (tin + tout)/2

eta = collector_efficiency(
    eta0,
    a1,
    a2,
    tm,
    ambient,
    irradiance
)

output = collector_output(
    aperture_area,
    eta,
    irradiance
)

daily_output = (
    output *
    peak_hours
) / 1000

collectors = collectors_required(
    load,
    daily_output
)

total_area = collectors * gross_area

# =====================================================
# HYDRAULIC
# =====================================================

total_flow = collectors * flow_per_collector

velocity = pipe_velocity(
    total_flow
)

re = reynolds_number(
    velocity
)

head = pump_head(
    total_flow
)

# =====================================================
# TABS
# =====================================================

tabs = st.tabs([
    "Dashboard",
    "Thermal",
    "Solar Layout",
    "P&ID",
    "Financial",
    "Integration",
    "Installation",
    "Literature Survey"
])

# =====================================================
# DASHBOARD
# =====================================================

with tabs[0]:

    st.title("Industrial Solar Thermal Proposal Platform")

    st.subheader("Thermal Metrics")
    c1,c2,c3,c4 = st.columns(4)

    c1.metric(
        "Thermal Load",
        f"{load:.1f} kWh/day"
    )

    c2.metric(
        "Collectors",
        collectors
    )

    c3.metric(
        "Total Area",
        f"{total_area:.1f} m²"
    )

    c4.metric(
        "Flow Rate",
        f"{total_flow:.1f} LPH"
    )

    st.divider()

    st.subheader("Financial Analysis")
    f1, f2, f3, f4 = st.columns(4)

    cost = project_cost(
        total_area
    )

    savings = annual_savings(
        load*300,
        fuel_cost
    )

    pb = payback(
        cost,
        savings
    )

    n = npv(
        cost,
        savings,
        20,
        0.08
    )

    f1.metric(
        "Project Cost",
        f"₹ {cost:,.0f}"
    )

    f2.metric(
        "Annual Savings",
        f"₹ {savings:,.0f}"
    )

    f3.metric(
        "Payback Period",
        f"{pb:.2f} Years"
    )

    f4.metric(
        "NPV (20 Years)",
        f"₹ {n:,.0f}"
    )

    st.divider()

    fig3 = payback_plot()

    st.plotly_chart(
        fig3,
        width='stretch',
        key='dashboard_payback'
    )

# =====================================================
# THERMAL TAB
# =====================================================


with tabs[1]:

    st.header("Thermal Analysis")

    st.write(f"Collector Efficiency = {eta*100:.2f} %")

    fig1 = efficiency_plot(
        eta0,
        a1,
        a2,
        irradiance
    )

    st.plotly_chart(
        fig1,
        width='stretch',
        key='thermal_efficiency'
    )

    fig2 = monthly_yield_plot()

    st.plotly_chart(
        fig2,
        width='stretch',
        key='thermal_monthly_yield'
    )

# =====================================================
# LAYOUT TAB
# =====================================================


with tabs[2]:

    st.header("Solar Field Layout")

    pitch = spacing(
        collector_height,
        25,
        latitude
    )

    cols = 5

    rows = int(np.ceil(collectors/cols))

    st.write(
        f"Recommended Row Pitch = {pitch:.2f} m"
    )

    layout_fig = draw_layout(
        rows,
        cols,
        collector_width,
        collector_height,
        pitch
    )

    st.pyplot(layout_fig)

# =====================================================
# PID TAB
# =====================================================

with tabs[3]:

    st.header("Industrial P&ID (Piping & Instrumentation Diagram)")
    
    st.subheader(f"System Configuration: {industry} Industry")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Collectors:** {collectors}")
        st.write(f"**Daily Demand:** {daily_water} LPD")
        st.write(f"**Outlet Temp:** {tout}°C")
    with col2:
        st.write(f"**Total Flow:** {total_flow:.0f} LPH")
        st.write(f"**Inlet Temp:** {tin}°C")
        st.write(f"**System Load:** {load:.1f} kWh/day")

    pid = generate_pid(
        industry=industry,
        collectors=collectors,
        tout=tout,
        daily_water=daily_water,
        total_flow=total_flow
    )

    st.graphviz_chart(pid)

# =====================================================
# FINANCIAL TAB
# =====================================================

with tabs[4]:

    st.header("Financial Analysis")

    cost = project_cost(
        total_area
    )

    savings = annual_savings(
        load*300,
        fuel_cost
    )

    pb = payback(
        cost,
        savings
    )

    n = npv(
        cost,
        savings,
        20,
        0.08
    )

    st.metric(
        "Project Cost",
        f"₹ {cost:,.0f}"
    )

    st.metric(
        "Annual Savings",
        f"₹ {savings:,.0f}"
    )

    st.metric(
        "Payback",
        f"{pb:.2f} Years"
    )

    st.metric(
        "NPV",
        f"₹ {n:,.0f}"
    )

    fig3 = payback_plot()

    st.plotly_chart(
        fig3,
        width='stretch',
        key='financial_payback'
    )

# =====================================================
# INTEGRATION TAB VIEW MODULE
# =====================================================

with tabs[5]:
    st.header("System Integration & Requirements")
    st.info(f"Detailed integration specifications for **{industry}** industry applications.")
    
    # Generate the highly pictorial product blueprint view layout
    proposal_view = recommendations(
        industry=industry,
        tout=tout,
        tinlet=inlet_temp if 'inlet_temp' in locals() else 25,       # Links to 'Inlet Temperature' slider
        tambient=ambient_temp if 'ambient_temp' in locals() else 30, # Links to 'Ambient Temperature' slider
        daily_water=daily_water,                                     # Links to LPD input
        total_flow=total_flow                                        # Links to active LPH calculation flow rate
    )

    # Render the structured HTML components onto the screen layout
    st.html(proposal_view)
    # =====================================================
# INSTALLATION TAB
# =====================================================

with tabs[6]:

    st.header("Installation Procedure")

    steps = installation_steps()

    for i,s in enumerate(steps):

        st.write(f"{i+1}. {s}")

# =====================================================
# LITERATURE TAB
# =====================================================

with tabs[7]:

    st.header("Literature Survey")

    refs = literature()

    for r in refs:

        st.write(f"- {r}")
