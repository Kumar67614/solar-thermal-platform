import streamlit as st
import pandas as pd
import numpy as np
import math
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from engines.thermal_engine import *
from engines.layout_engine import *
from engines.financial_engine import *
from engines.pid_engine import *
from engines.plotting_engine import *
from engines.integration_engine import *
from engines.installation_engine import *
from engines.literature_engine import *
from engines.hydraulic_engine import *

# Explicitly forcing fresh registration of your newer analytical functions
from engines.thermal_engine import generate_proposal_analytics, simulate_diurnal_curve

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

# Derive instantaneous collector capacity using the updated engine parameters
instantaneous_output_w = (aperture_area * eta * irradiance)

# Map continuous daily baseline generation (kWh/day) per individual module
daily_output = (instantaneous_output_w * peak_hours) / 1000.0

# Calculate required number of collectors with systemic loss tolerances
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
# THERMAL TAB (EXECUTIVE VISUALIZATION DISPLAY)
# =====================================================

with tabs[1]:

    st.header("Advanced Thermal Analysis & Proposal Metrics")
    st.markdown("---")

    # 1. Execute the comprehensive simulation calculations
    daily_plant_load, monthly_analytics_list = generate_proposal_analytics(
        lpd=daily_water,
        tin=tin,
        tout=tout,
        latitude=latitude,
        eta0=eta0,
        a1=a1,
        a2=a2,
        aperture_area=aperture_area
    )
    
    # Generate DataFrame and explicitly ensure columns are typed properly
    df_analytics = pd.DataFrame(monthly_analytics_list)
    
    # Safeguard calculations against empty lists/data structures
    if not df_analytics.empty:
        total_annual_fuel_saved = float(df_analytics["Fuel Saved (Liters/month)"].sum())
        total_annual_co2_saved = float(df_analytics["CO2 Mitigated (kg/month)"].sum())
        average_solar_fraction = float(df_analytics["Solar Fraction (%)"].mean())
    else:
        total_annual_fuel_saved = 0.0
        total_annual_co2_saved = 0.0
        average_solar_fraction = 0.0

    # 2. Key Performance Metric Highlights (C-Suite Value Trackers)
    st.subheader("Annualized Projected Savings Summary")
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    
    summary_col1.metric(
        label="🔥 Total Fuel Displaced Annually",
        value=f"{total_annual_fuel_saved:,.0f} Liters / Year"
    )
    summary_col2.metric(
        label="🌱 Carbon Footprint Reduction",
        value=f"{(total_annual_co2_saved / 1000):,.1f} Metric Tons CO2"
    )
    summary_col3.metric(
        label="☀️ Average Solar Fraction",
        value=f"{average_solar_fraction:.1f} % Contribution"
    )
    
    st.markdown("---")

    # 3. Interactive Graphical Proposal Visualizations (Inlined to prevent ImportErrors)
    st.subheader("Executive Proposal Performance Dashboards")
    graph_col1, graph_col2 = st.columns(2)
    
    # --- CHART 1 GENERATION: ENERGY YIELD & SOLAR FRACTION ---
    fig_perf = make_subplots(specs=[[{"secondary_y": True}]])
    fig_perf.add_trace(
        go.Bar(
            x=df_analytics["Month"],
            y=df_analytics["Collector Yield (kWh/day)"],
            name="Daily Thermal Yield (kWh)",
            marker_color="#0284c7",
            opacity=0.85
        ),
        secondary_y=False
    )
    fig_perf.add_trace(
        go.Scatter(
            x=df_analytics["Month"],
            y=df_analytics["Solar Fraction (%)"],
            name="Solar Fraction (%)",
            mode="lines+markers",
            line=dict(color="#16a34a", width=3)
        ),
        secondary_y=True
    )
    fig_perf.update_layout(
        title="<b>Seasonal Energy Yield & Grid Independence Profile</b>",
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
        plot_bgcolor="#ffffff",
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    fig_perf.update_yaxes(title_text="Daily Yield (kWh)", secondary_y=False, gridcolor="#f1f5f9")
    fig_perf.update_yaxes(title_text="Solar Fraction (%)", range=[0, 110], secondary_y=True, showgrid=False)

    # --- CHART 2 GENERATION: FUEL DISPLACEMENT & CARBON OFFSETS ---
    fig_save = make_subplots(specs=[[{"secondary_y": True}]])
    fig_save.add_trace(
        go.Bar(
            x=df_analytics["Month"],
            y=df_analytics["Fuel Saved (Liters/month)"],
            name="Fossil Fuel Displaced (L)",
            marker_color="#ea580c",
            opacity=0.85
        ),
        secondary_y=False
    )
    fig_save.add_trace(
        go.Scatter(
            x=df_analytics["Month"],
            y=df_analytics["CO2 Mitigated (kg/month)"] / 1000.0,
            name="Carbon Footprint Abated (Tons)",
            mode="lines+markers",
            line=dict(color="#047857", width=3, dash="dash")
        ),
        secondary_y=True
    )
    fig_save.update_layout(
        title="<b>Monthly Operational Cost Shield & Carbon Offsets</b>",
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
        plot_bgcolor="#ffffff",
        height=400,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    fig_save.update_yaxes(title_text="Fuel Saved (Liters)", secondary_y=False, gridcolor="#f1f5f9")
    fig_save.update_yaxes(title_text="CO2 Saved (Metric Tons)", secondary_y=True, showgrid=False)
    
    with graph_col1:
        st.plotly_chart(fig_perf, use_container_width=True, key='proposal_seasonal_performance')
        
    with graph_col2:
        st.plotly_chart(fig_save, use_container_width=True, key='proposal_financial_sustainability')

    st.markdown("---")

    # 4. Technical Verification Data Grid
    st.subheader("Seasonal Performance Matrix (Month-by-Month Simulation Verification)")
    st.dataframe(
        df_analytics,
        column_config={
            "Month": st.column_config.TextColumn("Operational Month"),
            "Efficiency (%)": st.column_config.NumberColumn("Avg Efficiency", format="%d%%"),
            "Collector Yield (kWh/day)": st.column_config.NumberColumn("Daily Energy Yield", format="%.1f kWh"),
            "Solar Fraction (%)": st.column_config.NumberColumn("Boiler Offset", format="%.1f%%"),
            "Fuel Saved (Liters/month)": st.column_config.NumberColumn("Fuel Saved", format="%d L"),
            "CO2 Mitigated (kg/month)": st.column_config.NumberColumn("CO2 Saved", format="%d kg"),
        },
        hide_index=True,
        use_container_width=True
    )

# =====================================================
# LAYOUT TAB
# =====================================================

with tabs[2]:

    st.header("Solar Field Layout")
    
    st.subheader("Array Matrix Control Structure")
    col_ui1, col_ui2, col_ui3 = st.columns(3)
    
    with col_ui1:
        input_rows = st.number_input("Number of Rows", min_value=1, max_value=20, value=max(1, int(math.ceil(math.sqrt(collectors) / 2))))
    with col_ui2:
        input_cols = st.number_input("Collectors per Row (Columns)", min_value=1, max_value=50, value=max(1, int(math.ceil(collectors / input_rows))))
    with col_ui3:
        selected_tilt = st.slider("Collector Tilt Angle (°)", 0, 60, 30)

    # Re-verify layout bounds and sizing parameters
    winter_solstice_altitude = 90.0 - abs(latitude + 23.45)
    vertical_rise = collector_height * math.sin(math.radians(selected_tilt))
    panel_ground_footprint = collector_height * math.cos(math.radians(selected_tilt))

    min_shading_space = vertical_rise / math.tan(math.radians(winter_solstice_altitude))
    ideal_pitch_distance = panel_ground_footprint + min_shading_space + 0.5 

    # Plot responsive engineering blueprint maps
    fig = draw_layout(
        rows=input_rows,
        cols=input_cols,
        width=collector_width,
        height=collector_height,
        pitch=ideal_pitch_distance,
        tilt=selected_tilt,
        latitude=latitude
    )

    st.pyplot(fig)

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
# SYSTEM INTEGRATION DASHBOARD VIEW TAB MODULE
# =====================================================

with tabs[5]:
    st.header("Real-Time System Integration Blueprint")
    st.markdown("---")
    
    integration_blueprint = render_dynamic_integration_ui(
        industry=industry,                                           
        tout=tout,                                                   
        tinlet=tin if 'tin' in locals() else 25,                     
        tambient=ambient if 'ambient' in locals() else 30,           
        daily_water=daily_water,                                     
        total_flow=total_flow,                                       
        eta_0=eta0 if 'eta0' in locals() else 0.75,                  
        a1=a1 if 'a1' in locals() else 3.5,                          
        a2=a2 if 'a2' in locals() else 0.015                         
    )
    
    st.html(integration_blueprint)

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
