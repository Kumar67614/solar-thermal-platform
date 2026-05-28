def calculate_pipe_diameter(total_flow):
    """Calculates engineering pipe sizing based on LPH flow rate."""
    if total_flow <= 150: return "20"
    elif total_flow <= 400: return "25"
    elif total_flow <= 900: return "32"
    elif total_flow <= 1500: return "40"
    elif total_flow <= 3000: return "50"
    elif total_flow <= 6000: return "65"
    elif total_flow <= 12000: return "80"
    else: return "100"

def recommendations(industry="Dairy", tout=80, daily_water=5000, total_flow=250):
    recommended_dn = calculate_pipe_diameter(total_flow)
    
    # Configuration Profiles for Commercial Proposals
    profiles = {
        "Dairy": {
            "color": "#1e4620", "accent": "#2E7D32", "bg": "#f4f9f4", "icon": "🥛",
            "specs": [
                {"label": "Fluid Piping", "val": f"DN {recommended_dn} SS316 Food-Grade", "desc": "Velocity targeted at 1.0–1.5 m/s to prevent organic sediment settling. Pre-sloped at 1:40 for total CIP drainage floor compliance."},
                {"label": "Heat Exchanger", "val": "Sanitary Plate (PHE)", "desc": "AISI 304 polished plates with sanitary EPDM gaskets. Designed with crevice depths under 100 microns to avoid fat buildup."},
                {"label": "Thermal Storage", "val": f"{daily_water:,} L Tank (Ra < 0.8µm)", "desc": "Ultra-smooth internal sanitation finish to prevent bacterial anchoring. Clad in 50mm high-density mineral wool insulation."},
                {"label": "Automation & Safety", "val": "PLC Modulating Control", "desc": "Automated 3-way valves manage boiler bypass. Pt100 RTD sensors deliver precision cross-loop logging within ±0.5°C accuracy."}
            ]
        },
        "Textile": {
            "color": "#0d3c61", "accent": "#1565C0", "bg": "#f0f5fa", "icon": "🧵",
            "specs": [
                {"label": "Fluid Piping", "val": f"DN {recommended_dn} Heavy-Wall Steel", "desc": "Optimized to handle high-velocity batch dumps without water-hammer risks. Features 5mm heavy sacrificial corrosion allowances."},
                {"label": "Heat Exchanger", "val": "Titanium Shell & Tube", "desc": "Solid Titanium element array to resist aggressive textile dyes, fixing salts, and high-fouling process chemistry streams."},
                {"label": "Buffer Tank", "val": f"{daily_water:,} L Stratified Storage", "desc": "Vertical high-aspect architecture with built-in internal diffusion chimneys to preserve thermal layers across fast shift rotations."},
                {"label": "Process Control", "val": "Multi-Zone Batch Loop", "desc": "Automated temperature ramping curves tailored specifically for industrial dye house integration profiles."}
            ]
        },
        "Pharmaceutical": {
            "color": "#4a154b", "accent": "#6A1B9A", "bg": "#faf2fa", "icon": "🧪",
            "specs": [
                {"label": "Fluid Piping", "val": f"DN {recommended_dn} Electropolished SS316L", "desc": "Ultra-pure surface finishes removing fluid stagnation zones. Fully traceable heat-stamped segments for GMP compliance audits."},
                {"label": "Heat Exchanger", "val": "Double-Wall Framework", "desc": "Guarantees zero-leak separation boundaries, separating active solar utility loops from pure WFI production streams."},
                {"label": "Precision Sensors", "val": "Dual RTD Loop (±0.1°C)", "desc": "High-accuracy calibrated instrumentation nodes feeding automated, real-time electronic logs for batch processing verification."},
                {"label": "Compliance Stack", "val": "FDA 21 CFR Part 11 PLC", "desc": "Advanced controllers equipped with tamper-proof automated event tracing logs to pass rigorous quality safety loops."}
            ]
        }
    }
    
    # Fallback default
    p = profiles.get(industry, profiles["Dairy"])
    
    # Build Pictorial Proposal HTML Grid Layout
    html = f"""
    <div style="font-family: 'Segoe UI', Roboto, sans-serif; background-color: #ffffff; padding: 5px; border-radius: 12px;">
        
        <div style="background: linear-gradient(135deg, {p['color']}, {p['accent']}); color: white; padding: 24px; border-radius: 10px; margin-bottom: 24px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <span style="font-size: 32px; background: rgba(255,255,255,0.2); padding: 8px 14px; border-radius: 50%;">{p['icon']}</span>
                    <div>
                        <h2 style="margin: 0; font-size: 22px; font-weight: 700; letter-spacing: 0.5px;">ENGINEERING PROPOSAL SPECIFICATION</h2>
                        <p style="margin: 3px 0 0 0; opacity: 0.85; font-size: 13px;">Custom Solar Thermal Integration Architecture for the {industry} Industry</p>
                    </div>
                </div>
                <div style="background: rgba(255,255,255,0.15); padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 600; text-transform: uppercase; border: 1px solid rgba(255,255,255,0.25);">
                    Proposal Target Code: {industry[:3].upper()}-ISO-{tout}
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 20px; background: rgba(0,0,0,0.15); padding: 15px; border-radius: 8px;">
                <div style="border-right: 1px solid rgba(255,255,255,0.2); padding-right: 10px;">
                    <div style="font-size: 11px; text-transform: uppercase; opacity: 0.75; font-weight: 600;">Target Output Process Temp</div>
                    <div style="font-size: 22px; font-weight: 700; margin-top: 2px;">{tout}°C</div>
                </div>
                <div style="border-right: 1px solid rgba(255,255,255,0.2); padding-right: 10px;">
                    <div style="font-size: 11px; text-transform: uppercase; opacity: 0.75; font-weight: 600;">Daily Hydraulic Design Capacity</div>
                    <div style="font-size: 22px; font-weight: 700; margin-top: 2px;">{daily_water:,} <span style="font-size:13px; font-weight:400;">LPD</span></div>
                </div>
                <div>
                    <div style="font-size: 11px; text-transform: uppercase; opacity: 0.75; font-weight: 600;">Calculated Pipeline Main Size</div>
                    <div style="font-size: 22px; font-weight: 700; margin-top: 2px; color: #fffb00;">DN {recommended_dn}</div>
                </div>
            </div>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 10px;">
    """
    
    for s in p['specs']:
        html += f"""
            <div style="background-color: {p['bg']}; border: 1px solid rgba(0,0,0,0.06); border-top: 4px solid {p['accent']}; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 11px; text-transform: uppercase; color: #666; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 4px;">SYSTEM MODULE</div>
                    <h3 style="margin: 0 0 10px 0; font-size: 16px; font-weight: 700; color: {p['color']};">{s['label']}</h3>
                    <div style="font-size: 14px; font-weight: 700; color: #222; background: #ffffff; padding: 8px 12px; border-radius: 6px; border-left: 3px solid {p['accent']}; margin-bottom: 12px; box-shadow: inset 0 1px 2px rgba(0,0,0,0.02);">
                        {s['val']}
                    </div>
                    <p style="margin: 0; font-size: 12px; color: #44546a; line-height: 1.6; text-align: justify;">
                        {s['desc']}
                    </p>
                </div>
            </div>
        """
        
    html += """
        </div>
        <div style="text-align: right; font-size: 11px; color: #999; margin-top: 15px; font-style: italic; padding-right: 5px;">
            * This technical proposal is dynamically locked to standard industrial plant validation rules.
        </div>
    </div>
    """
    return html
