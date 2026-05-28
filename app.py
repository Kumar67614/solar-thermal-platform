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
# SIDEBAR - CUSTOMER INPUTS
# =====================================================

st.sidebar.title("Customer Inputs")

industry = st.sidebar.selectbox(
    "Industry",
    ["Dairy", "Textile", "Pharmaceutical", "Chemical", "Food"]
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
    "Solar Irradiance (W/m²)",
    200, 1200, 800
)

# Changed label to reflect standard solar engineering terminology
peak_hours = st.sidebar.slider(
    "Equivalent Peak Sun Hours (h/day)",
    1.0, 10.0, 5.5
)

latitude = st.sidebar.number_input(
    "Latitude",
    value=19.1
)

# Added: Conventional Boiler Efficiency to correct financial metrics
boiler_efficiency = st.sidebar.slider(
    "Existing Boiler Efficiency (%)",
    50, 100, 75
) / 100.0

fuel_cost = st.sidebar.number_input(
    "Fuel Cost ₹/kWh (Thermal equivalent)",
    value=8
)

# =====================================================
# SIDEBAR - COLLECTOR PARAMETERS
# =====================================================

st.sidebar.header("Collector Parameters")

collector_type = st.sidebar.selectbox(
    "Collector Type",
    ["Flat Plate Collector", "ETC"]
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
    "Collector Width (m)",
    value=1.0
)

collector_height = st.sidebar.number_input(
    "Collector Height (m)",
    value=2.0
)

eta0 = st.sidebar.number_input(
    "η0 (Optical Efficiency)",
    value=0.78
)

a1 = st.sidebar.number_input(
    "a1 (Linear Loss Coeff)",
    value=3.5
)

a2 = st.sidebar.number_input(
    "a2 (Quadratic Loss Coeff)",
    value=0.015
)

flow_per_collector = st.sidebar.number_input(
    "Flow Per Collector LPH",
    value=50
)

# Added: Matrix routing parameters to fix hydraulic calculations
st.sidebar.subheader("Array Configuration")
collectors_in_series = st.sidebar.number_input(
    "Collectors in Series per String",
    value=4,
    min_value=1
)

# =====================================================
# THERMAL CALCULATION
# =====================================================

# Q = m * Cp * dT / 3600 -> Outlines daily thermal energy required
load = thermal_load(daily_water, tin, tout)

# NOTE: If this is a closed loop system, tm should dynamically track tank temperatures.
# For a raw single-pass calculation, using the system mean:
tm = (tin + tout) / 2

# Verify that your backend uses: eta = eta0 - a1*(tm-ambient)/irradiance - a2*((tm-ambient)**2)/irradiance
eta = collector_efficiency(eta0, a1, a2, tm, ambient, irradiance)

# Power output per collector based on APERTURE area (kW)
output = collector_output(aperture_area, eta, irradiance) 

# Daily energy yield per collector (kWh/day)
daily_output = (output * peak_hours) / 1000

# Total number of collectors needed
collectors = collectors_required(load, daily_output)

# Total ground/roof footprint based on GROSS area
total_area = collectors * gross_area

# =====================================================
# HYDRAULIC CALCULATION (FIXED LOGIC)
# =====================================================

# Calculate parallel strings to prevent pipe sizing overestimation
parallel_strings = int(np.ceil(collectors / collectors_in_series))
total_flow = parallel_strings * flow_per_collector

velocity = pipe_velocity(total_flow)
re = reynolds_number(velocity)
head = pump_head(total_flow)

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
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Thermal Load", f"{load:.1f} kWh/day")
    c2.metric("Collectors Required", f"{collectors} units")
    c3.metric("Total Gross Area", f"{total_area:.1f} m²")
    c4.metric("Actual System Flow Rate", f"{total_flow:.1f} LPH")

    st.divider()

    st.subheader("Financial Analysis")
    f1, f2, f3, f4 = st.columns(4)

    cost = project_cost(total_area)

    # FIXED: Factored in boiler efficiency to show true displaced fuel savings
    annual_energy_saved = load * 300 
    savings = annual_savings(annual_energy_saved, fuel_cost) / boiler_efficiency

    pb = payback(cost, savings)
    
    # Ensure your backend engine subtracts project_cost from discounted cumulative savings
    n = npv(cost, savings, 20, 0.08)

    f1.metric("Project Cost", f"₹ {cost:,.0f}")
    f2.metric("Annual Savings", f"₹ {savings:,.0f}")
    f3.metric("Payback Period", f"{pb:.2f} Years")
    f4.metric("NPV (20 Years)", f"₹ {n:,.0f}")

    st.divider()

    fig3 = payback_plot()
    st.plotly_chart(fig3, use_container_width=True, key='dashboard_payback')

# =====================================================
# THERMAL TAB
# =====================================================

with tabs[1]:
    st.header("Thermal Analysis")
    st.write(f"Estimated Collector Operational Efficiency = **{eta*100:.2f} %**")

    fig1 = efficiency_plot(eta0, a1, a2, irradiance)
    st.plotly_chart(fig1, use_container_width=True, key='thermal_efficiency')

    fig2 = monthly_yield_plot()
    st.plotly_chart(fig2, use_container_width=True, key='thermal_monthly_yield')

# =====================================================
# LAYOUT TAB
# =====================================================

with tabs[2]:
    st.header("Solar Field Layout")

    pitch = spacing(collector_height, 25, latitude)
    
    # Layout matches the physical wiring constraints established in hydraulics
    cols = parallel_strings
    rows = collectors_in_series

    st.write(f"Recommended Row Pitch (Anti-shading spacing) = **{pitch:.2f} m**")
    st.write(f"Array Matrix Setup: **{rows} rows** deep $\\times$ **{cols} strings** wide")

    layout_fig = draw_layout(rows, cols, collector_width, collector_height, pitch)
    st.pyplot(layout_fig)

# =====================================================
# PID TAB
# =====================================================

with tabs[3]:
    st.header("Industrial P&ID (Piping & Instrumentation Diagram)")
    st.subheader(f"System Configuration: {industry} Industry")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Total Collectors:** {collectors}")
        st.write(f"**Daily Demand:** {daily_water} LPD")
        st.write(f"**Target Outlet Temp:** {tout}°C")
    with col2:
        st.write(f"**Manifold Flow Rate:** {total_flow:.0f} LPH")
        st.write(f"**Source Inlet Temp:** {tin}°C")
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
    st.header("Financial Analysis Breakdown")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Project Cost", f"₹ {cost:,.0f}")
    m2.metric("Annual Savings", f"₹ {savings:,.0f}")
    m3.metric("Payback", f"{pb:.2f} Years")
    m4.metric("NPV", f"₹ {n:,.0f}")

    fig3_financial = payback_plot()
    st.plotly_chart(fig3_financial, use_container_width=True, key='financial_payback')

# =====================================================
# INTEGRATION TAB
# =====================================================

with tabs[5]:
    st.header("System Integration & Requirements")
    st.info(f"Detailed integration specifications for **{industry}** industry applications.")
    
    rec = recommendations(
        industry=industry,
        tout=tout,
        daily_water=daily_water,
        total_flow=total_flow
    )

    current_section = None
    for item in rec:
        if item.startswith("###"):
            if current_section is not None:
                st.divider()
            st.subheader(item.replace("###", "").strip())
            current_section = item
        elif item.startswith("•") or item.startswith("*"):
            st.write(item)

# =====================================================
# INSTALLATION TAB
# =====================================================

with tabs[6]:
    st.header("Installation Procedure")
    steps = installation_steps()
    for i, s in enumerate(steps):
        st.write(f"**Step {i+1}:** {s}")

# =====================================================
# LITERATURE TAB
# =====================================================

with tabs[7]:
    st.header("Literature Survey")
    refs = literature()
    for r in refs:
        st.write(f"- {r}")
