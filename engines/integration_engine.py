def calculate_pipe_diameter(total_flow):
    """Calculates standard industrial nominal pipe size (DN) based on LPH flow rate."""
    if total_flow <= 150: return "20"
    elif total_flow <= 400: return "25"
    elif total_flow <= 900: return "32"
    elif total_flow <= 1500: return "40"
    elif total_flow <= 3000: return "50"
    elif total_flow <= 6000: return "65"
    elif total_flow <= 12000: return "80"
    else: return "100"

def recommendations(industry="Dairy", tout=80, tinlet=25, tambient=30, daily_water=5000, total_flow=250):
    """
    Complete Commercial Solar Integration Engine.
    Combines core plumbing sizing, flow style meters, and 6-factor installation profiles
    into a clean, highly pictorial HTML proposal interface.
    """
    recommended_dn = calculate_pipe_diameter(total_flow)
    
    # --- MATH & CALCULATIONS FOR VISUAL STATUS BARS ---
    approach_delta = tout - tinlet
    heat_lift_pct = min(100, max(15, int((approach_delta / 100) * 100)))
    
    # 1. WATER FLOW REGIME METER
    if total_flow >= 500:
        flow_style = "High-Efficiency Fast Flow"
        flow_color = "#2E7D32" # Green
        flow_bar = "80%"
        flow_desc = "Water sweeps through the system quickly to <b>absorb heat rapidly</b> from the collectors. This active motion prevents mineral deposits and keeps internal surfaces clean."
    else:
        flow_style = "Steady Low-Energy Flow"
        flow_color = "#1565C0" # Blue
        flow_bar = "35%"
        flow_desc = "Water travels at a controlled speed to <b>reduce electric pump consumption</b>. Perfect for smaller daily volumes without stressing your facility's power lines."

    # 2. THERMAL RECIRCULATION MANAGEMENT
    if approach_delta > 50:
        recirc_style = "Smart Loop Recirculation"
        recirc_bar = "85%"
        recirc_desc = f"Because your required temperature rise is large ({approach_delta}°C), the system automatically recirculates water until it hits targets, protecting components from thermal shock."
    else:
        recirc_style = "Direct Single-Pass Stream"
        recirc_bar = "40%"
        recirc_desc = f"A moderate heat boost profile ({approach_delta}°C) allows water to reach the target temperature in a single pass, reducing plumbing complexity and valves."

    # 3. WINTER & OVERHEAT PROTECTIONS
    if tambient < 15:
        weather_style = "Freeze Defending Safety"
        weather_icon = "❄️"
        weather_desc = f"Low ambient temperature settings ({tambient}°C) engage automatic drain-down valves or food-safe glycol loops to prevent frozen, burst headers overnight."
    else:
        weather_style = "Overheat Shedding Safety"
        weather_icon = "☀️"
        weather_desc = f"Stable room/outdoor conditions ({tambient}°C) activate night-purging heat dissipation sequences. This keeps utility fluid within safe operational pressure limits."

    # 4. STRUCTURAL MASS FOOTPRINT
    if daily_water >= 6000:
        load_style = "Reinforced Ground/Roof Structural Grid"
        load_bar = "90%"
        load_desc = f"Handling {daily_water:,} Liters means managing a heavy operational load. We include extra structural framing brackets and concrete anchoring pads for high wind resistance."
    else:
        load_style = "Standard Platform Frame Mount"
        load_bar = "45%"
        load_desc = f"A smaller water capacity footprint ({daily_water:,} LPD) fits seamlessly onto your standard facility structural platforms or available maintenance roofs."

    # --- BRANDED INDUSTRY MATRIX ---
    profiles = {
        "Dairy": {"color": "#1e4620", "accent": "#2E7D32", "bg": "#f4f9f4", "icon": "🥛"},
        "Textile": {"color": "#0d3c61", "accent": "#1565C0", "bg": "#f0f5fa", "icon": "🧵"},
        "Pharmaceutical": {"color": "#4a154b", "accent": "#6A1B9A", "bg": "#faf2fa", "icon": "🧪"},
        "Chemical": {"color": "#E65100", "accent": "#E65100", "bg": "#FFF3E0", "icon": "⚗️"},
        "Food": {"color": "#D32F2F", "accent": "#D32F2F", "bg": "#FFEBEE", "icon": "🍲"}
    }
    p = profiles.get(industry, profiles["Food"])

    # Core hardware details based on chosen sector
    industry_specs = {
        "Dairy": [
            {"label": "🛠️ Pipe Specs & Cleaning", "val": f"DN {recommended_dn} SS316 Food-Grade", "desc": "Sized to maintain sanitation speeds (1.0-1.5 m/s) and sloped at 1:40 for clean-in-place (CIP) wash cycles. No residue left behind."},
            {"label": "🔄 Heat Transfer Core", "val": "Sanitary Plate Heat Exchanger", "desc": "Polished stainless plates with food-safe gaskets. Prevents organic buildup or fat accumulation inside the energy loop."}
        ],
        "Textile": [
            {"label": "🛠️ Pipe Specs & Cleaning", "val": f"DN {recommended_dn} Heavy-Wall Steel", "desc": "Extra-rugged wall framework built to absorb pressure spikes from quick batch-wash discharge dumps. Includes corrosion protection."},
            {"label": "🔄 Heat Transfer Core", "val": "Titanium Shell & Tube", "desc": "Industrial titanium elements crafted to handle high-fouling dye wastewater streams containing chemicals and salts safely."}
        ],
        "Pharmaceutical": [
            {"label": "🛠️ Pipe Specs & Cleaning", "val": f"DN {recommended_dn} Electropolished SS316L", "desc": "Mirror-smooth internal surface finishing to prevent microbial contamination. Fully audits-ready for compliance standards."},
            {"label": "🔄 Heat Transfer Core", "val": "Double-Wall Isolation Frame", "desc": "Two distinct physical walls ensure the solar loop water never touches your pure production lines. Absolute safety."}
        ],
        "Chemical": [
            {"label": "🛠️ Pipe Specs & Cleaning", "val": f"DN {recommended_dn} Hastelloy Alloy", "desc": "Premium anti-acid alloy piping designed to handle aggressive atmospheres, heavy temperature fluctuations, and volatile pressures safely."},
            {"label": "🔄 Heat Transfer Core", "val": "Dual-Tube Safety Shell", "desc": "Specially enclosed leak-capture plates that isolate reactive processing fluids from entering primary utility water lines."}
        ],
        "Food": [
            {"label": "🛠️ Pipe Specs & Cleaning", "val": f"DN {recommended_dn} Polished SS304", "desc": "Assembled with standard manual Tri-Clamp fittings. Maintenance teams can easily open, clean, and verify lines without welding tools."},
            {"label": "🔄 Heat Transfer Core", "val": "FDA-Approved Plate Stack", "desc": "Compression plates featuring non-porous silicone seals built to handle continuous pasteurizing runs reliably."}
        ]
    }
    active_specs = industry_specs.get(industry, industry_specs["Food"])

    # START COMPACT VISUAL CARD LAYOUT
    html = f"""
    <div style="font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #ffffff; padding: 5px; border-radius: 12px; max-width: 1000px; margin: 0 auto;">
        
        <div style="background: linear-gradient(135deg, {p['color']}, {p['accent']}); color: white; padding: 25px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                <div>
                    <h2 style="margin: 0; font-size: 24px; font-weight: 700; letter-spacing: 0.3px;">SYSTEM INTEGRATION BLUEPRINT</h2>
                    <p style="margin: 4px 0 0 0; opacity: 0.9; font-size: 13px;">Solar Plant Layout Configured for the <b>{industry} Industry</b></p>
                </div>
                <div style="font-size: 36px; background: rgba(255,255,255,0.2); width: 60px; height: 60px; line-height: 60px; text-align: center; border-radius: 50%;">{p['icon']}</div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px; margin-top: 25px; background: rgba(0,0,0,0.12); padding: 15px; border-radius: 10px;">
                <div>
                    <div style="font-size: 11px; opacity: 0.85; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Temperature Boost</div>
                    <div style="font-size: 22px; font-weight: 700; margin: 2px 0 6px 0;">+{approach_delta}°C</div>
                    <div style="background: rgba(255,255,255,0.2); height: 6px; border-radius: 3px; overflow: hidden;">
                        <div style="background: #ffd54f; width: {heat_lift_pct}%; height: 100%;"></div>
                    </div>
                </div>
                <div style="border-left: 1px solid rgba(255,255,255,0.2); padding-left: 15px;">
                    <div style="font-size: 11px; opacity: 0.85; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Main Pipe Diameter</div>
                    <div style="font-size: 22px; font-weight: 700; margin: 2px 0 2px 0; color: #fffb00;">DN {recommended_dn}</div>
                    <div style="font-size: 11px; opacity: 0.8;">Industrial Standard</div>
                </div>
                <div style="border-left: 1px solid rgba(255,255,255,0.2); padding-left: 15px;">
                    <div style="font-size: 11px; opacity: 0.85; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Daily Water Volume</div>
                    <div style="font-size: 22px; font-weight: 700; margin: 2px 0 2px 0;">{daily_water:,} <span style="font-size: 13px; font-weight: 400;">LPD</span></div>
                    <div style="font-size: 11px; opacity: 0.8;">Process Target Capacity</div>
                </div>
            </div>
        </div>

        <h3 style="color: #2C3E50; font-size: 15px; font-weight: 700; text-transform: uppercase; margin: 0 0 15px 5px; letter-spacing: 0.5px;">6-Factor Integration Breakdown</h3>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(290px, 1fr)); gap: 20px;">
            
            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border: 1px solid rgba(0,0,0,0.05); border-top: 4px solid {p['accent']}; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h4 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 16px; font-weight: 700;">{active_specs[0]['label']}</h4>
                    <div style="background: #ffffff; padding: 8px 12px; border-radius: 6px; font-size: 13px; font-weight: 700; color: #333; border-left: 3px solid {p['accent']}; margin-bottom: 12px; box-shadow: inset 0 1px 2px rgba(0,0,0,0.02);">
                        {active_specs[0]['val']}
                    </div>
                    <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5;">{active_specs[0]['desc']}</p>
                </div>
            </div>

            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border: 1px solid rgba(0,0,0,0.05); border-top: 4px solid {p['accent']}; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h4 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 16px; font-weight: 700;">{active_specs[1]['label']}</h4>
                    <div style="background: #ffffff; padding: 8px 12px; border-radius: 6px; font-size: 13px; font-weight: 700; color: #333; border-left: 3px solid {p['accent']}; margin-bottom: 12px; box-shadow: inset 0 1px 2px rgba(0,0,0,0.02);">
                        {active_specs[1]['val']}
                    </div>
                    <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5;">{active_specs[1]['desc']}</p>
                </div>
            </div>

            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border: 1px solid rgba(0,0,0,0.05); border-top: 4px solid {p['accent']}; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h4 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 16px; font-weight: 700;">💧 Optimal Flow Regime</h4>
                    <div style="display: flex; justify-content: space-between; font-size: 11px; color: #777; margin-bottom: 4px; font-weight: 600;">
                        <span>Slow Flow</span><span style="color: {flow_color};">{flow_style}</span><span>Storm Flow</span>
                    </div>
                    <div style="background: #e2e8f0; height: 10px; border-radius: 5px; margin-bottom: 12px; overflow: hidden;">
                        <div style="background: {flow_color}; width: {flow_bar}; height: 100%;"></div>
                    </div>
                    <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5;">{flow_desc}</p>
                </div>
            </div>

            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border: 1px solid rgba(0,0,0,0.05); border-top: 4px solid {p['accent']}; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h4 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 16px; font-weight: 700;">🔄 Thermal Loop Delivery</h4>
                    <div style="display: flex; justify-content: space-between; font-size: 11px; color: #777; margin-bottom: 4px; font-weight: 600;">
                        <span>Single-Pass</span><span style="color: {p['accent']};">{recirc_style}</span><span>Recirculation</span>
                    </div>
                    <div style="background: #e2e8f0; height: 10px; border-radius: 5px; margin-bottom: 12px; overflow: hidden;">
                        <div style="background: {p['accent']}; width: {recirc_bar}; height: 100%;"></div>
                    </div>
                    <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5;">{recirc_desc}</p>
                </div>
            </div>

            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border: 1px solid rgba(0,0,0,0.05); border-top: 4px solid {p['accent']}; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h4 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 16px; font-weight: 700;">{weather_icon} Climate Protection</h4>
                    <div style="background: #ffffff; padding: 8px 12px; border-radius: 6px; font-size: 13px; font-weight: 700; color: #333; border-left: 3px solid #e53935; margin-bottom: 12px; box-shadow: inset 0 1px 2px rgba(0,0,0,0.02);">
                        {weather_style}
                    </div>
                    <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5;">{weather_desc}</p>
                </div>
            </div>

            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border: 1px solid rgba(0,0,0,0.05); border-top: 4px solid {p['accent']}; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h4 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 16px; font-weight: 700;">🏗️ Plant Support Profile</h4>
                    <div style="display: flex; justify-content: space-between; font-size: 11px; color: #777; margin-bottom: 4px; font-weight: 600;">
                        <span>Light Frame</span><span style="color: #37474F;">Mass Scale Level</span><span>Heavy Pad</span>
                    </div>
                    <div style="background: #e2e8f0; height: 10px; border-radius: 5px; margin-bottom: 12px; overflow: hidden;">
                        <div style="background: #37474F; width: {load_bar}; height: 100%;"></div>
                    </div>
                    <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5;">{load_desc}</p>
                </div>
            </div>

        </div>

        <div style="margin-top: 25px; padding: 15px; background-color: #fffde7; border-left: 5px solid #fbc02d; border-radius: 4px; font-size: 12.5px; color: #5c501a; line-height: 1.5;">
            <b>Financial Advantage for Plant Directors:</b> This custom system configuration is designed to replace expensive diesel boilers or electric heaters with 100% free sun energy. The layout requires minimal maintenance and is engineered to run reliably for 15 to 20 years.
        </div>
    </div>
    """
    return html
