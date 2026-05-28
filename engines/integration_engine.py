def calculate_pipe_diameter(total_flow):
    """
    Calculates recommended nominal pipe diameter (DN in mm) 
    based on continuous liquid flow rates (LPH) to target an 
    economical, high-efficiency velocity window of 1.0 to 1.5 m/s.
    """
    if total_flow <= 150:
        return "20"   # DN20 (3/4")
    elif total_flow <= 400:
        return "25"   # DN25 (1")
    elif total_flow <= 900:
        return "32"   # DN32 (1-1/4")
    elif total_flow <= 1500:
        return "40"   # DN40 (1-1/2")
    elif total_flow <= 3000:
        return "50"   # DN50 (2")
    elif total_flow <= 6000:
        return "65"   # DN65 (2-1/2")
    elif total_flow <= 12000:
        return "80"   # DN80 (3")
    else:
        return "100"  # DN100 (4")


def recommendations(industry="Dairy", tout=80, daily_water=5000, total_flow=250):
    """
    Generates high-end, visually striking HTML component spec blocks 
    tailored specifically for deployment within a web dashboard interface.
    
    Replaces boring bullet lists with structured, color-coded enterprise cards.
    """
    recommended_dn = calculate_pipe_diameter(total_flow)
    
    # 1. INDUSTRY DEFINITIONS & METRIC MAPPINGS
    specs = {
        "Dairy": {
            "theme_color": "#2E7D32",   # Deep Sanitary Green
            "bg_light": "#E8F5E9",
            "icon": "🥛",
            "cards": [
                {
                    "title": "Plant Fluid Piping",
                    "badge": f"DN {recommended_dn} Standard",
                    "details": [
                        f"Recommended Main Line Size: <b>DN {recommended_dn}</b> optimized to achieve a fluid scouring velocity of 1.0–1.5 m/s to completely eliminate organic sediment settling.",
                        "Material Standard: <b>Food-Grade Stainless Steel (SS316)</b> ensuring zero risk of bacterial contamination or pitting across active pasteurization runs.",
                        "Piping Slope Strategy: Pre-install with a downward drainage pitch of at least <b>1:40</b> directly targeting process collection basins for effortless cleaning cycles.",
                        "Thermal Insulation: <b>50mm high-density mineral wool clad in a rugged aluminum protective shell</b> to eliminate heat radiation across plant floors."
                    ]
                },
                {
                    "title": "Thermal Heat Exchanger System",
                    "badge": "Sanitary PHE",
                    "details": [
                        "Hardware Configuration: High-efficiency <b>Sanitary Plate Heat Exchanger (PHE)</b> utilizing a flexible 50-to-100 plate stack layout.",
                        "Wetted Metal Plates: Precision stamped <b>AISI 304 Stainless Steel plates</b> polished to match product purity protocols.",
                        "Sealing Gaskets: <b>Sanitary-grade EPDM rubber seals</b> engineered to maintain seal compression across thousands of rapid thermal cycles.",
                        "Hygienic Profile: Built with a specialized smooth geometry maintaining a <b>crevice depth under 100 microns</b> to eliminate fat buildup zones."
                    ]
                },
                {
                    "title": "Plant Integration & Thermal Re-use",
                    "badge": f"Target: {tout}°C Max",
                    "details": [
                        "Clean-In-Place (CIP) Interface: Connects directly to main plant wash loops, turning captured solar heat into instant energy for high-temperature sanitary flushes.",
                        "Storage Tank Interior: Insulated containment units specify an ultra-smooth internal finish of <b>Ra &lt; 0.8 microns</b> to prevent bacterial anchoring.",
                        "Thermal Extraction Circuit: Closed-loop design entirely isolates secondary solar heat transfers from raw, unpasteurized product streams."
                    ]
                },
                {
                    "title": "Automation & Safety Controls",
                    "badge": "PLC Integrated",
                    "details": [
                        "Control System Hardware: <b>Programmable Logic Controller (PLC)</b> loaded with preset recipe profiles for automated heating, cleaning, and standby modes.",
                        "Precision Sensors: High-accuracy dual <b>RTD (Pt100) sensors</b> monitoring cross-loop temperature profiles to within ±0.5°C.",
                        "Automated Boiler Overrides: Motorized 3-way modulating valves auto-route delivery pipelines to the backup steam boiler on low-radiation or high-demand cycles.",
                        "Hardware Safety Interlocks: High-limit fast-acting relief systems instantly bypass and isolate solar field loops if internal line pressures surge."
                    ]
                },
                {
                    "title": "Regulatory Compliance & Verification",
                    "badge": "Auditable Standards",
                    "details": [
                        "Sanitation Benchmark: Deploys 100% certified <b>3-A Sanitary Standards</b> components for all fluid contact faces.",
                        "Quality Verification: Manufacturing documentation patterns map fully to active <b>HACCP guidelines</b> and <b>ISO 9001</b> factory frameworks."
                    ]
                }
            ]
        },
        
        "Textile": {
            "theme_color": "#1565C0",   # Indigo Blue
            "bg_light": "#E3F2FD",
            "icon": "🧵",
            "cards": [
                {
                    "title": "Plant Fluid Piping",
                    "badge": f"DN {recommended_dn} Heavy Wall",
                    "details": [
                        f"Recommended Main Line Size: <b>DN {recommended_dn}</b> optimized to handle high-volume batch discharge dumps without encountering pipeline water-hammer.",
                        "Material Standard: Heavy-duty <b>Carbon Steel or Ductile Iron</b> featuring a thick 5mm sacrificial corrosion margin to withstand abrasive raw water treatment values.",
                        "Thermal Insulation: <b>75mm asbestos-free silicate insulation</b> enclosed in dense protective canvas wrapping tailored for aggressive dye house room floors."
                    ]
                },
                {
                    "title": "Thermal Buffer Storage Systems",
                    "badge": f"{daily_water} LPD Buffer Tank",
                    "details": [
                        "Storage Strategy: Dedicated <b>Thermal Buffer Storage Tanks</b> built out to handle 20-30% of total plant daily load metrics to smooth out sudden batch demand curves.",
                        "Stratification Design: High-aspect vertical storage vessels incorporate internal structural diffusion chimneys to isolate hot water from return lines.",
                        "Capacity Target: Scaled with active buffer configurations allowing massive operational reserves to accommodate changing textile processing shifts."
                    ]
                },
                {
                    "title": "Thermal Heat Exchanger System",
                    "badge": "Shell & Tube",
                    "details": [
                        "Hardware Configuration: Heavy-duty <b>Shell & Tube Heat Exchanger</b> purpose-built to process high-fouling, raw fabric wastewater discharge streams.",
                        "Wetted Tubes Material: Deploys <b>Solid Titanium Tube Elements</b> providing defense against harsh dyes, caustic bleaching solutions, and fixing salts.",
                        "Direct Boiler Interface: Outfitted with built-in utility steam connection ports to quickly balance loop temperatures during extreme operational phases."
                    ]
                },
                {
                    "title": "Dye House Process Integration",
                    "badge": "Multi-Zone Circuit",
                    "details": [
                        "Multi-Circuit Heat Zoning: Distributed piping headers run independent supply lines to provide varying process temperatures across different areas of the facility.",
                        "Dye Vat Coupling: Direct thermal integration into individual dye vats using high-speed regulating control valves.",
                        "Wastewater Energy Capture: Integrated heat exchangers harvest residual energy from hot wastewater dumps to preheat fresh incoming utility water."
                    ]
                },
                {
                    "title": "Automation & Safety Controls",
                    "badge": "Batch Scheduler",
                    "details": [
                        "Production Scheduler Interface: Control software matches energy delivery to active batch schedules across the plant floors.",
                        "Temperature Ramping Control: Automated control loops provide smooth temperature ramping curves (±2°C precision) for critical fabric dyeing runs.",
                        "Pressure Constraints: Heavy pressure relief infrastructure caps line pressures at 4 to 6 bar."
                    ]
                }
            ]
        },
        
        "Pharmaceutical": {
            "theme_color": "#6A1B9A",   # Pure Purple
            "bg_light": "#F3E5F5",
            "icon": "🧪",
            "cards": [
                {
                    "title": "Plant Fluid Piping",
                    "badge": f"DN {recommended_dn} Electropolished",
                    "details": [
                        f"Recommended Main Line Size: <b>DN {recommended_dn}</b> engineered with extreme precision to secure seamless loop flow and remove fluid stagnation pockets.",
                        "Material Standard: <b>Ultra-pure Electropolished Stainless Steel (SS316L)</b> providing non-reactive, clean fluid delivery.",
                        "Traceability Logs: Every pipeline assembly is heat-stamped and mapped for strict <b>FDA/GMP material qualification audits</b>."
                    ]
                },
                {
                    "title": "Thermal Heat Exchanger System",
                    "badge": "Double-Wall Frame",
                    "details": [
                        "Hardware Design: <b>Double-Tube or Certified Pharmaceutical Grade Plate Exchanger</b> delivering zero-leak separation protocols.",
                        "Sealing Elements: <b>Cleanroom-certified, non-degrading fluoropolymer gaskets</b> compliant with high-purity Water-For-Injection (WFI) streams.",
                        "Structural Integrity: High-strength configuration tested and rated for heavy-duty industrial processing limits up to <b>10 bar</b>."
                    ]
                },
                {
                    "title": "Precision Instrumentation",
                    "badge": "±0.1°C Calibrated",
                    "details": [
                        "Sensor Benchmarks: Double-calibrated <b>RTD sensor networks (accurate to ±0.1°C)</b> deployed at critical regulatory control nodes.",
                        "Data Archival Automation: 24/7 digital data acquisition system logging compliance metrics for batch audit reviews.",
                        "Alarm Management: Automated pressure sensors featuring hard-coded software limit triggers to catch line anomalies instantaneously."
                    ]
                },
                {
                    "title": "Plant Integration & Validation",
                    "badge": "IQ/OQ/PQ Ready",
                    "details": [
                        "Validation Standards: Complete validation documentation pack featuring full <b>Installation, Operation, and Performance Qualification (IQ/OQ/PQ)</b> files.",
                        "System Isolation: Built with clean three-way diversion valves to instantly isolate and loops if fluid temperatures step out of alignment.",
                        "Sanitary Trapping: Features automatic sterile steam traps ensuring zero ambient back-siphoning vector risks."
                    ]
                },
                {
                    "title": "Automation & Safety Controls",
                    "badge": "21 CFR Part 11",
                    "details": [
                        "Regulatory Software Stack: Advanced PLC controllers built fully compliant with <b>FDA 21 CFR Part 11 electronic data validation metrics</b>.",
                        "Audit Tracking Automation: Tamper-proof internal logging loops record every configuration change made across the system.",
                        "Deviation Logic: Auto-tripping logic flags instant warnings to plant managers if a processing run slips by more than 2°C."
                    ]
                }
            ]
        },

        "Chemical": {
            "theme_color": "#E65100",   # Warning Orange / Amber
            "bg_light": "#FFF3E0",
            "icon": "⚗️",
            "cards": [
                {
                    "title": "Plant Fluid Piping",
                    "badge": f"DN {recommended_dn} Heavy Wall",
                    "details": [
                        f"Recommended Main Line Size: <b>DN {recommended_dn}</b> precisely calculated to optimize flow velocity, balancing friction loss against required volume delivery.",
                        "Material Standard: <b>Heavy-gauge Carbon Steel or Hastelloy Alloys</b> protected with specialized internal anti-corrosion chemical linings.",
                        "Pressure Bounds: All piping runs and connection couplings utilize industrial high-strength fittings rated for severe process pressures."
                    ]
                },
                {
                    "title": "Thermal Heat Exchanger System",
                    "badge": "Double-Wall Isolation",
                    "details": [
                        "Hardware Configuration: Fully isolated <b>Double-Wall Shell or Plate Exchanger</b> ensuring hazardous process media can never mix into storage lines.",
                        "Wetted Tubes Material: Specialized <b>Inconel or Solid Titanium alloy sets</b> to withstand reactive, aggressive process chemistries.",
                        "Safety Infrastructure: Outfitted with hardware burst discs and pressure relief lines targeting containment sumps."
                    ]
                },
                {
                    "title": "Process Integration & Safety Zones",
                    "badge": "ATEX Compliant",
                    "details": [
                        "Multi-Tiered Thermal Zoning: Independent flow control circuits regulate temperature profiles across sequential reactor stages.",
                        "Explosion-Proof Compliance: All localized wiring, motors, and instrumentation meet strict <b>ATEX/IECEx explosion-proof specifications</b>.",
                        "Secondary Safety Containment: Process pipelines run inside protective secondary outer sleeves to manage line leaks or breaks safely."
                    ]
                },
                {
                    "title": "Automation & Safety Controls",
                    "badge": "Ramp/Soak Profiles",
                    "details": [
                        "Advanced Controls Strategy: Process controllers deploy automated heating and cooling curves to manage reaction loops safely.",
                        "Fault Tolerance Interlocks: Automated bypass valves trigger immediately if a pump fails, maintaining safe internal temperature balances.",
                        "Real-time Alarm Management: Distributed Control System (DCS) links provide instantaneous notifications on tracking variances."
                    ]
                }
            ]
        },

        "Food": {
            "theme_color": "#D32F2F",   # Production Red
            "bg_light": "#FFEBEE",
            "icon": "🍲",
            "cards": [
                {
                    "title": "Plant Fluid Piping",
                    "badge": f"DN {recommended_dn} Food-Safe",
                    "details": [
                        f"Recommended Main Line Size: <b>DN {recommended_dn}</b> calibrated to maintain clean, high-velocity sweeps throughout daily system operations.",
                        "Material Standard: <b>Polished Stainless Steel (SS304 or SS316)</b> offering high oxidation resistance and perfectly clean sanitary fluid lines.",
                        "Quick-Release Assembly: Outfitted with standardized industrial <b>Tri-Clamp sanitary fittings</b> for easy, tool-free line checks and internal component sweeps."
                    ]
                },
                {
                    "title": "Thermal Heat Exchanger System",
                    "badge": "FDA-Approved Plate",
                    "details": [
                        "Hardware Geometry: <b>Sanitary Frame Heat Exchanger</b> with an ultra-smooth plate face profile to eliminate bacterial anchoring vectors.",
                        "Sealing Elements: <b>FDA-certified, non-porous food-grade silicone or EPDM gaskets</b> designed for continuous clean operation.",
                        "Passivated Surfaces: External structural surfaces receive an acid-bath chemical passivation layout to ensure dynamic wear resilience."
                    ]
                },
                {
                    "title": "Plant Integration & Food Safety",
                    "badge": "HACCP Data Logging",
                    "details": [
                        "Direct Production Splicing: Solar lines connect smoothly to pre-heating stations for jacketed cooking kettles, cleanups, and boiler feed lines.",
                        "Loop Isolation Strategy: Dual-loop barriers prevent solar storage fluids from ever interacting with food product streams.",
                        "HACCP Data Interface: Built-in data loggers continuously record processing line temperatures to fulfill critical food safety audit guidelines."
                    ]
                },
                {
                    "title": "Automation & Safety Controls",
                    "badge": f"Trip: {tout}°C",
                    "details": [
                        "Daily Sanitization Cycles: Control systems schedule automatic thermal disinfection sequences during down-time hours.",
                        "Boiler Integration Logic: Automatic control systems switch to utility gas boilers when solar storage reserves empty below the target value.",
                        "High-Limit Thermal Trips: Safety systems isolate the solar field if delivery lines exceed the design threshold of <b>{tout}°C</b>."
                    ]
                }
            ]
        }
    }

    # Fallback to Food if the selected industry isn't explicitly defined
    selected_data = specs.get(industry, specs["Food"])
    theme = selected_data["theme_color"]
    bg_card = selected_data["bg_light"]
    icon = selected_data["icon"]

    # 2. RENDER SUMMARY METRIC HEADER BANNER
    html_output = f"""
    <div style='font-family: Arial, sans-serif; margin-bottom: 25px;'>
        <div style='display: flex; align-items: center; background-color: {theme}; color: white; padding: 15px; border-radius: 8px 8px 0 0; margin-bottom: 0;'>
            <span style='font-size: 24px; margin-right: 12px;'>{icon}</span>
            <h2 style='margin: 0; font-size: 18px; font-weight: bold; letter-spacing: 0.5px;'>{industry.upper()} INTEGRATION SPECIFICATION OVERVIEW</h2>
        </div>
        <table style='width: 100%; border-collapse: collapse; background-color: #FAFAFA; border: 1px solid #CFD8DC; border-top: none; font-size: 13px;'>
            <tr style='background-color: #ECEFF1;'>
                <td style='padding: 10px; font-weight: bold; color: #37474F; border-right: 1px solid #CFD8DC;'>Target Temperature</td>
                <td style='padding: 10px; font-weight: bold; color: #37474F; border-right: 1px solid #CFD8DC;'>Daily Volume Capacity</td>
                <td style='padding: 10px; font-weight: bold; color: #37474F;'>Calculated Pipe Line Size</td>
            </tr>
            <tr>
                <td style='padding: 12px; color: #455A64; border-right: 1px solid #CFD8DC; font-size: 15px; font-weight: bold;'>{tout}°C</td>
                <td style='padding: 12px; color: #455A64; border-right: 1px solid #CFD8DC; font-size: 15px; font-weight: bold;'>{daily_water:,} LPD</td>
                <td style='padding: 12px; color: #D32F2F; font-size: 15px; font-weight: bold;'>DN {recommended_dn}</td>
            </tr>
        </table>
    </div>
    """

    # 3. GENERATE THE COMPONENT VISUAL CARDS
    for card in selected_data["cards"]:
        detail_items_html = ""
        for detail in card["details"]:
            detail_items_html += f"""
            <li style='margin-bottom: 8px; color: #37474F; line-height: 1.5;'>
                {detail}
            </li>
            """
            
        html_output += f"""
        <div style='font-family: Arial, sans-serif; background-color: #FFFFFF; border-left: 5px solid {theme}; border-top: 1px solid #E0E0E0; border-right: 1px solid #E0E0E0; border-bottom: 1px solid #E0E0E0; border-radius: 4px; padding: 18px; margin-bottom: 16px; box-shadow: 0 2px 4px rgba(0,0,0,0.04);'>
            <div style='display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #ECEFF1; padding-bottom: 8px; margin-bottom: 12px;'>
                <h3 style='margin: 0; color: {theme}; font-size: 15px; font-weight: bold;'>{card["title"]}</h3>
                <span style='background-color: {bg_card}; color: {theme}; padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold; text-transform: uppercase;'>{card["badge"]}</span>
            </div>
            <ul style='margin: 0; padding-left: 20px;'>
                {detail_items_html}
            </ul>
        </div>
        """
        
    return html_output
