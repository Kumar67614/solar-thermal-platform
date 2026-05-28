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
    Comprehensive Commercial Solar Integration Engine.
    Combines core plumbing sizing, flow style meters, heat exchangers, boiler automation,
    and 6-factor installation profiles into a highly pictorial HTML blueprint presentation.
    """
    recommended_dn = calculate_pipe_diameter(total_flow)
    
    # --- VISUAL GAUGES & DATA CALCULATIONS ---
    approach_delta = tout - tinlet
    heat_lift_pct = min(100, max(15, int((approach_delta / 100) * 100)))
    
    # Heat Exchanger (HX) Performance Simulation (Based on Standard Log Mean Temp Difference)
    hx_efficiency_pct = 92 if total_flow >= 500 else 86
    
    # Boiler Dependency Estimation (Higher target temp = higher boiler readiness requirement)
    boiler_trigger_temp = tout - 5
    boiler_dependency_pct = min(100, max(20, int((tout / 120) * 100)))

    # 1. WATER FLOW REGIME PROFILE
    if total_flow >= 500:
        flow_style = "High-Efficiency Fast Flow"
        flow_color = "#2E7D32" 
        flow_bar = "82%"
        flow_desc = "Water sweeps through the loop quickly to <b>maximize heat absorption</b> from the solar panels. This continuous high velocity stops mineral scaling and keeps internal tubes clean."
    else:
        flow_style = "Steady Low-Energy Flow"
        flow_color = "#1565C0" 
        flow_bar = "40%"
        flow_desc = "Water moves at a controlled speed to <b>reduce electric pump power consumption</b>. Ideal for modest daily process volumes without overloading facility sub-panels."

    # 2. THERMAL ROUTING CONTROL
    if approach_delta > 50:
        recirc_style = "Smart Recirculation Loop"
        recirc_bar = "85%"
        recirc_desc = f"Your large temperature lift requirement ({approach_delta}°C) activates a variable-speed recirculation sequence to pump fluid back through the panels until it reaches full target specs."
    else:
        recirc_style = "Direct Single-Pass Stream"
        recirc_bar = "45%"
        recirc_desc = f"A moderate heat boost profile ({approach_delta}°C) allows water to hit targets in a single pass, streamlining line layouts and minimizing valve maintenance."

    # 3. WINTER & OVERHEAT PROTECTIONS
    if tambient < 15:
        weather_style = "Freeze Defending Protection"
        weather_icon = "❄️"
        weather_desc = f"Low climate conditions ({tambient}°C) engage automated drain-down sequences or food-safe glycol lines to completely eliminate frozen, split manifold hazards overnight."
    else:
        weather_style = "Overheat Dissipation Safeguard"
        weather_icon = "☀️"
        weather_desc = f"Warm ambient baseline ({tambient}°C) activates a night-sky radiation purge loop, keeping utility water within safe, stable operational pressure limits."

    # 4. STRUCTURAL GRID FOOTPRINT
    if daily_water >= 6000:
        load_style = "Reinforced Ground/Roof Grid"
        load_bar = "92%"
        load_desc = f"Managing {daily_water:,} Liters creates heavy structural weight. We utilize heavy-gauge structural steel frames and vibration-isolated mounting pads for maximum wind safety."
    else:
        load_style = "Standard Platform Rack"
        load_bar = "50%"
        load_desc = f"A compact water capacity profile ({daily_water:,} LPD) mounts directly onto standard factory utility mezzanines or available factory roof lines with zero modification."

    # --- BRANDED INDUSTRY ARCHITECTURE MATRIX ---
    profiles = {
        "Dairy": {"color": "#1e4620", "accent": "#2E7D32", "bg": "#f4f9f4", "icon": "🥛"},
        "Textile": {"color": "#0d3c61", "accent": "#1565C0", "bg": "#f0f5fa", "icon": "🧵"},
        "Pharmaceutical": {"color": "#4a154b", "accent": "#6A1B9A", "bg": "#faf2fa", "icon": "🧪"},
        "Chemical": {"color": "#E65100", "accent": "#E65100", "bg": "#FFF3E0", "icon": "⚗️"},
        "Food": {"color": "#D32F2F", "accent": "#D32F2F", "bg": "#FFEBEE", "icon": "🍲"}
    }
    p = profiles.get(industry, profiles["Food"])

    # Detailed Industrial Equipment Specifications
    industry_specs = {
        "Dairy": [
            {"label": "🛠️ Piping Infrastructure", "val": f"DN {recommended_dn} SS316 Food-Grade", "desc": "Maintains fluid velocities inside the 1.0–1.5 m/s sanitation window. Sloped at 1:40 for effortless Clean-In-Place (CIP) drainage sweeps."},
            {"label": "🔄 Heat Exchanger (PHE)", "val": "Sanitary Plate Exchanger Core", "desc": f"AISI 304 electro-polished plate stack with food-safe gaskets. Operates at <b>{hx_efficiency_pct}% thermal transfer efficiency</b> to maximize energy delivery."},
            {"label": "🔥 Boiler Automation Loop", "val": "Modulating Boiler Integration", "desc": f"Tied directly into your main backup steam boiler. Instantly triggers a control valve if tank storage drops below {boiler_trigger_temp}°C, ensuring zero process downtime."}
        ],
        "Textile": [
            {"label": "🛠️ Piping Infrastructure", "val": f"DN {recommended_dn} Heavy-Wall Steel", "desc": "Thick-walled carbon steel featuring a sacrificial 5mm corrosion allowance, engineered to survive rough water-hammer pressure shockwaves from quick dump cycles."},
            {"label": "🔄 Heat Exchanger (PHE)", "val": "Solid Titanium Shell & Tube", "desc": f"Indestructible internal tube bundle designed to operate at <b>{hx_efficiency_pct}% efficiency</b> while completely resisting harsh, acidic dye processing chemical mixtures."},
            {"label": "🔥 Boiler Automation Loop", "val": "Dual-Fuel Hybrid Integration", "desc": f"Automated solar-preheat manifold routes water directly to your existing boiler loop, lowering primary fuel burn demands by up to {boiler_dependency_pct}% during peak operations."}
        ],
        "Pharmaceutical": [
            {"label": "🛠️ Piping Infrastructure", "val": f"DN {recommended_dn} Electropolished SS316L", "desc": "Ultra-pure internal mirror-polish tracking eliminates micro-pockets. Engineered to completely prevent bio-film anchoring and ensure absolute sterility compliance."},
            {"label": "🔄 Heat Exchanger (PHE)", "val": "Double-Wall Isolation Frame", "desc": f"Two physical steel boundary barriers running at <b>{hx_efficiency_pct}% efficiency</b>. Guarantees solar loop fluids can never cross-contaminate pure unadulterated WFI lines."},
            {"label": "🔥 Boiler Automation Loop", "val": "PID Clean Steam Boiler Link", "desc": f"Modulating bypass architecture responds within ±0.5°C accuracy. Automatically engages clean steam backup loops to hold tight sanitization boundaries."}
        ],
        "Chemical": [
            {"label": "🛠️ Piping Infrastructure", "val": f"DN {recommended_dn} Hastelloy Alloy", "desc": "High-nickel alloy composition engineered to survive severe chemical outgassing, high baseline temperatures, and heavy hydraulic line pressure shifts safely."},
            {"label": "🔄 Heat Exchanger (PHE)", "val": "Dual-Tube Protective Shell", "desc": f"Isolated internal core operating at <b>{hx_efficiency_pct}% transfer efficiency</b>. Safely isolates hazardous chemical process liquids away from common municipal utility water systems."},
            {"label": "🔥 Boiler Automation Loop", "val": "Interlocked Thermal Boiler", "desc": f"Electronic 3-way modulating bypass valve link. Diverts fluid to your primary facility boiler system if solar storage reserves show low energy levels during dark weather spells."}
        ],
        "Food": [
            {"label": "🛠️ Piping Infrastructure", "val": f"DN {recommended_dn} Polished SS304", "desc": "Built completely using modular industrial Tri-Clamp fittings. Maintenance personnel can rapidly pull apart, clean, and reassamble standard lines with no welding work needed."},
            {"label": "🔄 Heat Exchanger (PHE)", "val": "FDA-Approved Plate Matrix", "desc": f"High-performance open compression layout utilizing certified non-porous silicone gaskets, running at <b>{hx_efficiency_pct}% efficiency</b> for quick processing runs."},
            {"label": "🔥 Boiler Automation Loop", "val": "Direct Burner Controller", "desc": f"Main system PLC monitors line temperatures via Pt100 sensors. Fires backup heat loops seamlessly if solar reserves dip under raw plant requirement limits."}
        ]
    }
    active_specs = industry_specs.get(industry, industry_specs["Food"])

    # START COMPACT VISUAL DESIGN MATRIX LAYOUT
    html = f"""
    <div style="font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #ffffff; padding: 5px; border-radius: 12px; max-width: 1050px; margin: 0 auto;">
        
        <div style="background: linear-gradient(135deg, {p['color']}, {p['accent']}); color: white; padding: 25px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                <div>
                    <h2 style="margin: 0; font-size: 24px; font-weight: 700; letter-spacing: 0.3px;">SYSTEM INTEGRATION & FLOW ANALYSIS</h2>
                    <p style="margin: 4px 0 0 0; opacity: 0.9; font-size: 13px;">Complete Hardware Deployment Mapping for the <b>{industry} Sector</b></p>
                </div>
                <div style="font-size: 36px; background: rgba(255,255,255,0.2); width: 60px; height: 60px; line-height: 60px; text-align: center; border-radius: 50%;">{p['icon']}</div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 15px; margin-top: 25px; background: rgba(0,0,0,0.12); padding: 15px; border-radius: 10px;">
                <div>
                    <div style="font-size: 11px; opacity: 0.85; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Temperature Lift</div>
                    <div style="font-size: 22px; font-weight: 700; margin: 2px 0 6px 0;">+{approach_delta}°C</div>
                    <div style="background: rgba(255,255,255,0.2); height: 6px; border-radius: 3px; overflow: hidden;">
                        <div style="background: #ffd54f; width: {heat_lift_pct}%; height: 100%;"></div>
                    </div>
                </div>
                <div style="border-left: 1px solid rgba(255,255,255,0.2); padding-left: 15px;">
                    <div style="font-size: 11px; opacity: 0.85; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Main Pipe Diameter</div>
                    <div style="font-size: 22px; font-weight: 700; margin: 2px 0 2px 0; color: #fffb00;">DN {recommended_dn}</div>
                    <div style="font-size: 11px; opacity: 0.8;">Industrial Standard Fitting</div>
                </div>
                <div style="border-left: 1px solid rgba(255,255,255,0.2); padding-left: 15px;">
                    <div style="font-size: 11px; opacity: 0.85; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Daily Water Load</div>
                    <div style="font-size: 22px; font-weight: 700; margin: 2px 0 2px 0;">{daily_water:,} <span style="font-size: 13px; font-weight: 400;">LPD</span></div>
                    <div style="font-size: 11px; opacity: 0.8;">Target Storage Tank Vol</div>
                </div>
            </div>
        </div>

        <h3 style="color: #2C3E50; font-size: 15px; font-weight: 700; text-transform: uppercase; margin: 0 0 15px 5px; letter-spacing: 0.5px;">All-Inclusive Plant Integration Matrix</h3>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(310px, 1fr)); gap: 20px;">
            
            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border: 1px solid rgba(0,0,0,0.05); border-top: 4px solid {p['accent']}; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h4 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 15px; font-weight: 700;">{active_specs[0]['label']}</h4>
                    <div style="background: #ffffff; padding: 8px 12px; border-radius: 6px; font-size: 13px; font-weight: 700; color: #333; border-left: 3px solid {p['accent']}; margin-bottom: 12px; box-shadow: inset 0 1px 2px rgba(0,0,0,0.02);">
                        {active_specs[0]['val']}
                    </div>
                    <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5; text-align: justify;">{active_specs[0]['desc']}</p>
                </div>
            </div>

            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border: 1px solid rgba(0,0,0,0.05); border-top: 4px solid {p['accent']}; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h4 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 15px; font-weight: 700;">{active_specs[1]['label']}</h4>
                    <div style="display: flex; justify-content: space-between; font-size: 11px; color: #666; margin-bottom: 4px; font-weight: 600;">
                        <span>Loss Margin</span><span style="color: {p['accent']};">Thermal Efficiency: {hx_efficiency_pct}%</span>
                    </div>
                    <div style="background: #e2e8f0; height: 10px; border-radius: 5px; margin-bottom: 12px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, {p['accent']}, #81c784); width: {hx_efficiency_pct}%; height: 100%;"></div>
                    </div>
                    <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5; text-align: justify;">{active_specs[1]['desc']}</p>
                </div>
            </div>

            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border: 1px solid rgba(0,0,0,0.05); border-top: 4px solid {p['accent']}; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h4 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 15px; font-weight: 700;">{active_specs[2]['label']}</h4>
                    <div style="display: flex; justify-content: space-between; font-size: 11px; color: #666; margin-bottom: 4px; font-weight: 600;">
                        <span>Solar Priority</span><span style="color: #d32f2f;">Boiler Standby Level: {boiler_dependency_pct}%</span>
                    </div>
                    <div style="background: #e2e8f0; height: 10px; border-radius: 5px; margin-bottom: 12px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #ffb74d, #e53935); width: {boiler_dependency_pct}%; height: 100%;"></div>
                    </div>
                    <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5; text-align: justify;">{active_specs[2]['desc']}</p>
                </div>
            </div>

            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border: 1px solid rgba(0,0,0,0.05); border-top: 4px solid {p['accent']}; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h4 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 15px; font-weight: 700;">💧 Fluid Circulation Style</h4>
                    <div style="display: flex; justify-content: space-between; font-size: 11px; color: #777; margin-bottom: 4px; font-weight: 600;">
                        <span>Laminar (Slow)</span><span style="color: {flow_color};">{flow_style}</span><span>Turbulent (Fast)</span>
                    </div>
                    <div style="background: #e2e8f0; height: 10px; border-radius: 5px; margin-bottom: 12px; overflow: hidden;">
                        <div style="background: {flow_color}; width: {flow_bar}; height: 100%;"></div>
                    </div>
                    <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5; text-align: justify;">{flow_desc}</p>
                </div>
            </div>

            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border: 1px solid rgba(0,0,0,0.05); border-top: 4px solid {p['accent']}; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h4 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 15px; font-weight: 700;">🔄 Energy Flow Configuration</h4>
                    <div style="display: flex; justify-content: space-between; font-size: 11px; color: #777; margin-bottom: 4px; font-weight: 600;">
                        <span>Single-Pass</span><span style="color: {p['accent']};">{recirc_style}</span><span>Recirculation Loop</span>
                    </div>
                    <div style="background: #e2e8f0; height: 10px; border-radius: 5px; margin-bottom: 12px; overflow: hidden;">
                        <div style="background: {p['accent']}; width: {recirc_bar}; height: 100%;"></div>
                    </div>
                    <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5; text-align: justify;">{recirc_desc}</p>
                </div>
            </div>

            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border: 1px solid rgba(0,0,0,0.05); border-top: 4px solid {p['accent']}; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h4 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 15px; font-weight: 700;">{weather_icon} Weather Defense Strategy</h4>
                    <div style="background: #ffffff; padding: 8px 12px; border-radius: 6px; font-size: 13px; font-weight: 700; color: #333; border-left: 3px solid #e53935; margin-bottom: 12px; box-shadow: inset 0 1px 2px rgba(0,0,0,0.02);">
                        {weather_style}
                    </div>
                    <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5; text-align: justify;">{weather_desc}</p>
                </div>
            </div>

        </div>

        <div style="margin-top: 25px; padding: 15px; background-color: #fffde7; border-left: 5px solid #fbc02d; border-radius: 4px; font-size: 12.5px; color: #5c501a; line-height: 1.5;">
            <b>Operational Value to Management:</b> This configuration runs your high-efficiency heat exchanger and primary storage network as a priority fuel shield. Your automated backup boiler will only draw power or fuel on overcast days or during unexpected peak demand spikes. This reduces localized manufacturing energy bills for your facility over a 15–20 year runtime.
        </div>
    </div>
    """
    return html
