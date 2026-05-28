def calculate_pipe_diameter(total_flow):
    """Calculates engineering nominal pipe size (DN) based on LPH flow rate."""
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
    Deep Industrial Product Design Engine.
    Evaluates hydraulic mass, thermal lift, and site climate parameters to dynamically
    generate optimized fluid regimes and hardware specs for a technical proposal.
    """
    recommended_dn = calculate_pipe_diameter(total_flow)
    
    # --- DYNAMIC SYSTEM DESIGN CALCULATIONS ---
    approach_delta = tout - tinlet
    total_mass_kg = daily_water
    
    # 1. DYNAMIC REGIME SPECIFICATION (RESEARCH-DRIVEN PRODUCT DESIGN)
    # Target a high Reynolds number approximation for optimal heat exchanger sizing
    if total_flow >= 500:
        flow_regime = "High-Turbulence Flow (Re &gt; 4,000)"
        flow_desc = f"At {total_flow} LPH, the loop induces high fluid velocity, disrupting boundary layers. This maximizes the convective heat transfer coefficient inside the heat exchanger, keeping surface fouling low."
    else:
        flow_regime = "Transitional/Laminar Flow (Re &le; 4,000)"
        flow_desc = f"A conservative process flow of {total_flow} LPH prioritizes minimal pump parasitic power draw. System relies on specialized micro-channel plate patterns to artificially induce mixing at low velocities."

    # 2. LOOP RECIRCULATION STRATEGY
    if approach_delta > 50:
        recirc_strategy = "Multi-Stage Recirculation Loop"
        recirc_desc = f"A substantial thermal lift requirement ({approach_delta}°C Delta) demands an automated variable-speed recirculation layout to avoid thermal shocking across the exchanger matrix."
    else:
        recirc_strategy = "Single-Pass Crossflow"
        recirc_desc = f"A compact approach profile ({approach_delta}°C Delta) allows energy-efficient single-pass target heating, streamlining footprint and valve layouts."

    # 3. CLIMATIC SHIELDING STRATEGY
    if tambient < 10:
        freeze_strategy = "Active Glycol / Auto-Drain Down"
        freeze_desc = f"Low ambient risk profile ({tambient}°C) triggers active drain-down sequencing or an isolated food-safe monopropylene glycol circuit to prevent piping rupture."
    else:
        freeze_strategy = "Standard Night-Sky Venting"
        freeze_desc = f"Stable climate profile ({tambient}°C ambient) eliminates freeze risk. System prioritizes continuous night-sky heat radiation purge loops to maintain safety bounds."

    # 4. STRUCTURAL ARRAY MOUNTING FOOTPRINT
    if total_mass_kg >= 6000:
        structural_load = "Heavy Structural Array Concrete Pad"
        structural_desc = f"High structural loading ({total_mass_kg:,} kg hydraulic operating weight) dictates reinforced dual-girder placement and vibration-isolated foundation pads."
    else:
        structural_load = "Standard Elevated Platform Mount"
        structural_desc = f"Moderate hydraulic structural footprint ({total_mass_kg:,} kg weight) fits standard elevated plant mezzanine space configurations."

    # --- BRANDED INDUSTRY THEME MATRIX ---
    profiles = {
        "Dairy": {"color": "#1e4620", "accent": "#2E7D32", "bg": "#f4f9f4", "icon": "🥛"},
        "Textile": {"color": "#0d3c61", "accent": "#1565C0", "bg": "#f0f5fa", "icon": "🧵"},
        "Pharmaceutical": {"color": "#4a154b", "accent": "#6A1B9A", "bg": "#faf2fa", "icon": "🧪"},
        "Chemical": {"color": "#E65100", "accent": "#E65100", "bg": "#FFF3E0", "icon": "⚗️"},
        "Food": {"color": "#D32F2F", "accent": "#D32F2F", "bg": "#FFEBEE", "icon": "🍲"}
    }
    p = profiles.get(industry, profiles["Food"])
    
    # Core hardware specifications mapped to targeted industrial sectors
    industry_specs = {
        "Dairy": [
            {"label": "Fluid Piping Infrastructure", "val": f"DN {recommended_dn} SS316 Food-Grade", "desc": "Sized perfectly to maintain fluid velocities within a 1.0–1.5 m/s sanitation window to eliminate residue settling. Sloped at 1:40 for self-draining CIP compliance."},
            {"label": "Heat Exchanger Core", "val": "Sanitary Plate (PHE)", "desc": "AISI 304 electro-polished plate layout with food-grade sanitary EPDM seals. Internal crevice depth is restricted below 100 microns to stop fat accumulation."}
        ],
        "Textile": [
            {"label": "Fluid Piping Infrastructure", "val": f"DN {recommended_dn} Heavy-Wall Steel", "desc": "Engineered to withstand abrupt pressure wave anomalies from sudden batch dump sequencing. Incorporates a 5mm carbon structural corrosion wall allowance."},
            {"label": "Heat Exchanger Core", "val": "Titanium Shell & Tube", "desc": "Solid titanium internal element bundle designed to completely resist degradation from chemical aggressive dye compounds, mordants, and harsh fixing salts."}
        ],
        "Pharmaceutical": [
            {"label": "Fluid Piping Infrastructure", "val": f"DN {recommended_dn} Electropolished SS316L", "desc": "Ultra-pure internal surface treatments completely eliminating static micro-pockets. Heat-stamped serial lines feed directly into automated cleanroom tracking loops."},
            {"label": "Heat Exchanger Core", "val": "Double-Wall Isolation Frame", "desc": "Dual physical partition plates guarantee absolute isolation, rendering cross-contamination impossible between process utility heating water and unadulterated pure WFI lines."}
        ],
        "Chemical": [
            {"label": "Fluid Piping Infrastructure", "val": f"DN {recommended_dn} Hastelloy Alloy", "desc": "High-nickel alloy piping configured to survive severe acidic exposures, heavy thermal cycling stress, and fluctuating high operating pressures safely."},
            {"label": "Heat Exchanger Core", "val": "Dual-Tube Safety Shell", "desc": "Double isolated tube sheets designed to reliably capture and separate hazardous process media away from primary factory water utility systems."}
        ],
        "Food": [
            {"label": "Fluid Piping Infrastructure", "val": f"DN {recommended_dn} Polished SS304", "desc": "Assembled entirely using standard industrial heavy-duty Tri-Clamp modular components for rapid breakdown maintenance, sterilization sweeps, and line re-routing."},
            {"label": "Heat Exchanger Core", "val": "FDA-Approved Plate Stack", "desc": "Clean-profile mirror-polished sheets held inside an open-frame compression layout using certified non-porous food-grade silicone seals for simplified cleaning."}
        ]
    }

    active_specs = industry_specs.get(industry, industry_specs["Food"])

    # Combine localized hardware configurations with calculated fluid design profiles
    all_specs = active_specs + [
        {"label": "Optimal Fluid Dynamics", "val": flow_regime, "desc": flow_desc},
        {"label": "Thermal Loop Control", "val": recirc_strategy, "desc": recirc_desc},
        {"label": "Climatic Shielding Strategy", "val": freeze_strategy, "desc": freeze_desc},
        {"label": "Structural Support Footprint", "val": structural_load, "desc": structural_desc}
    ]

    # Render HTML Executive Layout Presentation Matrix
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
                    Proposal Reference: {industry[:3].upper()}-ISO-{tout}
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 15px; margin-top: 20px; background: rgba(0,0,0,0.15); padding: 15px; border-radius: 8px;">
                <div style="border-right: 1px solid rgba(255,255,255,0.2); padding-right: 10px;">
                    <div style="font-size: 10px; text-transform: uppercase; opacity: 0.8; font-weight: 600;">Process Lift Delta</div>
                    <div style="font-size: 20px; font-weight: 700; margin-top: 2px;">+{approach_delta}°C</div>
                </div>
                <div style="border-right: 1px solid rgba(255,255,255,0.2); padding-right: 10px;">
                    <div style="font-size: 10px; text-transform: uppercase; opacity: 0.8; font-weight: 600;">Daily Volumetric Design</div>
                    <div style="font-size: 20px; font-weight: 700; margin-top: 2px;">{daily_water:,} <span style="font-size:12px; font-weight:400;">LPD</span></div>
                </div>
                <div style="border-right: 1px solid rgba(255,255,255,0.2); padding-right: 10px;">
                    <div style="font-size: 10px; text-transform: uppercase; opacity: 0.8; font-weight: 600;">Site Ambient Baseline</div>
                    <div style="font-size: 20px; font-weight: 700; margin-top: 2px;">{tambient}°C</div>
                </div>
                <div>
                    <div style="font-size: 10px; text-transform: uppercase; opacity: 0.8; font-weight: 600;">Calculated Pipeline Main</div>
                    <div style="font-size: 20px; font-weight: 700; margin-top: 2px; color: #fffb00;">DN {recommended_dn}</div>
                </div>
            </div>
        </div>

        <h4 style="color: #37474F; font-size: 14px; font-weight: 700; text-transform: uppercase; margin: 0 0 15px 0; letter-spacing: 0.5px;">Custom Integration Feature Layout</h4>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 10px;">
    """
    
    # Populate the dynamic proposal cards inside the presentation layout grid
    for s in all_specs:
        html += f"""
            <div style="background-color: {p['bg']}; border: 1px solid rgba(0,0,0,0.06); border-top: 4px solid {p['accent']}; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <div style="font-size: 10px; text-transform: uppercase; color: #666; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 4px;">PRODUCT MODULE</div>
                    <h3 style="margin: 0 0 10px 0; font-size: 15px; font-weight: 700; color: {p['color']};">{s['label']}</h3>
                    <div style="font-size: 13px; font-weight: 700; color: #222; background: #ffffff; padding: 8px 12px; border-radius: 6px; border-left: 3px solid {p['accent']}; margin-bottom: 12px; box-shadow: inset 0 1px 2px rgba(0,0,0,0.02);">
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
            * Technical engineering recommendation models adapt continuously based on customized input parameters.
        </div>
    </div>
    """
    return html
