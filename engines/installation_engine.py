def installation_steps():
    """
    Returns a comprehensive database of industrial-grade engineering installation steps,
    complete with technical specs, safety parameters, and compliance tracking metrics.
    """
    return [
        {
            "step": "Foundation Marking & Anchoring Groundwork",
            "icon": "📐",
            "description": "Establish structural grid reference lines on the roof or ground site utilizing high-precision digital transits or laser markers. Cross-verify the layout dimensions with the solar array matrix blueprint.",
            "specs": "Ensure anchoring embeds match civil design depth. Wind load rating tolerance must withstand local structural codes (e.g., up to 150 km/h wind shear forces).",
            "checklist": ["Civil layout dimensions verified", "Anchoring depth specifications matched", "Wind load rating tolerance met"]
        },
        {
            "step": "Support Structure Erection & Torque Fastening",
            "icon": "🏗️",
            "description": "Assemble hot-dip galvanized steel or structural-grade aluminum support modules. Set the fixed tilt angle precisely to the calculated tilt angle from the software design profile to eliminate multi-row shading risks.",
            "specs": "Apply structural anti-seize compound to all hardware. Fasteners must be tightened to explicit engineering torques using calibrated industrial torque wrenches.",
            "checklist": ["Tilt angle calibrated to design", "Hardware treated with anti-seize compound", "Fasteners tightened with calibrated torque tools"]
        },
        {
            "step": "Solar Collector Module Mounting & Alignment",
            "icon": "☀️",
            "description": "Lift and safely anchor individual collector panels (Flat Plate or Evacuated Tube Arrays) onto the mounted racks. Ensure uniform coplanar alignment across the array to eliminate structural stress and visual defects.",
            "specs": "Verify panel clearance lines match structural requirements. Check that EPDM vibration-isolation pads are correctly seated between panel casings and brackets.",
            "checklist": ["Panels checked for flat, coplanar alignment", "Module clearances verified", "EPDM isolation pads seated correctly"]
        },
        {
            "step": "Hydraulic Mainfold Piping & Flexible Link Fitting",
            "icon": "🚰",
            "description": "Run heavy-gauge copper or industrial stainless steel header pipelines. Connect rows using high-durability braided flexible loops or expansion joints to absorb heavy mechanical and thermal shifts.",
            "specs": "All standard pipeline joins must utilize high-temperature brazing alloys or premium press-fit systems. Avoid any rubber fittings inside the high-temperature loop.",
            "checklist": ["Main headers run in specified copper/stainless steel", "Expansion joins or braided loops installed", "High-temperature brazing/press-fit systems used"]
        },
        {
            "step": "Hydrostatic Pressure Testing & Integrity Audit",
            "icon": "🛡️",
            "description": "Seal the system loop, fill with clean utility water, and slowly pressurize the piping field to verify systemic mechanical integrity before adding any chemical heat transfer fluids.",
            "specs": "Hold the loop at 1.5 times the peak system design operating pressure (typically 6 to 9 bar) for a continuous 24-hour monitoring period to confirm zero pressure drop.",
            "checklist": ["System filled and air-pockets purged", "Pressurized to 1.5x peak system design load", "Zero pressure drop documented over 24-hour run"]
        },
        {
            "step": "High-Temperature Thermal Insulation & Weather Shielding",
            "icon": "🧥",
            "description": "Wrap all active solar manifold lines and external interconnect loops with high-density mineral wool or closed-cell elastomeric insulation to reduce systemic thermal losses.",
            "specs": "Protect all insulation runs with an outer layer of UV-resistant aluminum sheet cladding. Ensure seams are weatherproofed to prevent rain water intrusion.",
            "checklist": ["Manifolds insulated with high-density material", "UV-resistant aluminum jacketing installed", "Weatherproof cladding seals confirmed"]
        },
        {
            "step": "Electrical Control Integration & Sensor Instrumentation",
            "icon": "⚡",
            "description": "Wire the primary temperature thermistors (PT100/PT1000) at collector outlets and storage tank inlets. Route all sensor signaling lines back to the central automated logic controller panel.",
            "specs": "Run all outdoor wiring through weather-tight liquid-tight flexible conduits. Ensure proper grounding and lightning protection arrays are bonded to the structural frame.",
            "checklist": ["PT100/PT1000 sensors correctly mounted", "Signal wiring pulled through liquid-tight conduit", "Grounding systems bonded and tested"]
        },
        {
            "step": "System Flashing, Fluid Charging & Commissioning",
            "icon": "🚀",
            "description": "Flush construction debris out of the loop with a specialized cleaning chemical. Charge the system with the targeted process fluid (such as an anti-freeze glycol blend or conditioned water) and start the automated circulation pumps.",
            "specs": "Balance flow loops across all parallel arrays using calibrated balancing valves. Document baseline delta-T splits and pump electrical power draw profiles.",
            "checklist": ["Debris flush completed and filters cleaned", "Thermal transfer fluid charged to design pressure", "Balanced flow lines verified with differential gauges"]
        }
    ]
