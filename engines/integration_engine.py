def recommendations(industry="Dairy", tout=80, daily_water=5000, total_flow=250):
    """
    Generates tailored industrial integration blueprints.
    Rephrased to clearly explain the business and mechanical justification for each component
    so non-technical stakeholders can easily follow the integration requirements.
    """
    
    # Calculate an accurate process velocity line diameter based on flow rate
    recommended_dn = calculate_pipe_diameter(total_flow)
    
    recommendations_dict = {
        "Dairy": {
            "Plant Fluid Piping": [
                f"Recommended Main Line Size: **DN {recommended_dn}** (Optimized to maintain a fluid velocity of 1.0–1.5 m/s, preventing sediment settling).",
                "Material Standard: **Food-Grade Stainless Steel (SS316)** to prevent bacterial contamination and maintain pasteurization sanitation standards.",
                "Piping Slope Strategy: Install with a downward slope of at least **1:40** toward the drainage basins to ensure easy fluid removal during cleaning.",
                "Thermal Insulation: **50mm high-density mineral wool clad in protective rugged aluminum sheet metal** to ensure zero heat leakage across unconditioned plant floors."
            ],
            "Thermal Heat Exchanger System": [
                "Hardware Type: **Sanitary Plate Heat Exchanger (PHE)** configured with a 50-to-100 plate stack depending on final operational pressure drops.",
                "Wetted Plates Material: **High-corrosion resistant AISI 304 Stainless Steel** matching process water purity rules.",
                "Sealing Gaskets: **Sanitary-grade EPDM rubber seals** capable of withstand constant thermal cycles without drying or cracking.",
                "Hygienic Geometry: Designed with an ultra-smooth profile (crevice depths below 100 microns) to prevent active milk fat or organic buildup."
            ],
            "Plant Integration & Thermal Re-use": [
                "Clean-In-Place (CIP) Interface: Seamlessly connects directly to the wash lines, utilizing solar energy to heat raw cleaning water to the needed temperature.",
                "Sanitary Storage Tank Finishes: Storage tanks feature an ultra-smooth, highly polished internal finish (**Ra < 0.8 microns**) to completely eliminate bacterial anchor zones.",
                "Thermal Extraction Circuit: Built with an isolated closed-loop heat recovery pipeline, keeping incoming solar loop fluids separated from milk cooling operations."
            ],
            "Automation & Safety Controls": [
                "Control System Hardware: **Programmable Logic Controller (PLC)** equipped with automated process profiles for cleaning, production, and standby modes.",
                "Precision Instrumentation: Dual industrial **RTD (Pt100) temperature sensors** tracking fluid behavior down to a sharp ±0.5°C tolerance.",
                "Automated Boiler Overrides: Automated valve networks route fluid to the backup fuel boiler on cloudy days or during high production runs.",
                "Industrial Safety Interlocks: High-limit shutoff valves instantly isolate the solar field if line pressures spike or fluid temperatures approach boiling."
            ],
            "Regulatory Compliance & Verification": [
                "Quality Benchmark: Every fluid component meets strict **3-A Sanitary Standards** for food-grade processing.",
                "Quality Certifications: System engineering frameworks are built fully compliant with **HACCP documentation metrics** and **ISO 9001** standards."
            ]
        },
        
        "Textile": {
            "Plant Fluid Piping": [
                f"Recommended Main Line Size: **DN {recommended_dn}** (Sized to handle high-volume batch dumps without causing fluid hammering).",
                "Material Standard: **Heavy-wall Carbon Steel or Ductile Iron** treated with a 5mm sacrificial corrosion allowance to handle raw water chemistry.",
                "Thermal Insulation: **75mm robust asbestos-free silicate insulation** wrapped in protective outer canvas jackets to protect fabric processing floors."
            ],
            "Thermal Buffer Storage Systems": [
                "Sizing Benchmark: **Dedicated Thermal Buffer Storage** sized for 20-30% of the entire plant's daily volume requirement to manage sudden demand spikes.",
                "Stratification Design: Vertical storage vessels utilize an internal physical column to separate hot water from cold water without mixing.",
                "Operational Volume Guidance: Provisions a standalone buffer configuration capable of holding large volumes depending on daily batch schedules."
            ],
            "Thermal Heat Exchanger System": [
                "Hardware Type: **Rugged Shell & Tube Heat Exchanger** to easily process heavily treated dye house wastewater lines.",
                "Wetted Components Material: **Industrial Titanium Tubing** to shield structural elements from corrosive dyes, bleaching agents, and fixing salts.",
                "Direct Boiler Interface: Outfitted with auxiliary injection ports to smoothly mix direct utility steam into the loop during heavy operational phases."
            ],
            "Dye House Process Integration": [
                "Multi-Circuit Heat Zoning: Distributed piping headers run independent supply lines to provide varying process temperatures across different areas of the facility.",
                "Dye Vat Coupling: Direct thermal integration into individual dye vats using high-speed regulating control valves.",
                "Wastewater Energy Capture: Integrated heat exchangers harvest residual energy from hot wastewater dumps to preheat fresh incoming utility water."
            ],
            "Automation & Safety Controls": [
                "Production Scheduler Interface: Control software matches energy delivery to active batch schedules across the plant floors.",
                "Temperature Ramping Control: Automated control loops provide smooth temperature ramping curves (±2°C precision) for critical fabric dyeing runs.",
                "Pressure Constraints: Heavy pressure relief infrastructure caps line pressures at 4 to 6 bar."
            ]
        },
        
        "Pharmaceutical": {
            "Plant Fluid Piping": [
                f"Recommended Main Line Size: **DN {recommended_dn}** (Precisely engineered to maintain clean flow and eliminate stagnant fluid zones).",
                "Material Standard: **Ultra-pure Electropolished Stainless Steel (SS316L)** ensuring clean, non-reactive fluid delivery.",
                "Regulatory Traceability: Every pipe layout is heat-stamped and certified for full **FDA/GMP material compliance** trails."
            ],
            "Thermal Heat Exchanger System": [
                "Hardware Type: **Double-Tube or Certified Sanitary Plate & Frame Heat Exchanger** to prevent cross-contamination.",
                "Sealing Gaskets: **Cleanroom-grade non-degrading gaskets** matching pristine water-for-injection (WFI) standards.",
                "Pressure Bounds: Heavy-duty structural construction rated for high-pressure operations up to **10 bar**."
            ],
            "Precision Instrumentation": [
                "Sensor Benchmarks: Double-calibrated **RTD sensor networks (accurate to ±0.1°C)** deployed at critical regulatory control nodes.",
                "Data Archival Automation: 24/7 digital data acquisition system logging compliance metrics for batch audit reviews."
            ],
            "Plant Integration & Validation": [
                "Validation Standards: Complete validation documentation pack featuring full **Installation, Operation, and Performance Qualification (IQ/OQ/PQ)** files.",
                "System Isolation: Built with three-way diversion valves to instantly redirect fluid streams if production temperatures deviate by even 1°C."
            ],
            "Automation & Safety Controls": [
                "Regulatory Software Stack: Advanced PLC controllers built fully compliant with **FDA 21 CFR Part 11 electronic data validation metrics**.",
                "Audit Tracking Automation: Tamper-proof internal logging loops record every configuration change made across the system."
            ]
        },
        
        "Chemical": {
            "Plant Fluid Piping": [
                f"Recommended Main Line Size: **DN {recommended_dn}** (Sized to balance friction losses against high fluid volumes).",
                "Material Standard: **Heavy-gauge Carbon Steel or Hastelloy alloys** protected with specialized internal chemical coatings.",
                "Pressure Rating: Components use high-strength, durable fittings rated for heavy-duty industrial fluid applications."
            ],
            "Thermal Heat Exchanger System": [
                "Hardware Type: **Double-Wall Industrial Heat Exchanger** preventing hazardous fluids from crossing into process loops.",
                "Wetted Components Material: Custom **Inconel or Titanium alloy tube sets** to handle aggressive process chemistries."
            ],
            "Process Integration & Safety Zones": [
                "Multi-Tiered Thermal Zoning: Independent flow control circuits regulate temperature profiles across sequential reactor stages.",
                "Explosion-Proof Compliance: All localized wiring, motors, and instrumentation meet strict **ATEX/IECEx explosion-proof specifications**.",
                "Secondary Safety Containment: Process pipelines run inside protective secondary outer sleeves to manage line leaks or breaks safely."
            ],
            "Automation & Safety Controls": [
                "Advanced Controls Strategy: Process controllers deploy automated heating and cooling curves to manage reaction loops safely.",
                "Fault Tolerance Interlocks: Automated bypass valves trigger immediately if a pump fails, maintaining safe internal temperature balances."
            ]
        },
        
        "Food": {
            "Plant Fluid Piping": [
                f"Recommended Main Line Size: **DN {recommended_dn}** (Sized to maintain high sanitation velocities across daily operation).",
                "Material Standard: **Food-Safe Polished Stainless Steel (SS304 or SS316)** ensuring corrosion resistance and clear sanitary lines.",
                "Quick-Release Fittings: Outfitted with convenient **Tri-Clamp sanitary fittings** for fast disassembly, cleanouts, and internal pipe checks."
            ],
            "Thermal Heat Exchanger System": [
                "Hardware Type: **Sanitary Frame Heat Exchanger** with smooth internal plate finishes to prevent bacterial adherence.",
                "Sealing Gaskets: **FDA-certified, non-porous food-grade silicone or EPDM gaskets**."
            ],
            "Plant Integration & Food Safety": [
                "Direct Production Splicing: Solar lines connect smoothly to pre-heating stations for jacketted cooking kettles, cleanups, and boiler feed lines.",
                "Loop Isolation Strategy: Dual-loop barriers prevent solar storage fluids from ever interacting with food product streams.",
                "HACCP Data Interface: Built-in data loggers continuously record processing line temperatures to fulfill critical food safety audit guidelines."
            ],
            "Automation & Safety Controls": [
                "Daily Sanitization Cycles: Control systems schedule automatic thermal disinfection sequences during down-time hours.",
                "Boiler Integration Logic: Automatic control systems switch to utility gas boilers when solar storage reserves empty below the target value.",
                "High-Limit Thermal Trips: Safety systems isolate the solar field if delivery lines exceed the design threshold of **{tout}°C**."
            ]
        }
    }
    
    industry_recommendations = recommendations_dict.get(industry, recommendations_dict["Food"])
    
    # Process structured output array cleanly for view parsers
    result = []
    for section, items in industry_recommendations.items():
        result.append(f"\\n### {section}")
        for item in items:
            result.append(f"• {item}")
            
    return result


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
