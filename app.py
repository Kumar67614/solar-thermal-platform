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

# Register updated engine functions
from engines.thermal_engine import generate_proposal_analytics, simulate_diurnal_curve, collector_efficiency
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
# SIDEBAR CUSTOMER INPUTS
# =====================================================
st.sidebar.title("Customer Inputs")

industry = st.sidebar.selectbox(
    "Industry Type",
    ["Dairy", "Textile", "Pharmaceutical", "Chemical", "Food"]
)

daily_water = st.sidebar.number_input(
    "Daily Water Requirement (LPD)",
    value=5000
)

tin = st.sidebar.number_input(
    "Inlet Temperature (°C)",
    value=25
)

tout = st.sidebar.number_input(
    "Outlet Temperature (°C)",
    value=80
)

ambient = st.sidebar.number_input(
    "Ambient Temperature (°C)",
    value=30
)

irradiance = st.sidebar.slider(
    "Solar Irradiance (W/m²)",
    200, 1200, 800
)

peak_hours = st.sidebar.slider(
    "Peak Sun Hours / Day",
    1.0, 10.0, 5.5
)

latitude = st.sidebar.number_input(
    "Site Latitude",
    value=19.1
)

# =====================================================
# SIDEBAR COLLECTOR PARAMETERS
# =====================================================
st.sidebar.header("Collector Parameters")

collector_type = st.sidebar.selectbox(
    "Collector Technology",
    ["Flat Plate Collector", "ETC"]
)

aperture_area = st.sidebar.number_input(
    "Aperture Area (m²)",
    value=2.0
)

gross_area = st.sidebar.number_input(
    "Gross Area (m²)",
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
    "Optical Efficiency (η0)",
    value=0.78
)

a1 = st.sidebar.number_input(
    "First-Order Loss Coeff (a1)",
    value=3.5
)

a2 = st.sidebar.number_input(
    "Second-Order Loss Coeff (a2)",
    value=0.015
)

flow_per_collector = st.sidebar.number_input(
    "Flow Per Collector (LPH)",
    value=50
)

fuel_cost = st.sidebar.number_input(
    "Displaced Fuel Cost (₹/kWh)",
    value=8
)

# =====================================================
# AUTOMATED CORE CALCULATIONS BASELINE
# =====================================================
load = thermal_load(daily_water, tin, tout)
tm = (tin + tout) / 2.0

# Calculate specific operational point efficiency via the HWB formula
eta_operational = collector_efficiency(eta0, a1, a2, tm, ambient, irradiance)

instantaneous_output_w = (aperture_area * eta_operational * irradiance)
daily_output = (instantaneous_output_w * peak_hours) / 1000.0
collectors = collectors_required(load, daily_output)
total_area = collectors * gross_area

# Hydraulic parameters
total_flow = collectors * flow_per_collector
velocity = pipe_velocity(total_flow)
re = reynolds_number(velocity)
head = pump_head(total_flow)

# Pre-compute shared backend analytics arrays to ensure sync across all tabs
daily_plant_load, monthly_analytics_list = generate_proposal_analytics(
    lpd=daily_water, tin=tin, tout=tout, latitude=latitude,
    eta0=eta0, a1=a1, a2=a2, aperture_area=aperture_area
)
df_analytics = pd.DataFrame(monthly_analytics_list)

# =====================================================
# SYSTEM APPLICATION INTERFACE NAVIGATION TABS
# =====================================================
tabs = st.tabs([
    "Dashboard",
    "Thermal Analysis",
    "Solar Layout",
    "P&ID Blueprint",
    "Financial Returns",
    "System Integration",
    "Installation Roadmap",
    "Literature Survey"
])

# =====================================================
# TAB 0: PILOT DASHBOARD VIEW
# =====================================================
with tabs[0]:
    st.title("Industrial Solar Thermal Proposal Platform")
    st.markdown("Welcome to the executive assessment cockpit. This dashboard provides real-time system sizing, financial modeling, and performance predictions derived from your input parameters.")
    st.markdown("---")

    # Row 1: Engineering & Thermal Sizing KPIs
    st.subheader("☀️ Engineered Thermal System Sizing")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Calculated Process Load", f"{load:.1f} kWh / Day")
    c2.metric("Required Modules Count", f"{collectors} Units")
    c3.metric("Total Field Gross Footprint", f"{total_area:.1f} m²")
    c4.metric("Design Hydraulic Loop Flow", f"{total_flow:.1f} LPH")

    # Row 2: Financial Payback Sizing KPIs with corrected rates
    st.subheader("💰 Investment Returns Summary")
    f1, f2, f3, f4 = st.columns(4)
    
    cost_dash = calculate_market_project_cost(total_area=total_area, collector_type=collector_type)
    annual_energy_yield_sum_kwh = float(df_analytics["Collector Yield (kWh/day)"].sum() * 30.4)
    savings_dash = calculate_real_annual_savings(annual_energy_yield_kwh=annual_energy_yield_sum_kwh, fuel_cost_per_kwh=fuel_cost)
    pb_dash = calculate_dynamic_payback(initial_investment=cost_dash, year_one_savings=savings_dash, fuel_escalation=0.06, opex_rate=0.015)
    n_dash = calculate_comprehensive_npv(initial_investment=cost_dash, year_one_savings=savings_dash, lifecycle_years=20, discount_rate=0.08, fuel_escalation=0.06, opex_rate=0.015)

    f1.metric("Estimated Project Cost (CapEx)", f"₹ {cost_dash:,.0f}")
    f2.metric("Year 1 Fuel Displaced Savings", f"₹ {savings_dash:,.0f}")
    f3.metric("Dynamic Payback Period", f"{pb_dash:.2f} Years")
    f4.metric("Net Present Value (20-Yr NPV)", f"₹ {n_dash:,.0f}")

    st.markdown("---")

    # Row 3: HWB Efficiency Plot & Payback Curve
    st.subheader("📊 Performance Analytics & Investment Projections")
    dash_graph_col1, dash_graph_col2 = st.columns(2)

    with dash_graph_col1:
        # Generate the dynamic HWB Performance Curve
        param_x_range = np.linspace(0.0, 0.12, 100)
        efficiency_curve = eta0 - (a1 * param_x_range) - (a2 * (param_x_range ** 2) * irradiance / 1000.0)
        efficiency_curve = np.clip(efficiency_curve, 0, 1) * 100.0
        
        current_x_point = (tm - ambient) / irradiance
        current_y_point = eta_operational * 100.0

        fig_hwb = go.Figure()
        fig_hwb.add_trace(go.Scatter(
            x=param_x_range, y=efficiency_curve,
            mode='lines', name='HWB Characteristic Curve',
            line=dict(color='#0284c7', width=3)
        ))
        fig_hwb.add_trace(go.Scatter(
            x=[current_x_point], y=[current_y_point],
            mode='markers', name='Active Operating Point',
            marker=dict(color='#ea580c', size=12, symbol='diamond', line=dict(color='#ffffff', width=2))
        ))
        
        fig_hwb.update_layout(
            title=f"<b>Collector Efficiency Profile (HWB Equation)</b><br>Current Efficiency: {current_y_point:.1f}%",
            xaxis_title="Thermal Characterization Parameter (Tm - Ta) / G",
            yaxis_title="Collector Efficiency (%)",
            plot_bgcolor="#ffffff", height=380, margin=dict(l=20, r=20, t=60, b=20),
            legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center")
        )
        fig_hwb.update_yaxes(range=[0, 105], gridcolor="#f1f5f9")
        fig_hwb.update_xaxes(gridcolor="#f1f5f9")
        st.plotly_chart(fig_hwb, use_container_width=True, key='dashboard_hwb_curve')

    with dash_graph_col2:
        df_timeline_dash = generate_financial_timeline_dataframe(
            initial_investment=cost_dash, year_one_savings=savings_dash,
            lifecycle_years=15, discount_rate=0.08, fuel_escalation=0.06, opex_rate=0.015
        )
        
        fig_dash_payback = go.Figure()
        fig_dash_payback.add_shape(type="line", x0=0, y0=0, x1=15, y1=0, line=dict(color="#cbd5e1", width=2, dash="dash"))
        fig_dash_payback.add_trace(go.Scatter(
            x=df_timeline_dash["Year"], y=df_timeline_dash["Cumulative Cash Position (₹)"],
            mode="lines+markers", name="Cumulative Cash Balance",
            line=dict(color="#16a34a", width=4, shape="spline"), marker=dict(size=8, color="#15803d")
        ))
        
        fig_dash_payback.update_layout(
            title="<b>Projected Return on Investment (Payback Horizon Curve)</b><br>Breakeven Point Tracker",
            xaxis_title="Years in Operation", yaxis_title="Net Cumulative Position (₹)",
            plot_bgcolor="#ffffff", height=380, margin=dict(l=20, r=20, t=60, b=20),
            legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center")
        )
        fig_dash_payback.update_yaxes(gridcolor="#f1f5f9")
        fig_dash_payback.update_xaxes(tickmode="linear", dtick=2, gridcolor="#f1f5f9")
        st.plotly_chart(fig_dash_payback, use_container_width=True, key='dashboard_payback_curve')

# =====================================================
# TAB 1: THERMAL ANALYSIS MODULE
# =====================================================
with tabs[1]:
    st.header("Advanced Thermal Analysis & Proposal Metrics")
    st.markdown("---")
    
    if not df_analytics.empty:
        total_annual_fuel_saved = float(df_analytics["Fuel Saved (Liters/month)"].sum())
        total_annual_co2_saved = float(df_analytics["CO2 Mitigated (kg/month)"].sum())
        average_solar_fraction = float(df_analytics["Solar Fraction (%)"].mean())
    else:
        total_annual_fuel_saved, total_annual_co2_saved, average_solar_fraction = 0.0, 0.0, 0.0

    summary_col1, summary_col2, summary_col3 = st.columns(3)
    summary_col1.metric("Total Fuel Displaced Annually", f"{total_annual_fuel_saved:,.0f} Liters / Year")
    summary_col2.metric("Carbon Footprint Reduction", f"{(total_annual_co2_saved / 1000):,.1f} Metric Tons CO2")
    summary_col3.metric("Average Solar Fraction", f"{average_solar_fraction:.1f} % Contribution")
    st.markdown("---")

    graph_col1, graph_col2 = st.columns(2)
    
    fig_perf = make_subplots(specs=[[{"secondary_y": True}]])
    fig_perf.add_trace(go.Bar(x=df_analytics["Month"], y=df_analytics["Collector Yield (kWh/day)"], name="Daily Thermal Yield (kWh)", marker_color="#0284c7", opacity=0.85), secondary_y=False)
    fig_perf.add_trace(go.Scatter(x=df_analytics["Month"], y=df_analytics["Solar Fraction (%)"], name="Solar Fraction (%)", mode="lines+markers", line=dict(color="#16a34a", width=3)), secondary_y=True)
    fig_perf.update_layout(title="<b>Seasonal Energy Yield & Grid Independence Profile</b>", legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"), plot_bgcolor="#ffffff", height=400)
    fig_perf.update_yaxes(title_text="Daily Yield (kWh)", secondary_y=False, gridcolor="#f1f5f9")
    fig_perf.update_yaxes(title_text="Solar Fraction (%)", range=[0, 110], secondary_y=True, showgrid=False)

    fig_save = make_subplots(specs=[[{"secondary_y": True}]])
    fig_save.add_trace(go.Bar(x=df_analytics["Month"], y=df_analytics["Fuel Saved (Liters/month)"], name="Fossil Fuel Displaced (L)", marker_color="#ea580c", opacity=0.85), secondary_y=False)
    fig_save.add_trace(go.Scatter(x=df_analytics["Month"], y=df_analytics["CO2 Mitigated (kg/month)"] / 1000.0, name="Carbon Footprint Abated (Tons)", mode="lines+markers", line=dict(color="#047857", width=3, dash="dash")), secondary_y=True)
    fig_save.update_layout(title="<b>Monthly Operational Cost Shield & Carbon Offsets</b>", legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center"), plot_bgcolor="#ffffff", height=400)
    fig_save.update_yaxes(title_text="Fuel Saved (Liters)", secondary_y=False, gridcolor="#f1f5f9")
    fig_save.update_yaxes(title_text="CO2 Saved (Metric Tons)", secondary_y=True, showgrid=False)
    
    with graph_col1: st.plotly_chart(fig_perf, use_container_width=True, key='proposal_seasonal_performance')
    with graph_col2: st.plotly_chart(fig_save, use_container_width=True, key='proposal_financial_sustainability')

    st.markdown("---")
    st.subheader("Seasonal Performance Data Matrix")
    st.dataframe(df_analytics, hide_index=True, use_container_width=True)

# =====================================================
# TAB 2: INDUSTRIAL SHADING & FIELD LAYOUT MATRIX
# =====================================================
with tabs[2]:
    st.header("Solar Field Layout Plan")
    col_ui1, col_ui2, col_ui3 = st.columns(3)
    with col_ui1: input_rows = st.number_input("Number of Rows Layout", min_value=1, max_value=20, value=max(1, int(math.ceil(math.sqrt(collectors) / 2))))
    with col_ui2: input_cols = st.number_input("Collectors per Row (Columns Layout)", min_value=1, max_value=50, value=max(1, int(math.ceil(collectors / input_rows))))
    with col_ui3: selected_tilt = st.slider("Collector Frame Tilt Angle (°)", 0, 60, 30)

    winter_solstice_altitude = 90.0 - abs(latitude + 23.45)
    vertical_rise = collector_height * math.sin(math.radians(selected_tilt))
    panel_ground_footprint = collector_height * math.cos(math.radians(selected_tilt))
    min_shading_space = vertical_rise / math.tan(math.radians(winter_solstice_altitude))
    ideal_pitch_distance = panel_ground_footprint + min_shading_space + 0.5 

    fig_layout = draw_layout(rows=input_rows, cols=input_cols, width=collector_width, height=collector_height, pitch=ideal_pitch_distance, tilt=selected_tilt, latitude=latitude)
    st.pyplot(fig_layout)

# =====================================================
# TAB 3: SCHEMATIC P&ID ENGINE WIREFRAME
# =====================================================
with tabs[3]:
    st.header("Industrial Piping & Instrumentation Diagram (P&ID)")
    pid = generate_pid(industry=industry, collectors=collectors, tout=tout, daily_water=daily_water, total_flow=total_flow)
    st.graphviz_chart(pid)

# =====================================================
# TAB 4: ADVANCED INVESTMENT LIFECYCLE MODELING
# =====================================================
with tabs[4]:
    st.header("Financial Performance Analysis & Modeling Parameters")
    fin_col1, fin_col2, fin_col3 = st.columns(3)
    with fin_col1: input_discount_rate = st.slider("Corporate Discount Rate (WACC %)", 4.0, 15.0, 8.5) / 100.0
    with fin_col2: input_fuel_inflation = st.slider("Expected Annual Fuel Inflation (%)", 0.0, 12.0, 6.0) / 100.0
    with fin_col3: input_maintenance_opex = st.slider("Annual Maintenance / OpEx (% of Capex)", 0.5, 5.0, 1.5) / 100.0

    calculated_investment = calculate_market_project_cost(total_area=total_area, collector_type=collector_type)
    year_one_gross_savings = calculate_real_annual_savings(annual_energy_yield_kwh=annual_energy_yield_sum_kwh, fuel_cost_per_kwh=fuel_cost)
    true_payback_period = calculate_dynamic_payback(calculated_investment, year_one_gross_savings, input_fuel_inflation, 0.01, input_maintenance_opex)
    project_net_present_value = calculate_comprehensive_npv(calculated_investment, year_one_gross_savings, 20, input_discount_rate, input_fuel_inflation, 0.01, input_maintenance_opex)

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Capital Required (CapEx)", f"₹ {calculated_investment:,.0f}")
    m2.metric("Year 1 Net Savings", f"₹ {year_one_gross_savings:,.0f}")
    m3.metric("Dynamic Payback Period", f"{true_payback_period:.2f} Years")
    m4.metric("Net Present Value (20-Yr NPV)", f"₹ {project_net_present_value:,.0f}")

    df_timeline = generate_financial_timeline_dataframe(calculated_investment, year_one_gross_savings, 15, input_discount_rate, input_fuel_inflation, 0.01, input_maintenance_opex)
    fig_payback_curve = go.Figure()
    fig_payback_curve.add_shape(type="line", x0=0, y0=0, x1=15, y1=0, line=dict(color="#cbd5e1", width=2, dash="dash"))
    fig_payback_curve.add_trace(go.Scatter(x=df_timeline["Year"], y=df_timeline["Cumulative Cash Position (₹)"], mode="lines+markers", line=dict(color="#10b981", width=4, shape="spline"), marker=dict(size=8)))
    fig_payback_curve.update_layout(xaxis_title="Years in Operation", yaxis_title="Net Project Value (₹)", plot_bgcolor="#ffffff", height=400)
    st.plotly_chart(fig_payback_curve, use_container_width=True, key='financial_tab_payback_render')

# =====================================================
# TAB 5: PROCESS INTEGRATION
# =====================================================
with tabs[5]:
    st.header("Real-Time System Integration Blueprint")
    integration_blueprint = render_dynamic_integration_ui(industry=industry, tout=tout, tinlet=tin, tambient=ambient, daily_water=daily_water, total_flow=total_flow, eta_0=eta0, a1=a1, a2=a2)
    st.html(integration_blueprint)

# =====================================================
# TAB 6: INSTALLATION WORKFLOW PROCEDURES
# =====================================================
with tabs[6]:
    st.header("Step-by-Step System Installation Guide")
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

    installation_data = installation_steps()
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
# TAB 7: LITERATURE SURVEY References
# =====================================================
with tabs[7]:
    st.header("Literature Survey & Engineering Standards Reference List")
    refs = literature()
    for r in refs:
        st.write(f"- {r}")
