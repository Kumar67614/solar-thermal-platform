import streamlit as st
import pandas as pd
import numpy as np
import math
import io
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import core mathematical and layout calculation modules
from engines.thermal_engine import *
from engines.layout_engine import *
from engines.financial_engine import *
from engines.pid_engine import *
from engines.plotting_engine import *
from engines.integration_engine import *
from engines.installation_engine import *
from engines.literature_engine import *
from engines.hydraulic_engine import *

# Register updated engine functions explicitly
from engines.thermal_engine import generate_proposal_analytics, simulate_diurnal_curve, collector_efficiency
from engines.financial_engine import (
    calculate_market_project_cost,
    calculate_real_annual_savings,
    calculate_dynamic_payback,
    calculate_comprehensive_npv,
    generate_financial_timeline_dataframe
)

# =====================================================
# PREMIUM HIGH-RESOLUTION PDF COMPILER FUNCTION
# =====================================================
def compile_proposal_pdf_document(industry, load, collectors, total_area, total_flow, cost, savings, payback, npv_val, collector_type, rows, cols):
    """
    Generates a beautifully styled, print-ready layout.
    Injects realistic data metrics from all major tabs into a clean binary buffer stream.
    """
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            @page {{
                size: A4;
                margin: 20mm 15mm;
                @bottom-right {{
                    content: "Page " counter(page);
                    font-family: Arial, sans-serif;
                    font-size: 8pt;
                    color: #64748b;
                }}
            }}
            body {{ font-family: Arial, sans-serif; color: #1e293b; margin: 0; line-height: 1.5; font-size: 10pt; }}
            .header {{ background-color: #0f172a; color: #ffffff; padding: 25px; border-radius: 6px; margin-bottom: 25px; }}
            .header h1 {{ margin: 0; font-size: 22px; font-weight: 700; }}
            .header p {{ margin: 5px 0 0 0; color: #38bdf8; font-size: 13px; }}
            h2 {{ color: #0284c7; border-bottom: 2px solid #e2e8f0; padding-bottom: 6px; margin-top: 25px; page-break-after: avoid; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 12px; margin-bottom: 20px; }}
            th {{ background-color: #f8fafc; color: #475569; text-align: left; padding: 8px 10px; font-size: 12px; border-bottom: 2px solid #cbd5e1; }}
            td {{ padding: 10px; border-bottom: 1px solid #e2e8f0; font-size: 12px; }}
            .highlight-box {{ background-color: #f0fdf4; border-left: 4px solid #16a34a; padding: 12px; margin-top: 20px; border-radius: 0 4px 4px 0; }}
            .highlight-box p {{ margin: 0; color: #14532d; font-weight: bold; font-size: 12px; }}
            .list-item {{ margin-bottom: 8px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Industrial Solar Thermal Project Proposal</h1>
            <p>Comprehensive Engineering Assessment, Sizing Validation & Lifecycle Return Ledger</p>
        </div>
        
        <h2>1. Executive Application Profile</h2>
        <p>This automated industrial proposal document details the thermodynamic capacity models, field array layouts, and lifecycle returns configured for integration at the <strong>{industry}</strong> plant facility.</p>
        
        <h2>2. Technical Design & Hydraulic Sizing Framework</h2>
        <table>
            <thead>
                <tr><th>Design Sizing Parameter</th><th>Calculated Specification Target</th></tr>
            </thead>
            <tbody>
                <tr><td>Calculated Utility Process Thermal Load</td><td><strong>{load:.1f} kWh / Day</strong></td></tr>
                <tr><td>Selected Collector Technology Matrix</td><td><strong>{collector_type} Array</strong></td></tr>
                <tr><td>Required Solar Collector Modules Count</td><td><strong>{collectors} Units ({rows} Rows × {cols} Columns)</strong></td></tr>
                <tr><td>Total Field Footprint Gross Area</td><td><strong>{total_area:.1f} m²</strong></td></tr>
                <tr><td>Balanced Design Loop Flow Rate (Parallel)</td><td><strong>{total_flow:.1f} LPH</strong></td></tr>
            </tbody>
        </table>

        <h2>3. Commercial Investment Ledger</h2>
        <table>
            <thead>
                <tr><th>Financial Milestone Metric</th><th>Projected Lifecycle Return Yield</th></tr>
            </thead>
            <tbody>
                <tr><td>Estimated Initial Capital Outlay (CapEx)</td><td><strong>₹ {cost:,.0f}</strong></td></tr>
                <tr><td>Year 1 Displaced Boiler Fuel Savings</td><td><strong>₹ {savings:,.0f}</strong></td></tr>
                <tr><td>Dynamic Lifecycle Payback Period Window</td><td><strong>{payback:.2f} Years</strong></td></tr>
                <tr><td>Project Net Present Value (20-Yr NPV)</td><td><strong>₹ {npv_val:,.0f}</strong></td></tr>
            </tbody>
        </table>

        <h2>4. Construction & Quality Sign-Off Blueprint</h2>
        <div class="list-item"><strong>• Site Alignment Groundwork:</strong> Anchor racking tracks safely into structural roof beams using laser transit lines.</div>
        <div class="list-item"><strong>• Module Fixed Tilt Assembly:</strong> Clamp panels coplanarly to distribute wind and structural loads evenly.</div>
        <div class="list-item"><strong>• Pressure Integrity Audit:</strong> Perform an on-site hydrostatic test by holding the water loop at 1.5x design pressure for 24 hours to confirm leak-free plumbing.</div>
        <div class="list-item"><strong>• Loss Shield Insulation:</strong> Wrap manifolds in mineral wool jackets under aluminum covers to preserve utility heat.</div>
    </body>
    </html>
    """
    try:
        from weasyprint import HTML
        return HTML(string=html_template).write_pdf()
    except Exception:
        return bytes(html_template, 'utf-8')


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

eta_operational = collector_efficiency(eta0, a1, a2, tm, ambient, irradiance)
instantaneous_output_w = (aperture_area * eta_operational * irradiance)
daily_output = (instantaneous_output_w * peak_hours) / 1000.0
collectors = collectors_required(load, daily_output)
total_area = collectors * gross_area

calculated_rows = max(1, int(math.ceil(math.sqrt(collectors) / 2)))
calculated_cols = max(1, int(math.ceil(collectors / calculated_rows)))

# Fixed hydraulic flow based on parallel layout calculation
total_flow = calculated_rows * flow_per_collector
velocity = pipe_velocity(total_flow)
re = reynolds_number(velocity)
head = pump_head(total_flow)

daily_plant_load, monthly_analytics_list = generate_proposal_analytics(
    lpd=daily_water, tin=tin, tout=tout, latitude=latitude,
    eta0=eta0, a1=a1, a2=a2, aperture_area=aperture_area
)
df_analytics = pd.DataFrame(monthly_analytics_list)

cost_dash = calculate_market_project_cost(total_area=total_area, collector_type=collector_type)
if not df_analytics.empty:
    annual_energy_yield_sum_kwh = float(df_analytics["Collector Yield (kWh/day)"].sum() * 30.4)
else:
    annual_energy_yield_sum_kwh = 0.0
    
savings_dash = calculate_real_annual_savings(annual_energy_yield_kwh=annual_energy_yield_sum_kwh, fuel_cost_per_kwh=fuel_cost)
pb_dash = calculate_dynamic_payback(initial_investment=cost_dash, year_one_savings=savings_dash, fuel_escalation=0.06, opex_rate=0.015)
n_dash = calculate_comprehensive_npv(initial_investment=cost_dash, year_one_savings=savings_dash, lifecycle_years=20, discount_rate=0.08, fuel_escalation=0.06, opex_rate=0.015)

# PDF Generation Stream
pdf_data_buffer = compile_proposal_pdf_document(
    industry=industry, load=load, collectors=collectors, total_area=total_area, 
    total_flow=total_flow, cost=cost_dash, savings=savings_dash, payback=pb_dash, 
    npv_val=n_dash, collector_type=collector_type, rows=calculated_rows, cols=calculated_cols
)
st.sidebar.markdown("---")
st.sidebar.download_button(
    label="📥 Download Proposal PDF",
    data=pdf_data_buffer,
    file_name=f"Solar_Thermal_Proposal_{industry}.pdf",
    mime="application/pdf",
    use_container_width=True
)

# =====================================================
# SYSTEM INTERFACE TABS
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
    st.markdown("---")

    # Row 1: Sizing Metrics
    st.subheader("☀️ Engineered Thermal System Sizing")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Calculated Process Load", f"{load:.1f} kWh / Day")
    c2.metric("Required Modules Count", f"{collectors} Units")
    c3.metric("Total Field Gross Footprint", f"{total_area:.1f} m²")
    c4.metric("Design Hydraulic Loop Flow", f"{total_flow:.1f} LPH (Parallel Configuration)")

    # Row 2: Financial Metrics
    st.subheader("💰 Investment Returns Summary")
    f1, f2, f3, f4 = st.columns(4)
    f1.metric("Estimated Project Cost (CapEx)", f"₹ {cost_dash:,.0f}")
    f2.metric("Year 1 Fuel Displaced Savings", f"₹ {savings_dash:,.0f}")
    f3.metric("Dynamic Payback Period", f"{pb_dash:.2f} Years")
    f4.metric("Net Present Value (20-Yr NPV)", f"₹ {n_dash:,.0f}")

    st.markdown("---")

    # =====================================================
    # 5-VECTOR GRAPHICAL ANALYSIS SECTION
    # =====================================================
    st.subheader("📊 Dynamic Graphical Analysis Suite (Updates with Inputs)")
    
    # ROW 1 OF GRAPHS
    g_row1_c1, g_row1_c2 = st.columns(2)
    
    with g_row1_c1:
        # GRAPH 1: HWB Collector Efficiency Profile
        param_x_range = np.linspace(0.0, 0.12, 100)
        efficiency_curve = eta0 - (a1 * param_x_range) - (a2 * (param_x_range ** 2) * irradiance / 1000.0)
        efficiency_curve = np.clip(efficiency_curve, 0, 1) * 100.0
        current_x_point = (tm - ambient) / irradiance
        current_y_point = eta_operational * 100.0

        fig_hwb = go.Figure()
        fig_hwb.add_trace(go.Scatter(x=param_x_range, y=efficiency_curve, mode='lines', name='HWB Curve', line=dict(color='#0284c7', width=3)))
        fig_hwb.add_trace(go.Scatter(x=[current_x_point], y=[current_y_point], mode='markers', name='Operating Point', marker=dict(color='#ea580c', size=12, symbol='diamond')))
        fig_hwb.update_layout(title="<b>1. Collector Efficiency Curve (HWB Model)</b>", xaxis_title="(Tm - Ta) / G", yaxis_title="Efficiency (%)", plot_bgcolor="#ffffff", height=350, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_hwb, use_container_width=True, key='graph_hwb_profile')

    with g_row1_c2:
        # GRAPH 2: Volumetric Fluid Input vs Thermal Load Requirement
        water_range_lpd = np.linspace(max(1000, daily_water - 4000), daily_water + 4000, 50)
        calculated_kwh_range = (water_range_lpd * 4.186 * (tout - tin)) / 3600.0
        
        fig_vol = go.Figure()
        fig_vol.add_trace(go.Scatter(x=water_range_lpd, y=calculated_kwh_range, mode='lines', name='Thermal Load Scale', line=dict(color='#6366f1', width=3)))
        fig_vol.add_trace(go.Scatter(x=[daily_water], y=[load], mode='markers', name='Your Setup Target', marker=dict(color='#ec4899', size=12)))
        fig_vol.update_layout(title="<b>2. Fluid Volume Input vs Thermal Load Requirement</b>", xaxis_title="Daily Water Capacity (LPD)", yaxis_title="Energy Load (kWh/Day)", plot_bgcolor="#ffffff", height=350, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_vol, use_container_width=True, key='graph_volumetric_load')

    # ROW 2 OF GRAPHS
    g_row2_c1, g_row2_c2 = st.columns(2)
    
    with g_row2_c1:
        # GRAPH 3: Year-Long Monthly Thermal Yield & Solar Fraction
        fig_perf = make_subplots(specs=[[{"secondary_y": True}]])
        fig_perf.add_trace(go.Bar(x=df_analytics["Month"], y=df_analytics["Collector Yield (kWh/day)"], name="Thermal Yield (kWh)", marker_color="#0284c7"), secondary_y=False)
        fig_perf.add_trace(go.Scatter(x=df_analytics["Month"], y=df_analytics["Solar Fraction (%)"], name="Solar Fraction (%)", mode="lines+markers", line=dict(color="#16a34a", width=2)), secondary_y=True)
        fig_perf.update_layout(title="<b>3. Year-Long Seasonal Performance Profile</b>", plot_bgcolor="#ffffff", height=350, margin=dict(l=10, r=10, t=40, b=10), legend=dict(orientation="h", y=-0.2))
        fig_perf.update_yaxes(title_text="Daily Yield (kWh)", secondary_y=False)
        fig_perf.update_yaxes(title_text="Solar Fraction (%)", range=[0, 110], secondary_y=True)
        st.plotly_chart(fig_perf, use_container_width=True, key='graph_seasonal_profile')

    with g_row2_c2:
        # GRAPH 4: Monthly Operational Cost Shield & Carbon Offsets
        fig_save = make_subplots(specs=[[{"secondary_y": True}]])
        fig_save.add_trace(go.Bar(x=df_analytics["Month"], y=df_analytics["Fuel Saved (Liters/month)"], name="Fuel Saved (L)", marker_color="#ea580c"), secondary_y=False)
        fig_save.add_trace(go.Scatter(x=df_analytics["Month"], y=df_analytics["CO2 Mitigated (kg/month)"] / 1000.0, name="CO2 Abated (Tons)", mode="lines+markers", line=dict(color="#047857", width=2, dash="dash")), secondary_y=True)
        fig_save.update_layout(title="<b>4. Fuel Displacement & Carbon Offset Tracker</b>", plot_bgcolor="#ffffff", height=350, margin=dict(l=10, r=10, t=40, b=10), legend=dict(orientation="h", y=-0.2))
        fig_save.update_yaxes(title_text="Fuel Displaced (Liters)", secondary_y=False)
        fig_save.update_yaxes(title_text="CO2 Mitigated (Metric Tons)", secondary_y=True)
        st.plotly_chart(fig_save, use_container_width=True, key='graph_sustainability_profile')

    # ROW 3: HORIZON PAYBACK TIMELINE
    st.markdown("---")
    # GRAPH 5: Long-Term Payback Horizon Curve
    df_timeline_dash = generate_financial_timeline_dataframe(initial_investment=cost_dash, year_one_savings=savings_dash, lifecycle_years=15, discount_rate=0.08, fuel_escalation=0.06, opex_rate=0.015)
    fig_dash_payback = go.Figure()
    fig_dash_payback.add_shape(type="line", x0=0, y0=0, x1=15, y1=0, line=dict(color="#cbd5e1", width=2, dash="dash"))
    fig_dash_payback.add_trace(go.Scatter(x=df_timeline_dash["Year"], y=df_timeline_dash["Cumulative Cash Position (₹)"], mode="lines+markers", name="Cumulative Cash Balance", line=dict(color="#16a34a", width=4, shape="spline"), marker=dict(size=8, color="#15803d")))
    fig_dash_payback.update_layout(title="<b>5. Projected Return on Investment (Payback Horizon Curve)</b>", xaxis_title="Years in Operation", yaxis_title="Net Cumulative Cash Position (₹)", plot_bgcolor="#ffffff", height=350, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig_dash_payback, use_container_width=True, key='graph_payback_profile')

# =====================================================
# RETAIN STANDARD BACKEND MODULE TABS
# =====================================================
with tabs[1]:
    st.header("Advanced Seasonal Matrix")
    st.dataframe(df_analytics, hide_index=True, use_container_width=True)

with tabs[2]:
    st.header("Solar Field Layout Plan")
    col_ui1, col_ui2, col_ui3 = st.columns(3)
    with col_ui1: input_rows = st.number_input("Number of Rows Layout", min_value=1, max_value=20, value=int(calculated_rows))
    with col_ui2: input_cols = st.number_input("Collectors per Row", min_value=1, max_value=50, value=int(calculated_cols))
    with col_ui3: selected_tilt = st.slider("Collector Frame Tilt Angle (°)", 0, 60, 30)
    winter_solstice_altitude = 90.0 - abs(latitude + 23.45)
    vertical_rise = collector_height * math.sin(math.radians(selected_tilt))
    panel_ground_footprint = collector_height * math.cos(math.radians(selected_tilt))
    min_shading_space = vertical_rise / math.tan(math.radians(winter_solstice_altitude))
    ideal_pitch_distance = panel_ground_footprint + min_shading_space + 0.5 
    fig_layout = draw_layout(rows=input_rows, cols=input_cols, width=collector_width, height=collector_height, pitch=ideal_pitch_distance, tilt=selected_tilt, latitude=latitude)
    st.pyplot(fig_layout)

with tabs[3]:
    st.header("P&ID Engine Wiring Diagram")
    pid = generate_pid(industry=industry, collectors=collectors, tout=tout, daily_water=daily_water, total_flow=total_flow)
    st.graphviz_chart(pid)

with tabs[4]:
    st.header("Financial Performance Analysis")
    df_timeline = generate_financial_timeline_dataframe(cost_dash, savings_dash, 15, 0.08, 0.06, 0.015)
    st.dataframe(df_timeline, hide_index=True, use_container_width=True)

with tabs[5]:
    st.header("Real-Time System Integration Blueprint")
    integration_blueprint = render_dynamic_integration_ui(industry=industry, tout=tout, tinlet=tin, tambient=ambient, daily_water=daily_water, total_flow=total_flow, eta_0=eta0, a1=a1, a2=a2)
    st.html(integration_blueprint)

with tabs[6]:
    st.header("Step-by-Step System Installation Guide")
    installation_data = installation_steps()
    for idx, item in enumerate(installation_data):
        with st.expander(f"**Step {idx+1}: {item['step']}**"):
            st.write(item["description"])

with tabs[7]:
    st.header("Engineering Standards Reference List")
    st.write(literature())
