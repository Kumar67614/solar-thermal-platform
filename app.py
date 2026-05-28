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

# Explicitly forcing fresh registration of your analytical and financial functions
from engines.thermal_engine import generate_proposal_analytics, simulate_diurnal_curve
from engines.financial_engine import (
    calculate_market_project_cost,
    calculate_real_annual_savings,
    calculate_dynamic_payback,
    calculate_comprehensive_npv,
    generate_financial_timeline_dataframe
)

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
# PRE-COMPUTE THERMAL ANALYTICS FOR SHARED DATA DEPENDENCIES
# =====================================================

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
df_analytics = pd.DataFrame(monthly_analytics_list)

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

    # Market-calibrated pricing functions replacing basic project_cost()
    cost_dash = calculate_market_project_cost(
        total_area=total_area, 
        collector_type=collector_type
    )

    annual_energy_yield_sum_kwh = float(df_analytics["Collector Yield (kWh/day)"].sum() * 30.4)
    savings_dash = calculate_real_annual_savings(
        annual_energy_yield_kwh=annual_energy_yield_sum_kwh, 
        fuel_cost_per_kwh=fuel_cost
    )

    pb_dash = calculate_dynamic_payback(
        initial_investment=cost_dash,
        year_one_savings=savings_dash,
        fuel_escalation=0.06,
        annual_degradation=0.01,
        opex_rate=0.02
    )

    n_dash = calculate_comprehensive_npv(
        initial_investment=cost_dash,
        year_one_savings=savings_dash,
        lifecycle_years=20,
        discount_rate=0.08,
        fuel_escalation=0.06,
        annual_degradation=0.01,
        opex_rate=0.02
    )

    f1.metric(
        "Project Cost",
        f"₹ {cost_dash:,.0f}"
    )

    f2.metric(
        "Annual Savings",
        f"₹ {savings_dash:,.0f}"
    )

    f3.metric(
        "Payback Period",
        f"{pb_dash:.2f} Years"
    )

    f4.metric(
        "NPV (20 Years)",
        f"₹ {n_dash:,.0f}"
    )

    st.divider()

    # Generate visual payback curve map for dashboard interface
    df_timeline_dash = generate_financial_timeline_dataframe(
        initial_investment=cost_dash,
        year_one_savings=savings_dash,
        lifecycle_years=15,
        discount_rate=0.08,
        fuel_escalation=0.06,
        annual_degradation=0.01,
        opex_rate=0.02
    )
    
    fig_dash_payback = go.Figure()
    fig_dash_payback.add_shape(type="line", x0=0, y0=0, x1=15, y1=0, line=dict(color="#cbd5e1", width=2, dash="dash"))
    fig_dash_payback.add_trace(go.Scatter(
        x=df_timeline_dash["Year"], y=df_timeline_dash["Cumulative Cash Position (₹)"],
        mode="lines+markers", name="Cumulative Cash Balance",
        line=dict(color="#0284c7", width=4, shape="spline"), marker=dict(size=8)
    ))
    fig_dash_payback.update_layout(
        xaxis_title="Years in Operation", yaxis_title="Net Project Value (₹)",
        plot_bgcolor="#ffffff", height=400, margin=dict(l=20, r=20, t=20, b=20)
    )
    fig_dash_payback.update_yaxes(gridcolor="#f1f5f9")
    
    st.plotly_chart(
        fig_dash_payback,
        use_container_width=True,
        key='dashboard_payback'
    )

# =====================================================
# THERMAL TAB (EXECUTIVE VISUALIZATION DISPLAY)
# =====================================================

with tabs[1]:

    st.header("Advanced Thermal Analysis & Proposal Metrics")
    st.markdown("---")
    
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
            x=df_analytics["Month"], y=df_analytics["Collector Yield (kWh/day)"],
            name="Daily Thermal Yield (kWh)", marker_color="#0284c7", opacity=0.85
        ),
        secondary_y=False
    )
    fig_perf.add_trace(
        go.Scatter(
            x=df_analytics["Month"], y=df_analytics["Solar Fraction (%)"],
            name="Solar Fraction (%)", mode="lines+markers", line=dict(color="#16a34a", width=3)
        ),
        secondary_y=True
    )
    fig_perf.update_layout(
        title="<b>Seasonal Energy Yield & Grid Independence Profile</b>",
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
        plot_bgcolor="#ffffff", height=400, margin=dict(l=20, r=20, t=50, b=20)
    )
    fig_perf.update_yaxes(title_text="Daily Yield (kWh)", secondary_y=False, gridcolor="#f1f5f9")
    fig_perf.update_yaxes(title_text="Solar Fraction (%)", range=[0, 110], secondary_y=True, showgrid=False)

    # --- CHART 2 GENERATION: FUEL DISPLACEMENT & CARBON OFFSETS ---
    fig_save = make_subplots(specs=[[{"secondary_y": True}]])
    fig_save.add_trace(
        go.Bar(
            x=df_analytics["Month"], y=df_analytics["Fuel Saved (Liters/month)"],
            name="Fossil Fuel Displaced (L)", marker_color="#ea580c", opacity=0.85
        ),
        secondary_y=False
    )
    fig_save.add_trace(
        go.Scatter(
            x=df_analytics["Month"], y=df_analytics["CO2 Mitigated (kg/month)"] / 1000.0,
            name="Carbon Footprint Abated (Tons)", mode="lines+markers", line=dict(color="#047857", width=3, dash="dash")
        ),
        secondary_y=True
    )
    fig_save.update_layout(
        title="<b>Monthly Operational Cost Shield & Carbon Offsets</b>",
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"),
        plot_bgcolor="#ffffff", height=400, margin=dict(l=20, r=20, t=50, b=20)
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

    st.header("Financial Performance Analysis")
    st.markdown("This industrial investment model evaluates multi-year payback projections by tracking compound fuel cost inflation, ongoing maintenance expenses, and collector degradation.")
    st.markdown("---")

    # Local Scenario Modeling Inputs
    st.subheader("Financial Modeling Assumptions")
    fin_col1, fin_col2, fin_col3 = st.columns(3)
    
    with fin_col1:
        input_discount_rate = st.slider("Corporate Discount Rate (WACC %)", 4.0, 15.0, 8.5, step=0.5) / 100.0
    with fin_col2:
        input_fuel_inflation = st.slider("Expected Annual Fuel Inflation (%)", 0.0, 12.0, 6.0, step=0.5) / 100.0
    with fin_col3:
        input_maintenance_opex = st.slider("Annual Maintenance / OpEx (% of Capex)", 0.5, 5.0, 2.0, step=0.5) / 100.0

    st.markdown("---")

    # Compute values using our new market-aligned engine formulas
    calculated_investment = calculate_market_project_cost(
        total_area=total_area, 
        collector_type=collector_type
    )
    
    year_one_gross_savings = calculate_real_annual_savings(
        annual_energy_yield_kwh=annual_energy_yield_sum_kwh, 
        fuel_cost_per_kwh=fuel_cost
    )
    
    true_payback_period = calculate_dynamic_payback(
        initial_investment=calculated_investment,
        year_one_savings=year_one_gross_savings,
        fuel_escalation=input_fuel_inflation,
        annual_degradation=0.01,
        opex_rate=input_maintenance_opex
    )
    
    project_net_present_value = calculate_comprehensive_npv(
        initial_investment=calculated_investment,
        year_one_savings=year_one_gross_savings,
        lifecycle_years=20,
        discount_rate=input_discount_rate,
        fuel_escalation=input_fuel_inflation,
        annual_degradation=0.01,
        opex_rate=input_maintenance_opex
    )

    # Display Executive KPIs
    st.subheader("Investment Returns Metrics Summary")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    metric_col1.metric(
        label="💰 Total Capital Required (CapEx)",
        value=f"₹ {calculated_investment:,.0f}"
    )
    metric_col2.metric(
        label="📉 Year 1 Net Cash Savings",
        value=f"₹ {year_one_gross_savings:,.0f}"
    )
    metric_col3.metric(
        label="⏱️ Dynamic Payback Period",
        value=f"{true_payback_period:.2f} Years"
    )
    metric_col4.metric(
        label="📈 Net Present Value (20-Yr NPV)",
        value=f"₹ {project_net_present_value:,.0f}"
    )

    st.markdown("---")

    # Render an Interactive Investment Cash Flow Chart
    st.subheader("Projected Investment Cash Flow Matrix (Payback Curve)")
    
    df_timeline = generate_financial_timeline_dataframe(
        initial_investment=calculated_investment,
        year_one_savings=year_one_gross_savings,
        lifecycle_years=15,
        discount_rate=input_discount_rate,
        fuel_escalation=input_fuel_inflation,
        annual_degradation=0.01,
        opex_rate=input_maintenance_opex
    )
    
    # Build a clean visual timeline plot using Plotly
    fig_payback_curve = go.Figure()
    fig_payback_curve.add_shape(type="line", x0=0, y0=0, x1=15, y1=0, line=dict(color="#cbd5e1", width=2, dash="dash"))
    fig_payback_curve.add_trace(go.Scatter(
        x=df_timeline["Year"], y=df_timeline["Cumulative Cash Position (₹)"],
        mode="lines+markers", name="Cumulative Cash Balance",
        line=dict(color="#10b981", width=4, shape="spline"), marker=dict(size=8, color="#059669")
    ))
    
    fig_payback_curve.update_layout(
        xaxis_title="Years in Operation", yaxis_title="Net Project Value (₹)",
        plot_bgcolor="#ffffff", height=450, margin=dict(l=20, r=20, t=20, b=20)
    )
    fig_payback_curve.update_yaxes(gridcolor="#f1f5f9")
    fig_payback_curve.update_xaxes(tickmode="linear", dtick=1)
    
    st.plotly_chart(fig_payback_curve, use_container_width=True, key='financial_tab_payback_render')

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
# INSTALLATION TAB (SIMPLIFIED LAYMAN-FRIENDLY VIEW)
# =====================================================

with tabs[6]:
    st.header("Step-by-Step System Installation Guide")
    st.markdown("Here is a simple, easy-to-understand breakdown of how we take your project from a bare roof to a fully operational, fuel-saving solar plant.")
    st.markdown("---")

    # 1. Visual Flowchart Block for Quick Overview
    st.subheader("🗓️ Project Timeline at a Glance")
    
    flowchart_html = """
    <div style="background-color: #f8fafc; padding: 20px; border-radius: 10px; border: 1px solid #e2e8f0; text-align: center; margin-bottom: 25px;">
        <span style="font-weight: bold; color: #0284c7;">1. Marking Spots</span> ➔ 
        <span style="font-weight: bold; color: #0284c7;">2. Building Racks</span> ➔ 
        <span style="font-weight: bold; color: #0284c7;">3. Mounting Panels</span> ➔ 
        <span style="font-weight: bold; color: #0284c7;">4. Connecting Pipes</span>
        <br><br>
        <span style="font-weight: bold; color: #16a34a;">8. System Live!</span> 🮪 
        <span style="font-weight: bold; color: #475569;">7. Wiring Brains</span> 🮪 
        <span style="font-weight: bold; color: #475569;">6. Pipe Jackets</span> 🮪 
        <span style="font-weight: bold; color: #ea580c;">5. Leak Testing</span>
    </div>
    """
    st.html(flowchart_html)

    # 2. Extract Layman-Friendly Steps from the Installation Engine
    installation_data = installation_steps()

    st.subheader("📋 Detailed Phase-by-Phase Breakdown")
    
    # Loop through and build clean, collapsible dropdown info cards
    for idx, item in enumerate(installation_data):
        with st.container():
            with st.expander(f"**Step {idx+1}: {item['icon']} {item['step']}**", expanded=(idx == 0)):
                col_desc, col_checklist = st.columns([2, 1])
                with col_desc:
                    st.markdown("##### 📝 What we do:")
                    st.write(item["description"])
                    st.markdown("##### ✨ Why it matters:")
                    st.info(item["specs"])
                with col_checklist:
                    st.markdown("##### 🔍 Quality Checks:")
                    for check in item["checklist"]:
                        st.checkbox(check, key=f"layman_install_chk_{idx}_{hash(check)}")
            
        st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

# =====================================================
# LITERATURE TAB
# =====================================================

with tabs[7]:

    st.header("Literature Survey")

    refs = literature()

    for r in refs:

        st.write(f"- {r}")
