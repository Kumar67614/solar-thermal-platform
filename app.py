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
# SYSTEM PDF GENERATION FUNCTION
# =====================================================
def compile_proposal_pdf_document(industry, load, collectors, total_area, total_flow, cost, savings, payback, npv_val, collector_type, rows, cols, tin, tout, irradiance, fuel_cost, df_analytics, fig_layout_img):
    """
    Creates a clean, downloadable PDF report. 
    Uses standard everyday wording instead of complex engineering jargon.
    """
    try:
        from fpdf import FPDF
    except ImportError:
        st.error("Missing PDF tool. Please run: pip install fpdf2")
        return None

    class FPDFProposal(FPDF):
        def header(self):
            self.set_fill_color(15, 23, 42) 
            self.rect(0, 0, 210, 38, 'F')
            self.set_font("Helvetica", "B", 16)
            self.set_text_color(255, 255, 255)
            self.set_y(10)
            self.cell(0, 0, "Solar Water Heating Project Setup Plan", ln=1, align="C")
            self.set_font("Helvetica", "", 10)
            self.set_text_color(56, 189, 248)
            self.set_y(20)
            self.cell(0, 0, f"System Setup Details & Savings Estimate - {industry} Factory", ln=1, align="C")
            self.set_y(42)

        def footer(self):
            self.set_y(-15)
            self.set_font("Helvetica", "I", 8)
            self.set_text_color(100, 116, 139)
            self.cell(0, 10, f"Solar System Setup Guide  |  Page {self.page_no()}", align="R")

    pdf = FPDFProposal()
    pdf.add_page()
    pdf.set_margins(15, 20, 15)
    
    # --- SECTION 1: SYSTEM SETUP ---
    pdf.set_text_color(2, 132, 199)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "1. Solar System Size & Specifications", ln=1)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(30, 41, 59)
    tech_metrics = [
        ("Daily Hot Water Heat Needed", f"{load:.1f} kWh / Day"),
        ("Water Temperature Boost", f"From {tin} C up to {tout} C Target"),
        ("Type of Solar Panel Selected", f"{collector_type} System"),
        ("Total Solar Panels Needed", f"{collectors} Panels ({rows} Rows x {cols} Columns)"),
        ("Total Roof/Ground Space Needed", f"{total_area:.1f} sq. meters"),
        ("Water Flow Speed Inside Main Pipes", f"{total_flow:.1f} Liters Per Hour")
    ]
    for label, val in tech_metrics:
        pdf.cell(110, 7, label, border="B")
        pdf.cell(70, 7, val, border="B", ln=1, align="R")
        
    pdf.ln(8)
    
    # --- SECTION 2: COST AND SAVINGS ---
    pdf.set_text_color(2, 132, 199)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "2. Project Cost & Fuel Savings Summary", ln=1)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(3)
    
    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(30, 41, 59)
    fin_metrics = [
        ("Total Estimated Initial Cost (CapEx)", f"INR {cost:,.0f}"),
        ("Year 1 Boiler Fuel Money Saved", f"INR {savings:,.0f}"),
        ("Time Needed to Get Money Back (Payback)", f"{payback:.2f} Years"),
        ("Total Estimated 20-Year Profit (NPV)", f"INR {npv_val:,.0f}")
    ]
    for label, val in fin_metrics:
        pdf.cell(110, 7, label, border="B")
        pdf.cell(70, 7, val, border="B", ln=1, align="R")

    pdf.ln(8)

    # --- SECTION 3: MAP / DIAGRAM ---
    pdf.set_text_color(2, 132, 199)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "3. Solar Panel Field Layout Map", ln=1)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(4)

    if fig_layout_img is not None:
        current_y = pdf.get_y()
        pdf.image(fig_layout_img, x=25, y=current_y, w=160)
        pdf.set_y(current_y + 95) 
    else:
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 10, "Layout map drawing could not be loaded.", ln=1)
    
    pdf.ln(6)

    # --- SECTION 4: MONTHLY DATA ---
    pdf.add_page()
    pdf.set_text_color(2, 132, 199)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "4. Expected Month-by-Month Performance", ln=1)
    pdf.line(15, pdf.get_y(), 195, pdf.get_y())
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(248, 250, 252)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(35, 7, "Month", border=1, fill=True)
    pdf.cell(35, 7, "Panel Efficiency", border=1, fill=True, align="C")
    pdf.cell(40, 7, "Heat Produced (kWh/day)", border=1, fill=True, align="C")
    pdf.cell(35, 7, "Solar Share (%)", border=1, fill=True, align="C")
    pdf.cell(35, 7, "Fuel Saved", border=1, fill=True, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 9)
    pdf.set_text_color(30, 41, 59)
    for _, r in df_analytics.iterrows():
        pdf.cell(35, 7, str(r['Month']), border=1)
        pdf.cell(35, 7, f"{r['Efficiency (%)']:.1f}%", border=1, align="C")
        pdf.cell(40, 7, f"{r['Collector Yield (kWh/day)']:.1f}", border=1, align="C")
        pdf.cell(35, 7, f"{r['Solar Fraction (%)']:.1f}%", border=1, align="C")
        pdf.cell(35, 7, f"{r['Fuel Saved (Liters/month)']:.0f} L", border=1, align="C")
        pdf.ln()

    return bytes(pdf.output())


# =====================================================
# THERMAL CORE MATH & EVERYDAY LANGUAGE UTILITIES
# =====================================================
def calculate_pipe_diameter(total_flow_lph):
    """Calculates regular commercial nominal pipe size (DN) based on flow rate."""
    if total_flow_lph <= 150: return "20"
    elif total_flow_lph <= 400: return "25"
    elif total_flow_lph <= 900: return "32"
    elif total_flow_lph <= 1500: return "40"
    elif total_flow_lph <= 3000: return "50"
    elif total_flow_lph <= 6000: return "65"
    elif total_flow_lph <= 12000: return "80"
    else: return "100"

def calculate_solar_physics(daily_water_lpd, tinlet, tout, tambient, total_flow_lph, eta_0=0.75, a1=3.5, a2=0.015, g_radiation=800):
    """Calculates basic heat outputs using simple water temperature values."""
    cp_water = 4.186 
    delta_t = max(1.0, tout - tinlet)
    daily_energy_kj = daily_water_lpd * cp_water * delta_t
    daily_energy_kwh = daily_energy_kj / 3600.0
    
    t_avg = (tinlet + tout) / 2.0
    t_reduced = (t_avg - tambient) / max(10, g_radiation)
    
    efficiency = eta_0 - (a1 * t_reduced) - (a2 * g_radiation * (t_reduced ** 2))
    efficiency = max(0.20, min(0.85, efficiency))
    
    peak_solar_hours = 5.5
    required_peak_power_kw = daily_energy_kwh / peak_solar_hours
    available_solar_power_per_m2 = (g_radiation / 1000.0) * efficiency 
    aperture_area_m2 = required_peak_power_kw / max(0.1, available_solar_power_per_m2)
    
    th_in = tout + 8.0  
    th_out = tinlet + 6.0 
    
    dt1 = th_in - tout
    dt2 = th_out - tinlet
    dt_max = max(dt1, dt2)
    dt_min = min(dt1, dt2)
    
    lmtd = (dt_max - dt2) / math.log(dt_max / max(0.1, dt_min)) if dt_max != dt_min else dt1
    hx_efficiency = max(75.0, min(96.0, 95.0 - (total_flow_lph / 1500.0)))
    
    boiler_dependency = max(10, min(95, int((tout / 110.0) * 100 * (1.0 - (efficiency * 0.5)))))
    
    return {
        "daily_energy_kwh": round(daily_energy_kwh, 1),
        "efficiency_pct": round(efficiency * 100, 1),
        "aperture_area_m2": round(aperture_area_m2, 1),
        "lmtd": round(lmtd, 1),
        "hx_efficiency": round(hx_efficiency, 1),
        "boiler_dependency": int(boiler_dependency),
        "delta_t": round(delta_t, 1)
    }

def render_dynamic_integration_ui(industry="Dairy", tout=80, tinlet=25, tambient=30, daily_water=5000, total_flow=250, eta_0=0.75, a1=3.5, a2=0.015):
    """Generates simple, clear descriptions explaining how the parts fit together."""
    physics = calculate_solar_physics(daily_water, tinlet, tout, tambient, total_flow, eta_0, a1, a2)
    recommended_dn = calculate_pipe_diameter(total_flow)
    
    if total_flow >= 600:
        flow_style = "Fast Water Speed"
        flow_color = "#2E7D32" 
        flow_bar = min(100, int((total_flow / 2000) * 100))
        flow_desc = f"At <b>{total_flow:,} Liters Per Hour</b>, water moves quickly through the panels. This steady speed keeps mud or scale from settling inside the tubes, keeping them clean."
    else:
        flow_style = "Slow Water Speed"
        flow_color = "#1565C0" 
        flow_bar = max(20, int((total_flow / 600) * 100))
        flow_desc = f"At <b>{total_flow:,} Liters Per Hour</b>, water moves at a gentle pace. This saves electrical power on the water pump while getting plenty of heat from the sun."

    if physics['delta_t'] > 45:
        recirc_style = "Water Reuse Loop"
        recirc_bar = "88%"
        recirc_desc = f"Because you need a high temperature increase ({physics['delta_t']}°C), automatic valves will keep the water cycling through the solar panels until it reaches the final heat target."
    else:
        recirc_style = "Straight-Through Flow"
        recirc_bar = "35%"
        recirc_desc = f"Since you only need a small temperature change ({physics['delta_t']}°C), the water gets hot enough in just one trip through the panels, saving extra pipework."

    if tambient < 12:
        weather_style = "Freeze Safety Drain"
        weather_icon = "❄️"
        weather_desc = f"The weather gets quite cold ({tambient}°C) at night, so the system is set to automatically empty the pipes to stop ice from breaking them."
    else:
        weather_style = "Overheat Protection System"
        weather_icon = "☀️"
        weather_desc = f"The local climate is warm ({tambient}°C), so the system has an automated cooling release to stop water from turning into dangerous boiling steam when the factory is closed."

    profiles = {
        "Dairy": {"color": "#1e4620", "accent": "#2E7D32", "bg": "#f4f9f4", "icon": "🥛"},
        "Textile": {"color": "#0d3c61", "accent": "#1565C0", "bg": "#f0f5fa", "icon": "🧵"},
        "Pharmaceutical": {"color": "#4a154b", "accent": "#6A1B9A", "bg": "#faf2fa", "icon": "🧪"},
        "Chemical": {"color": "#E65100", "accent": "#E65100", "bg": "#FFF3E0", "icon": "⚗️"},
        "Food": {"color": "#D32F2F", "accent": "#D32F2F", "bg": "#FFEBEE", "icon": "🍲"}
    }
    p = profiles.get(industry, profiles["Food"])

    industry_specs = {
        "Dairy": [
            {"label": "🛠️ Pipes & Cleanliness", "val": f"DN {recommended_dn} Stainless Steel (Food-Grade)", "desc": f"Perfect size for a flow of {total_flow:,} Liters Per Hour to meet regular dairy hygiene rules. Sloped slightly so all water empties completely during washdowns."},
            {"label": "🔄 Heat Exchanger Unit", "val": f"Cleanable Plate Unit ({physics['hx_efficiency']}% Efficient)", "desc": f"Polished internal plates transfer sun heat smoothly to your clean water lines while keeping them completely separated."},
            {"label": "🔥 Main Boiler Interlock", "val": f"Backup Boiler Control ({physics['boiler_dependency']}% System Load)", "desc": f"The backup boiler automatically turns on only if the solar water tank temperature falls below {tout - 4}°C, reducing your daily fuel consumption."}
        ],
        "Textile": [
            {"label": "🛠️ Pipe Selection", "val": f"DN {recommended_dn} Industrial Steel Pipes", "desc": f"Thick steel tubes coated with protective paint. Built tough to withstand standard water pressure surges during dyeing runs."},
            {"label": "🔄 Heat Exchanger Unit", "val": f"Heavy Duty Titanium Unit ({physics['hx_efficiency']}% Efficient)", "desc": f"Sturdy internal plates that handle salt or dye chemicals easily without rusting or clogging over time."},
            {"label": "🔥 Boiler Setup link", "val": f"Automatic Steam Top-up ({physics['boiler_dependency']}% System Load)", "desc": f"Feeds warm solar water into your main steam system. Less fuel is burned since the water starts hot."}
        ],
        "Pharmaceutical": [
            {"label": "🛠️ Sterile Pipe Setup", "val": f"DN {recommended_dn} Clean Mirror-Finish Steel", "desc": f"Smooth inner lining made to handle {total_flow:,} Liters Per Hour safely. Stops bacteria or film buildup to pass regular clean-room safety audits."},
            {"label": "🔄 Heat Exchanger Unit", "val": f"Double-Wall Leak-Safe Unit ({physics['hx_efficiency']}% Efficient)", "desc": f"Two layers of metal isolate your production line. This makes sure solar fluid never mixes with factory medicine batches."},
            {"label": "🔥 Boiler Top-up Controls", "val": f"Precise Heat Regulator ({physics['boiler_dependency']}% System Load)", "desc": f"Holds temperatures dead-steady within a half-degree margin, even if unexpected clouds block out solar exposure."}
        ],
        "Chemical": [
            {"label": "🛠️ Heavy Chemical Pipes", "val": f"DN {recommended_dn} High-Strength Alloy", "desc": f"Special alloy tubes selected to survive nearby chemical gas fumes, outside heat changes, and long-term strain without rust issues."},
            {"label": "🔄 Heat Exchanger Unit", "val": f"Reinforced Shell & Core Stack ({physics['hx_efficiency']}% Efficient)", "desc": f"Sturdy build safely keeps harsh chemicals separate from regular water loops while letting heat pass through cleanly."},
            {"label": "🔥 Boiler Burner Sync", "val": f"Automated 3-Way Routing Valve ({physics['boiler_dependency']}% System Load)", "desc": f"Instantly routes water to your standard gas boiler if winter weather or persistent rain limits solar heat generation."}
        ],
        "Food": [
            {"label": "🛠️ Food-Safe Piping", "val": f"DN {recommended_dn} Clean Grade Stainless Steel", "desc": f"Uses standard quick-clamp joints. Plant workers can easily open, clean, and re-clamp sections by hand without needing welding tools."},
            {"label": "🔄 Heat Exchanger Unit", "val": f"Removable Silicone Gasket Unit ({physics['hx_efficiency']}% Efficient)", "desc": f"Easy-to-open design with safe silicone seals. Avoids food particles getting trapped between production shifts."},
            {"label": "🔥 Boiler Top-up Assist", "val": f"Direct Temperature Monitor ({physics['boiler_dependency']}% System Load)", "desc": f"Measures water tank warmth constantly. Tells the fuel burner to light up only when the solar system needs extra help."}
        ]
    }
    active_specs = industry_specs.get(industry, industry_specs["Food"])

    html = f"""
    <div style="font-family: Arial, sans-serif; background-color: #ffffff; padding: 5px; border-radius: 12px; max-width: 1050px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, {p['color']}, {p['accent']}); color: white; padding: 25px; border-radius: 12px; margin-bottom: 25px;">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                <div>
                    <h2 style="margin: 0; font-size: 23px; font-weight: 700;">SOLAR SYSTEM PARTS CONNECTOR</h2>
                    <p style="margin: 4px 0 0 0; opacity: 0.9; font-size: 13px;">Simple Setup Guide for <b>{industry} Factories</b></p>
                </div>
                <div style="font-size: 34px; background: rgba(255,255,255,0.2); width: 55px; height: 55px; line-height: 55px; text-align: center; border-radius: 50%;">{p['icon']}</div>
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 15px; margin-top: 25px; background: rgba(0,0,0,0.15); padding: 15px; border-radius: 10px;">
                <div>
                    <div style="font-size: 11px; opacity: 0.85; text-transform: uppercase; font-weight: 600;">Total Panel Size</div>
                    <div style="font-size: 21px; font-weight: 700; margin: 2px 0 4px 0; color: #ffd54f;">{physics['aperture_area_m2']} m²</div>
                    <div style="font-size: 11px; opacity: 0.8;">Total solar surface needed</div>
                </div>
                <div style="border-left: 1px solid rgba(255,255,255,0.2); padding-left: 15px;">
                    <div style="font-size: 11px; opacity: 0.85; text-transform: uppercase; font-weight: 600;">Daily Solar Heat Made</div>
                    <div style="font-size: 21px; font-weight: 700; margin: 2px 0 4px 0;">{physics['daily_energy_kwh']} kWh</div>
                    <div style="font-size: 11px; opacity: 0.8;">Heat delivered to your factory</div>
                </div>
                <div style="border-left: 1px solid rgba(255,255,255,0.2); padding-left: 15px;">
                    <div style="font-size: 11px; opacity: 0.85; text-transform: uppercase; font-weight: 600;">Panel Heat Capture</div>
                    <div style="font-size: 21px; font-weight: 700; margin: 2px 0 4px 0;">{physics['efficiency_pct']}%</div>
                    <div style="font-size: 11px; opacity: 0.8;">Sunlight turned into hot water</div>
                </div>
                <div style="border-left: 1px solid rgba(255,255,255,0.2); padding-left: 15px;">
                    <div style="font-size: 11px; opacity: 0.85; text-transform: uppercase; font-weight: 600;">Main Pipe Thickness</div>
                    <div style="font-size: 21px; font-weight: 700; margin: 2px 0 4px 0; color: #ffffff;">DN {recommended_dn}</div>
                    <div style="font-size: 11px; opacity: 0.8;">Best width for good water speed</div>
                </div>
            </div>
        </div>

        <h3 style="color: #2C3E50; font-size: 14px; font-weight: 700; text-transform: uppercase; margin: 0 0 15px 5px;">How the Core Parts Work</h3>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(310px, 1fr)); gap: 20px;">
            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border-top: 4px solid {p['accent']};">
                <h4 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 15px; font-weight: 700;">{active_specs[0]['label']}</h4>
                <div style="background: #ffffff; padding: 8px 12px; border-radius: 6px; font-size: 13px; font-weight: 700; color: #333; border-left: 3px solid {p['accent']}; margin-bottom: 12px;">
                    {active_specs[0]['val']}
                </div>
                <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5;">{active_specs[0]['desc']}</p>
            </div>

            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border-top: 4px solid {p['accent']};">
                <h4 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 15px; font-weight: 700;">{active_specs[1]['label']}</h4>
                <div style="display: flex; justify-content: space-between; font-size: 11px; color: #666; margin-bottom: 4px; font-weight: 600;">
                    <span>Heat Loss</span><span style="color: {p['accent']};">Transfer Rate: {physics['hx_efficiency']}%</span>
                </div>
                <div style="background: #e2e8f0; height: 10px; border-radius: 5px; margin-bottom: 12px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, {p['accent']}, #81c784); width: {physics['hx_efficiency']}%; height: 100%;"></div>
                </div>
                <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5;">{active_specs[1]['desc']}</p>
            </div>

            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border-top: 4px solid {p['accent']};">
                <h4 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 15px; font-weight: 700;">{active_specs[2]['label']}</h4>
                <div style="display: flex; justify-content: space-between; font-size: 11px; color: #666; margin-bottom: 4px; font-weight: 600;">
                    <span>Solar Coverage</span><span style="color: #d32f2f;">Boiler Support Needed: {physics['boiler_dependency']}%</span>
                </div>
                <div style="background: #e2e8f0; height: 10px; border-radius: 5px; margin-bottom: 12px; overflow: hidden;">
                    <div style="background: linear-gradient(90deg, #ffb74d, #e53935); width: {physics['boiler_dependency']}%; height: 100%;"></div>
                </div>
                <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5;">{active_specs[2]['desc']}</p>
            </div>

            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border-top: 4px solid {p['accent']};">
                <h4 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 15px; font-weight: 700;">💧 Water Speed Details</h4>
                <div style="display: flex; justify-content: space-between; font-size: 11px; color: #777; margin-bottom: 4px; font-weight: 600;">
                    <span>Slow Speed</span><span style="color: {flow_color};">{flow_style}</span><span>High Speed</span>
                </div>
                <div style="background: #e2e8f0; height: 10px; border-radius: 5px; margin-bottom: 12px; overflow: hidden;">
                    <div style="background: {flow_color}; width: {flow_bar}%; height: 100%;"></div>
                </div>
                <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5;">{flow_desc}</p>
            </div>

            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border-top: 4px solid {p['accent']};">
                <h4 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 15px; font-weight: 700;">🔄 Water Routing Method</h4>
                <div style="display: flex; justify-content: space-between; font-size: 11px; color: #777; margin-bottom: 4px; font-weight: 600;">
                    <span>Single Pass</span><span style="color: {p['accent']};">{recirc_style}</span><span>Recycle Loop</span>
                </div>
                <div style="background: #e2e8f0; height: 10px; border-radius: 5px; margin-bottom: 12px; overflow: hidden;">
                    <div style="background: {p['accent']}; width: {recirc_bar}; height: 100%;"></div>
                </div>
                <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5;">{recirc_desc}</p>
            </div>

            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border-top: 4px solid {p['accent']};">
                <h4 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 15px; font-weight: 700;">{weather_icon} Weather Safety Setting</h4>
                <div style="background: #ffffff; padding: 8px 12px; border-radius: 6px; font-size: 13px; font-weight: 700; color: #333; border-left: 3px solid #e53935; margin-bottom: 12px;">
                    {weather_style}
                </div>
                <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5;">{weather_desc}</p>
            </div>
        </div>

        <div style="margin-top: 25px; padding: 15px; background-color: #fffde7; border-left: 5px solid #fbc02d; border-radius: 4px; font-size: 12.5px; color: #5c501a; line-height: 1.5;">
            <b>Live Status:</b> Changing your water or temperature numbers on the left sidebar will immediately recalculate the panel size, fuel savings, pipe diameters, and safety settings.
        </div>
    </div>
    """
    return html

# =====================================================
# SYSTEM INITIALIZATION & PAGE CONFIG
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
# AUTOMATED CALCULATION ENGINES RUNTIME
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

# =====================================================
# GENERATE & CAPTURE LAYOUT MAP DRAWING IMAGE
# =====================================================
winter_solstice_altitude = 90.0 - abs(latitude + 23.45)
vertical_rise = collector_height * math.sin(math.radians(30)) 
panel_ground_footprint = collector_height * math.cos(math.radians(30))
min_shading_space = vertical_rise / math.tan(math.radians(winter_solstice_altitude))
ideal_pitch_distance = panel_ground_footprint + min_shading_space + 0.5 

fig_layout = draw_layout(
    rows=calculated_rows, cols=calculated_cols, 
    width=collector_width, height=collector_height, 
    pitch=ideal_pitch_distance, tilt=30, latitude=latitude
)

# Save diagram to memory buffer without crashing or corrupting files
buf_layout_img = io.BytesIO()
fig_layout.savefig(buf_layout_img, format="png", dpi=200, bbox_inches='tight')
buf_layout_img.seek(0)

# =====================================================
# COMPILE DOWNLOADABLE PDF DOCUMENT
# =====================================================
pdf_data_buffer = compile_proposal_pdf_document(
    industry=industry, load=load, collectors=collectors, total_area=total_area, 
    total_flow=total_flow, cost=cost_dash, savings=savings_dash, payback=pb_dash, 
    npv_val=n_dash, collector_type=collector_type, rows=calculated_rows, cols=calculated_cols,
    tin=tin, tout=tout, irradiance=irradiance, fuel_cost=fuel_cost, df_analytics=df_analytics,
    fig_layout_img=buf_layout_img
)

st.sidebar.markdown("---")
if pdf_data_buffer is not None:
    st.sidebar.download_button(
        label="📥 Download Proposal PDF Report",
        data=pdf_data_buffer,
        file_name=f"Solar_Heating_Plan_{industry}.pdf",
        mime="application/pdf",
        use_container_width=True
    )
else:
    st.sidebar.error("Error creating PDF document.")

# =====================================================
# APP USER INTERFACE NAVIGATION TABS
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
# TAB 0: MAIN VISUAL DASHBOARD
# =====================================================
with tabs[0]:
    st.title("Industrial Solar Thermal Proposal Platform")
    st.markdown("---")

    st.subheader("☀️ Engineered Thermal System Sizing")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Calculated Process Load", f"{load:.1f} kWh / Day")
    c2.metric("Required Modules Count", f"{collectors} Units")
    c3.metric("Total Field Gross Footprint", f"{total_area:.1f} m²")
    c4.metric("Design Hydraulic Loop Flow", f"{total_flow:.1f} LPH")

    st.subheader("💰 Investment Returns Summary")
    f1, f2, f3, f4 = st.columns(4)
    f1.metric("Estimated Project Cost (CapEx)", f"₹ {cost_dash:,.0f}")
    f2.metric("Year 1 Fuel Displaced Savings", f"₹ {savings_dash:,.0f}")
    f3.metric("Dynamic Payback Period", f"{pb_dash:.2f} Years")
    f4.metric("Net Present Value (20-Yr NPV)", f"₹ {n_dash:,.0f}")

    st.markdown("---")
    st.subheader("📊 Performance & Savings Analysis Graphs")
    
    g_row1_c1, g_row1_c2 = st.columns(2)
    with g_row1_c1:
        param_x_range = np.linspace(0.0, 0.12, 100)
        efficiency_curve = eta0 - (a1 * param_x_range) - (a2 * (param_x_range ** 2) * irradiance / 1000.0)
        efficiency_curve = np.clip(efficiency_curve, 0, 1) * 100.0
        current_x_point = (tm - ambient) / irradiance
        current_y_point = eta_operational * 100.0

        fig_hwb = go.Figure()
        fig_hwb.add_trace(go.Scatter(x=param_x_range, y=efficiency_curve, mode='lines', name='Panel Performance', line=dict(color='#0284c7', width=3)))
        fig_hwb.add_trace(go.Scatter(x=[current_x_point], y=[current_y_point], mode='markers', name='Current Status', marker=dict(color='#ea580c', size=12, symbol='diamond')))
        fig_hwb.update_layout(title="<b>1. Collector Efficiency Curve</b>", xaxis_title="Temperature Difference Parameter", yaxis_title="Efficiency (%)", plot_bgcolor="#ffffff", height=350, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_hwb, use_container_width=True, key='graph_hwb_profile')

    with g_row1_c2:
        water_range_lpd = np.linspace(max(1000, daily_water - 4000), daily_water + 4000, 50)
        calculated_kwh_range = (water_range_lpd * 4.186 * (tout - tin)) / 3600.0
        
        fig_vol = go.Figure()
        fig_vol.add_trace(go.Scatter(x=water_range_lpd, y=calculated_kwh_range, mode='lines', name='Water Heat Demand', line=dict(color='#6366f1', width=3)))
        fig_vol.add_trace(go.Scatter(x=[daily_water], y=[load], mode='markers', name='Your Setup Target', marker=dict(color='#ec4899', size=12)))
        fig_vol.update_layout(title="<b>2. Fluid Volume Input vs Thermal Load Requirement</b>", xaxis_title="Daily Water Capacity (LPD)", yaxis_title="Energy Load (kWh/Day)", plot_bgcolor="#ffffff", height=350, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig_vol, use_container_width=True, key='graph_volumetric_load')

    g_row2_c1, g_row2_c2 = st.columns(2)
    with g_row2_c1:
        fig_perf = make_subplots(specs=[[{"secondary_y": True}]])
        fig_perf.add_trace(go.Bar(x=df_analytics["Month"], y=df_analytics["Collector Yield (kWh/day)"], name="Heat Output (kWh)", marker_color="#0284c7"), secondary_y=False)
        fig_perf.add_trace(go.Scatter(x=df_analytics["Month"], y=df_analytics["Solar Fraction (%)"], name="Solar Share %", mode="lines+markers", line=dict(color="#16a34a", width=2)), secondary_y=True)
        fig_perf.update_layout(title="<b>3. Year-Long Seasonal Performance Profile</b>", plot_bgcolor="#ffffff", height=350, margin=dict(l=10, r=10, t=40, b=10), legend=dict(orientation="h", y=-0.2))
        fig_perf.update_yaxes(title_text="Daily Yield (kWh)", secondary_y=False)
        fig_perf.update_yaxes(title_text="Solar Share (%)", range=[0, 110], secondary_y=True)
        st.plotly_chart(fig_perf, use_container_width=True, key='graph_seasonal_profile')

    with g_row2_c2:
        fig_save = make_subplots(specs=[[{"secondary_y": True}]])
        fig_save.add_trace(go.Bar(x=df_analytics["Month"], y=df_analytics["Fuel Saved (Liters/month)"], name="Fuel Saved (Liters)", marker_color="#ea580c"), secondary_y=False)
        fig_save.add_trace(go.Scatter(x=df_analytics["Month"], y=df_analytics["CO2 Mitigated (kg/month)"] / 1000.0, name="CO2 Abated (Tons)", mode="lines+markers", line=dict(color="#047857", width=2, dash="dash")), secondary_y=True)
        fig_save.update_layout(title="<b>4. Fuel Displacement & Carbon Offset Tracker</b>", plot_bgcolor="#ffffff", height=350, margin=dict(l=10, r=10, t=40, b=10), legend=dict(orientation="h", y=-0.2))
        fig_save.update_yaxes(title_text="Fuel Displaced (Liters)", secondary_y=False)
        fig_save.update_yaxes(title_text="CO2 Saved (Metric Tons)", secondary_y=True)
        st.plotly_chart(fig_save, use_container_width=True, key='graph_sustainability_profile')

    st.markdown("---")
    df_timeline_dash = generate_financial_timeline_dataframe(initial_investment=cost_dash, year_one_savings=savings_dash, lifecycle_years=15, discount_rate=0.08, fuel_escalation=0.06, opex_rate=0.015)
    fig_dash_payback = go.Figure()
    fig_dash_payback.add_shape(type="line", x0=0, y0=0, x1=15, y1=0, line=dict(color="#cbd5e1", width=2, dash="dash"))
    fig_dash_payback.add_trace(go.Scatter(x=df_timeline_dash["Year"], y=df_timeline_dash["Cumulative Cash Position (₹)"], mode="lines+markers", name="Net Profits Tracking", line=dict(color="#16a34a", width=4, shape="spline"), marker=dict(size=8, color="#15803d")))
    fig_dash_payback.update_layout(title="<b>5. Financial Return Horizon Timeline Curve</b>", xaxis_title="Years in Operation", yaxis_title="Net Cumulative Balance (₹)", plot_bgcolor="#ffffff", height=350, margin=dict(l=10, r=10, t=40, b=10))
    st.plotly_chart(fig_dash_payback, use_container_width=True, key='graph_payback_profile')

# =====================================================
# APP FUNCTIONAL TABS
# =====================================================
with tabs[1]:
    st.header("Advanced Seasonal Matrix Summary")
    st.dataframe(df_analytics, hide_index=True, use_container_width=True)

with tabs[2]:
    st.header("Solar Field Layout Plan")
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
    st.header("System Integration Dashboard")
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
