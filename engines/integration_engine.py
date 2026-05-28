import math

def calculate_pipe_diameter(total_flow_lph):
    """Calculates standard industrial nominal pipe size (DN) based on LPH flow rate."""
    if total_flow_lph <= 150: return "20"
    elif total_flow_lph <= 400: return "25"
    elif total_flow_lph <= 900: return "32"
    elif total_flow_lph <= 1500: return "40"
    elif total_flow_lph <= 3000: return "50"
    elif total_flow_lph <= 6000: return "65"
    elif total_flow_lph <= 12000: return "80"
    else: return "100"

def calculate_solar_physics(daily_water_lpd, tinlet, tout, tambient, total_flow_lph, eta_0=0.75, a1=3.5, a2=0.015, g_radiation=800):
    """
    Performs real-time thermodynamic modeling of the solar field loop using the 
    standard ASHRAE 93 / EN 12975 efficiency curve calculation model.
    """
    # 1. Thermal Load Requirement (Q = m * Cp * deltaT) in Joules and kWh
    cp_water = 4.186 # kJ/kg·K
    delta_t = max(1.0, tout - tinlet)
    daily_energy_kj = daily_water_lpd * cp_water * delta_t
    daily_energy_kwh = daily_energy_kj / 3600.0
    
    # 2. Collector Efficiency Estimation at Average Operating Temp
    t_avg = (tinlet + tout) / 2.0
    t_reduced = (t_avg - tambient) / max(10, g_radiation)
    
    # Efficiency equation: eta = eta_0 - a1*Tm* - a2*G*(Tm*)^2
    efficiency = eta_0 - (a1 * t_reduced) - (a2 * g_radiation * (t_reduced ** 2))
    efficiency = max(0.20, min(0.85, efficiency)) # Operational limits clamp
    
    # 3. Aperture Area Sizing based on standard peak solar day performance (5.5 peak hours)
    peak_solar_hours = 5.5
    required_peak_power_kw = daily_energy_kwh / peak_solar_hours
    available_solar_power_per_m2 = (g_radiation / 1000.0) * efficiency # kW/m2
    aperture_area_m2 = required_peak_power_kw / max(0.1, available_solar_power_per_m2)
    
    # 4. Heat Exchanger Log Mean Temperature Difference (LMTD) & Coefficient
    # Simulating standard counter-flow solar thermal loop conditions
    th_in = tout + 8.0   # Solar collector delivery side fluid loop temperature
    th_out = tinlet + 6.0 # Solar collector returning side fluid loop temperature
    
    dt1 = th_in - tout
    dt2 = th_out - tinlet
    dt_max = max(dt1, dt2)
    dt_min = min(dt1, dt2)
    
    lmtd = (dt_max - dt2) / math.log(dt_max / max(0.1, dt_min)) if dt_max != dt_min else dt1
    hx_efficiency = max(75.0, min(96.0, 95.0 - (total_flow_lph / 1500.0)))
    
    # 5. Boiler Standby Dependency Fraction
    # High output targets mean the boiler runs a higher auxiliary top-up ratio
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
    """
    Renders an entirely input-reactive, physics-backed graphical integration map 
    incorporating real-time solar, boiler, and heat-exchanger performance variables.
    """
    # Run thermodynamic solver matrix
    physics = calculate_solar_physics(daily_water, tinlet, tout, tambient, total_flow, eta_0, a1, a2)
    recommended_dn = calculate_pipe_diameter(total_flow)
    
    # Dynamic Visual Scale Metrics
    heat_lift_pct = min(100, max(15, int((physics['delta_t'] / 100) * 100)))
    
    # 1. WATER FLOW REGIME METER (Reacts dynamically to real-time LPH calculations)
    if total_flow >= 600:
        flow_style = "High-Velocity Fast Flow"
        flow_color = "#2E7D32" 
        flow_bar = min(100, int((total_flow / 2000) * 100))
        flow_desc = f"At <b>{total_flow:,} LPH</b>, water sweeps through the array rapidly. This active scrubbing fluid velocity prevents internal mineral deposition and maintains pristine tube conditions."
    else:
        flow_style = "Controlled Low-Energy Flow"
        flow_color = "#1565C0" 
        flow_bar = max(20, int((total_flow / 600) * 100))
        flow_desc = f"At <b>{total_flow:,} LPH</b>, the loop operates at optimized low speeds, slashing auxiliary pump electrical consumption while maintaining uniform thermal extraction levels."

    # 2. THERMAL RECIRCULATION DELIVERABLE (Reacts dynamically to Temperature Delta)
    if physics['delta_t'] > 45:
        recirc_style = "Smart Recirculation Loop"
        recirc_bar = "88%"
        recirc_desc = f"Your large system temperature lift requirement ({physics['delta_t']}°C) activates digital 3-way modulating valves. Water recirculates dynamically until full target values are verified."
    else:
        recirc_style = "Direct Single-Pass Stream"
        recirc_bar = "35%"
        recirc_desc = f"A minor heat delta boost profiles ({physics['delta_t']}°C) allows water to reach production targets in a single loop traversal, eliminating excess staging valves and plumbing lines."

    # 3. SAFETY AUTOMATION PROFILE (Reacts dynamically to Ambient Weather Data)
    if tambient < 12:
        weather_style = "Active Freeze Drain Protection"
        weather_icon = "❄️"
        weather_desc = f"Low ambient temperature context ({tambient}°C) programs automated reverse drainage sequences into the master PLC controller, mitigating night freeze pipe damage risks."
    else:
        weather_style = "Overheat Dissipation Shedding"
        weather_icon = "☀️"
        weather_desc = f"Warm design ambient baseline ({tambient}°C) enables an active thermal dump loop to prevent fluid boiling and vapor pressure expansion spikes during factory idle hours."

    # --- BRANDED INDUSTRY THEMES ---
    profiles = {
        "Dairy": {"color": "#1e4620", "accent": "#2E7D32", "bg": "#f4f9f4", "icon": "🥛"},
        "Textile": {"color": "#0d3c61", "accent": "#1565C0", "bg": "#f0f5fa", "icon": "🧵"},
        "Pharmaceutical": {"color": "#4a154b", "accent": "#6A1B9A", "bg": "#faf2fa", "icon": "🧪"},
        "Chemical": {"color": "#E65100", "accent": "#E65100", "bg": "#FFF3E0", "icon": "⚗️"},
        "Food": {"color": "#D32F2F", "accent": "#D32F2F", "bg": "#FFEBEE", "icon": "🍲"}
    }
    p = profiles.get(industry, profiles["Food"])

    # High-End Equipment Configurations injecting the computed physical metrics
    industry_specs = {
        "Dairy": [
            {"label": "🛠️ Piping & Sanitation Framework", "val": f"DN {recommended_dn} SS316 Food-Grade", "desc": f"Sized precisely for {total_flow:,} LPH to stay within strict sanitation velocity standards. Pre-sloped at 1:40 for effortless fluid recovery during CIP cycles."},
            {"label": "🔄 Heat Exchanger (PHE Core)", "val": f"Sanitary Plate Exchanger ({physics['hx_efficiency']}% Eff.)", "desc": f"Electro-polished plates with a calculated LMTD of {physics['lmtd']}°C. Engineered with food-grade gaskets to secure pure pasteurizing streams."},
            {"label": "🔥 Boiler Automation Loop", "val": f"Modulating Backup Integration ({physics['boiler_dependency']}% Load)", "desc": f"Proportional PLC tracking ties directly into your fuel line valve. Automatically fires up to bridge energy deficits if the storage tank water dips below {tout - 4}°C."}
        ],
        "Textile": [
            {"label": "🛠️ Piping & Sanitation Framework", "val": f"DN {recommended_dn} Heavy-Wall Steel", "desc": f"Thick-walled carbon steel featuring an anti-corrosive primer coating. Configured to survive high-pressure utility wash water surges cleanly."},
            {"label": "🔄 Heat Exchanger (PHE Core)", "val": f"Titanium Process Plate Stack ({physics['hx_efficiency']}% Eff.)", "desc": f"High-fouling industrial core working across a localized LMTD of {physics['lmtd']}°C. Resists dye line salts and processing chemical deterioration safely."},
            {"label": "🔥 Boiler Automation Loop", "val": f"Auxiliary Steam Boiler Modulator ({physics['boiler_dependency']}% Load)", "desc": f"Calculated real-time solar preheating reduces primary boiler combustion cycles, translating into immediate plant fuel bill savings."}
        ],
        "Pharmaceutical": [
            {"label": "🛠️ Piping & Sanitation Framework", "val": f"DN {recommended_dn} Electropolished SS316L", "desc": f"Mirror-finished internal lining optimized for {total_flow:,} LPH. Prevents bacterial accumulation or bio-film adhesion to satisfy rigorous industrial auditing criteria."},
            {"label": "🔄 Heat Exchanger (PHE Core)", "val": f"Double-Wall Isolation Stack ({physics['hx_efficiency']}% Eff.)", "desc": f"Dual structural separation physical bar layers running an LMTD of {physics['lmtd']}°C. Completely shields pure plant clean production lines from primary solar fluid circuits."},
            {"label": "🔥 Boiler Automation Loop", "val": f"Clean Steam PID Interlock ({physics['boiler_dependency']}% Load)", "desc": f"Modulates backup input with ultra-precise ±0.5°C threshold tracking, sustaining mandatory temperature setpoints across variable solar cloud coverage windows."}
        ],
        "Chemical": [
            {"label": "🛠️ Piping & Sanitation Framework", "val": f"DN {recommended_dn} Hastelloy Alloy", "desc": f"High-performance alloy lines selected to comfortably tolerate aggressive ambient chemical fumes, thermal stress variations, and process line shifts."},
            {"label": "🔄 Heat Exchanger (PHE Core)", "val": f"Hastelloy Safe Shell Framework ({physics['hx_efficiency']}% Eff.)", "desc": f"Highly reinforced internal matrix working across a calculated LMTD of {physics['lmtd']}°C, completely confining volatile reactive fluids securely."},
            {"label": "🔥 Boiler Automation Loop", "val": f"Interlocked Thermal Boiler Bypass ({physics['boiler_dependency']}% Load)", "desc": f"Automated 3-way mixing loops divert fluids away to standard gas boiler reserves whenever primary solar array storage levels hit cold thermal baselines."}
        ],
        "Food": [
            {"label": "🛠️ Piping & Sanitation Framework", "val": f"DN {recommended_dn} Polished SS304", "desc": f"Equipped entirely with manual quick-release Tri-Clamp connections. Plant operators can instantly disassemble, clean, and re-clamp line sections without welding tools."},
            {"label": "🔄 Heat Exchanger (PHE Core)", "val": f"FDA Gasket Plate Stack ({physics['hx_efficiency']}% Eff.)", "desc": f"Removable plates featuring non-porous silicone seals operating at an LMTD of {physics['lmtd']}°C. Prevents particle buildup between continuous runs."},
            {"label": "🔥 Boiler Automation Loop", "val": f"PLC Direct Burner Interlocking ({physics['boiler_dependency']}% Load)", "desc": f"Reads tank water temperatures via calibrated Pt100 RTD instruments. Fires fuel loops cleanly if solar energy parameters fall short of processing goals."}
        ]
    }
    active_specs = industry_specs.get(industry, industry_specs["Food"])

    # RENDER COMPACT VISUAL DESIGN BLUEPRINT
    html = f"""
    <div style="font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #ffffff; padding: 5px; border-radius: 12px; max-width: 1050px; margin: 0 auto;">
        
        <div style="background: linear-gradient(135deg, {p['color']}, {p['accent']}); color: white; padding: 25px; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px;">
                <div>
                    <h2 style="margin: 0; font-size: 23px; font-weight: 700; letter-spacing: 0.3px;">INPUT-REACTIVE INTEGRATION SOLVER</h2>
                    <p style="margin: 4px 0 0 0; opacity: 0.9; font-size: 13px;">Thermodynamic Sizing Architecture for <b>{industry} Applications</b></p>
                </div>
                <div style="font-size: 34px; background: rgba(255,255,255,0.2); width: 55px; height: 55px; line-height: 55px; text-align: center; border-radius: 50%;">{p['icon']}</div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 15px; margin-top: 25px; background: rgba(0,0,0,0.15); padding: 15px; border-radius: 10px;">
                <div>
                    <div style="font-size: 11px; opacity: 0.85; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Calculated Aperture Area</div>
                    <div style="font-size: 21px; font-weight: 700; margin: 2px 0 4px 0; color: #ffd54f;">{physics['aperture_area_m2']} m²</div>
                    <div style="font-size: 11px; opacity: 0.8;">Required Net Solar Surface Size</div>
                </div>
                <div style="border-left: 1px solid rgba(255,255,255,0.2); padding-left: 15px;">
                    <div style="font-size: 11px; opacity: 0.85; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Daily System Heat Energy</div>
                    <div style="font-size: 21px; font-weight: 700; margin: 2px 0 4px 0;">{physics['daily_energy_kwh']} kWh</div>
                    <div style="font-size: 11px; opacity: 0.8;">Thermal Plant Load Met</div>
                </div>
                <div style="border-left: 1px solid rgba(255,255,255,0.2); padding-left: 15px;">
                    <div style="font-size: 11px; opacity: 0.85; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Estimated Optical Eff.</div>
                    <div style="font-size: 21px; font-weight: 700; margin: 2px 0 4px 0;">{physics['efficiency_pct']}%</div>
                    <div style="font-size: 11px; opacity: 0.8;">At Operating Fluid Delta</div>
                </div>
                <div style="border-left: 1px solid rgba(255,255,255,0.2); padding-left: 15px;">
                    <div style="font-size: 11px; opacity: 0.85; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px;">Main Line Diameter</div>
                    <div style="font-size: 21px; font-weight: 700; margin: 2px 0 4px 0; color: #ffffff;">DN {recommended_dn}</div>
                    <div style="font-size: 11px; opacity: 0.8;">Optimized for Fluid Velocity</div>
                </div>
            </div>
        </div>

        <h3 style="color: #2C3E50; font-size: 14px; font-weight: 700; text-transform: uppercase; margin: 0 0 15px 5px; letter-spacing: 0.5px;">Physics-Driven Component Mapping</h3>

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
                        <span>Loss Window</span><span style="color: {p['accent']};">HX Efficiency: {physics['hx_efficiency']}%</span>
                    </div>
                    <div style="background: #e2e8f0; height: 10px; border-radius: 5px; margin-bottom: 12px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, {p['accent']}, #81c784); width: {physics['hx_efficiency']}%; height: 100%;"></div>
                    </div>
                    <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5; text-align: justify;">{active_specs[1]['desc']}</p>
                </div>
            </div>

            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border: 1px solid rgba(0,0,0,0.05); border-top: 4px solid {p['accent']}; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h4 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 15px; font-weight: 700;">{active_specs[2]['label']}</h4>
                    <div style="display: flex; justify-content: space-between; font-size: 11px; color: #666; margin-bottom: 4px; font-weight: 600;">
                        <span>Solar Saving Coverage</span><span style="color: #d32f2f;">Auxiliary Boiler Load: {physics['boiler_dependency']}%</span>
                    </div>
                    <div style="background: #e2e8f0; height: 10px; border-radius: 5px; margin-bottom: 12px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #ffb74d, #e53935); width: {physics['boiler_dependency']}%; height: 100%;"></div>
                    </div>
                    <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5; text-align: justify;">{active_specs[2]['desc']}</p>
                </div>
            </div>

            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border: 1px solid rgba(0,0,0,0.05); border-top: 4px solid {p['accent']}; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h4 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 15px; font-weight: 700;">💧 Fluid Circulation Regime</h4>
                    <div style="display: flex; justify-content: space-between; font-size: 11px; color: #777; margin-bottom: 4px; font-weight: 600;">
                        <span>Low Flow Speed</span><span style="color: {flow_color};">{flow_style}</span><span>High Surge Speed</span>
                    </div>
                    <div style="background: #e2e8f0; height: 10px; border-radius: 5px; margin-bottom: 12px; overflow: hidden;">
                        <div style="background: {flow_color}; width: {flow_bar}%; height: 100%;"></div>
                    </div>
                    <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5; text-align: justify;">{flow_desc}</p>
                </div>
            </div>

            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border: 1px solid rgba(0,0,0,0.05); border-top: 4px solid {p['accent']}; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h4 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 15px; font-weight: 700;">🔄 Energy Flow Layout</h4>
                    <div style="display: flex; justify-content: space-between; font-size: 11px; color: #777; margin-bottom: 4px; font-weight: 600;">
                        <span>Single-Pass Loop</span><span style="color: {p['accent']};">{recirc_style}</span><span>Recirculation Loop</span>
                    </div>
                    <div style="background: #e2e8f0; height: 10px; border-radius: 5px; margin-bottom: 12px; overflow: hidden;">
                        <div style="background: {p['accent']}; width: {recirc_bar}; height: 100%;"></div>
                    </div>
                    <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5; text-align: justify;">{recirc_desc}</p>
                </div>
            </div>

            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border: 1px solid rgba(0,0,0,0.05); border-top: 4px solid {p['accent']}; display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <h4 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 15px; font-weight: 700;">{weather_icon} Climate Safety Logic</h4>
                    <div style="background: #ffffff; padding: 8px 12px; border-radius: 6px; font-size: 13px; font-weight: 700; color: #333; border-left: 3px solid #e53935; margin-bottom: 12px; box-shadow: inset 0 1px 2px rgba(0,0,0,0.02);">
                        {weather_style}
                    </div>
                    <p style="margin: 0; font-size: 12.5px; color: #4F5D73; line-height: 1.5; text-align: justify;">{weather_desc}</p>
                </div>
            </div>

        </div>

        <div style="margin-top: 25px; padding: 15px; background-color: #fffde7; border-left: 5px solid #fbc02d; border-radius: 4px; font-size: 12.5px; color: #5c501a; line-height: 1.5;">
            <b>Live Engineering Sizing Status:</b> This dashboard module uses active fluid-dynamic math models to adjust mechanical integration parameters. Altering the user's required temperature variables recalculates the <b>Plate Heat Exchanger</b> log temperature profiles and safety bypass parameters in real time.
        </div>
    </div>
    """
    return html
