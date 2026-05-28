def recommendations(industry="Dairy", tout=80, daily_water=5000, total_flow=250):
    """
    Generate detailed system integration recommendations
    based on industry requirements and system parameters.
    """
    
    recommendations_dict = {
        "Dairy": {
            "Piping": [
                "Use SS316 stainless steel piping (Food-grade)",
                f"Pipe diameter: {calculate_pipe_diameter(total_flow)} mm",
                "Minimum velocity: 0.3-0.5 m/s to prevent sedimentation",
                "Slope pipes at 1:40 minimum for drainage",
                "Insulation: 50mm mineral wool with aluminum cladding"
            ],
            "Heat Exchanger": [
                "Plate Heat Exchanger (PHE) - 50-100 plates",
                "AISI 304 stainless steel plates",
                "Gasket material: EPDM or FKM (sanitary grade)",
                "Hygienic design with <100µm crevice depth"
            ],
            "Instrumentation": [
                "RTD temperature sensors (Pt100) at inlet/outlet",
                "Pressure gauges with glycerin damping",
                "Digital flow meter for CIP monitoring",
                "pH sensors for water quality (optional)"
            ],
            "Integration": [
                "CIP (Clean-In-Place) system integration",
                "Automated valve sequencing for CIP cycles",
                "Tank: High-level polished finish (Ra < 0.8µm)",
                "Dedicated return line for thermal recovery",
                "Fresh milk cooling loop separation required"
            ],
            "Controls": [
                "PLC with recipe memory for different products",
                "Real-time temperature logging to 0.5°C accuracy",
                "Automatic switchover to backup boiler at dawn",
                "Safety interlocks for over-temperature shutdown"
            ],
            "Compliance": [
                "ISO 9001 certified system",
                "3-A sanitary standards for all wetted surfaces",
                "HACCP-compliant documentation"
            ]
        },
        
        "Textile": {
            "Piping": [
                f"Pipe diameter: {calculate_pipe_diameter(total_flow)} mm",
                "Cast iron or mild steel with 5mm corrosion allowance",
                "Insulation: 75mm asbestos-free for process lines",
                "Quick-disconnect couplings for rapid changeover"
            ],
            "Thermal Buffer": [
                "Thermal buffer tank (20-30% of daily requirement)",
                "Volume: 1000-2000 L depending on process",
                "Dual compartment design for layered heating",
                "Stratification height controller"
            ],
            "Heat Exchanger": [
                "Shell & Tube HX for dyeing processes",
                "Titanium tubes for chemical resistance",
                "Direct steam integration possible"
            ],
            "Integration": [
                "Rapid process changeover capability",
                "Multi-circuit distribution (different temp zones)",
                "Dye vat integration with individual control",
                "Waste heat recovery from exhaust steam"
            ],
            "Process Parameters": [
                f"Design temperature: {tout}°C",
                f"Daily water requirement: {daily_water} LPD",
                "Batch cycle adaptation: 2-4 hour cycles",
                "Auxiliary heating capacity required during off-season"
            ],
            "Controls": [
                "Process scheduler for multiple dye vats",
                "Temperature ramping control (±2°C)",
                "Pressure limiting to 4-6 bar"
            ]
        },
        
        "Pharmaceutical": {
            "Piping": [
                "Stainless steel AISI 316L electropolished",
                "FDA/GMP compliant material traceability",
                f"Pipe sizing: {calculate_pipe_diameter(total_flow)} mm",
                "WFI (Water For Injection) compatible"
            ],
            "Heat Exchanger": [
                "Plate & Frame HX with pharmaceutical certification",
                "Cleanroom compatible gaskets",
                "Pressure rating: ≥10 bar",
                "Validation of thermal profile maintained"
            ],
            "Instrumentation": [
                "Calibrated RTD sensors (±0.5°C accuracy)",
                "Data logging with 24/7 archival",
                "Pressure sensors with alarm limits",
                "Flow measurement with batch totalization"
            ],
            "Integration": [
                "Water preheating system before pharmaceutical lines",
                "Sterile steam trap integration",
                "Temperature hold capability (maintain ±1°C)",
                "Three-way isolation valves for servicing"
            ],
            "Quality Assurance": [
                "System validation (IQ/OQ/PQ) documentation",
                "Monthly calibration certificates required",
                "Microbial testing protocols",
                "Energy audit trail for batch traceability"
            ],
            "Controls": [
                "Advanced PLC with batch reporting",
                "Compliance to FDA 21 CFR Part 11",
                "Audit trail for all setpoint changes",
                "Automatic alert on deviation >2°C"
            ]
        },
        
        "Chemical": {
            "Piping": [
                "Stainless steel 316/316L or carbon steel with protective coating",
                "Chemical resistance assessment for process fluids",
                f"Pipe diameter: {calculate_pipe_diameter(total_flow)} mm",
                "Ductile iron fittings with 300 bar rating"
            ],
            "Heat Exchanger": [
                "Titanium or Inconel tubes for corrosive media",
                "Mechanical seals for hazardous processes",
                "Double-wall construction if required",
                "Emergency relief provisions"
            ],
            "Process Integration": [
                "Multi-zone heating for sequential reactions",
                "Temperature precision: ±3°C maintained",
                "Automatic shutdown on overpressure (>6 bar)",
                "Dedicated isolation for hazmat containment"
            ],
            "Safety Systems": [
                "Dual pressure relief valves",
                "Thermal cutoff switches at 100°C + margin",
                "Secondary containment for process lines",
                "ATEX compliance if flammable fluids involved"
            ],
            "Controls": [
                "Advanced process control with ramp/soak profiles",
                "Temperature uniformity monitoring",
                "Automatic switchover on pump failure",
                "Real-time process alarm management"
            ]
        },
        
        "Food": {
            "Piping": [
                "Stainless steel 304 or 316 for food contact",
                f"Pipe sizing: {calculate_pipe_diameter(total_flow)} mm",
                "Sanitary fittings with tri-clamp connections",
                "Insulation: 50-75mm food-grade with aluminum wrap"
            ],
            "Heat Exchanger": [
                "Plate HX with food-grade certification",
                "Smooth finish (Ra < 1.2µm) to prevent bacterial growth",
                "Gaskets: Silicone or EPDM (FDA approved)",
                "All external surfaces passivated"
            ],
            "Integration": [
                "Direct integration with cooking/processing lines",
                "Separate loop for product heating vs. utility",
                "CIP capability with chemical tolerance",
                "Product temperature logging (HACCP requirement)"
            ],
            "Instrumentation": [
                "RTD temperature sensors at critical points",
                "Flow measurement for portion control",
                "Pressure gauges for safety monitoring",
                "Product temperature recorder (chart/digital)"
            ],
            "Safety & Compliance": [
                "HACCP documentation for all processes",
                "NSF certification on components",
                "Regular hygiene audits recommended",
                "Legionella prevention measures"
            ],
            "Controls": [
                "Simple on/off control or modulating valve",
                "Automatic switchover to auxiliary heating",
                "Overheat protection at {tout}°C",
                "Daily sanitization cycle scheduling"
            ]
        }
    }
    
    industry_recommendations = recommendations_dict.get(industry, recommendations_dict["Food"])
    
    # Format output for display
    result = []
    for section, items in industry_recommendations.items():
        result.append(f"\\n### {section}")
        for item in items:
            result.append(f"• {item}")
    
    return result


def calculate_pipe_diameter(total_flow):
    """
    Calculate recommended pipe diameter based on total flow
    using standard velocity approach (1-2 m/s for hot water)
    """
    if total_flow < 100:
        return "16-20"
    elif total_flow < 250:
        return "25-32"
    elif total_flow < 500:
        return "40-50"
    elif total_flow < 1000:
        return "63-75"
    else:
        return "90-110"
