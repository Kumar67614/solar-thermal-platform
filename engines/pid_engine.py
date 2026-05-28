def generate_pid(industry="Dairy", collectors=5, tout=80, daily_water=5000, total_flow=250):
    """
    Generate a detailed P&ID (Piping and Instrumentation Diagram) 
    based on system parameters and industry requirements.
    
    Uses graphviz with ISA standard symbols.
    """
    
    # Determine system configuration based on parameters
    has_backup = tout > 60  # Add backup boiler for high temps
    has_cip = industry == "Dairy"
    has_buffer = industry == "Textile"
    has_process_control = industry in ["Pharmaceutical", "Chemical", "Food"]
    
    pid = f"""
digraph SystemPID {{
    rankdir=LR;
    splines=curved;
    bgcolor=white;
    
    /* Node attributes */
    node [fontname="Arial", fontsize=10];
    
    /* ========== SOLAR FIELD SECTION ========== */
    
    SC [label="Solar Collectors\\n({collectors} units)", shape=box, style=filled, fillcolor=lightyellow];
    
    PT1 [label="PT\\n(Pressure)", shape=diamond, height=0.5, width=0.5];
    TT1 [label="TT\\n(Temp)", shape=diamond, height=0.5, width=0.5];
    
    SC -> PT1;
    SC -> TT1;
    
    /* ========== PUMP SECTION ========== */
    
    CVin [label="CHV\\n(Check Valve)", shape=box, height=0.4, width=0.8];
    PSV [label="PSV\\n(Relief Valve)", shape=box, height=0.4, width=0.8];
    
    PT1 -> CVin;
    CVin -> PSV;
    
    PUMP [label="Primary Pump\\n(Main Circulation)", shape=circle, height=0.8];
    PSV -> PUMP;
    
    /* ========== HEAT EXCHANGER SECTION ========== */
    
    HX [label="Plate HX\\n(Solar-to-Storage)", shape=box, style=filled, fillcolor=lightblue];
    
    PUMP -> HX;
    
    TT2 [label="TT\\n(Outlet)", shape=diamond, height=0.5, width=0.5];
    HX -> TT2;
    
    CVout [label="CHV\\n(Check Valve)", shape=box, height=0.4, width=0.8];
    TT2 -> CVout;
    
    /* ========== THERMAL STORAGE ========== """
    
    if has_buffer:
        pid += f"""
    TB [label="Thermal Buffer\\n(Hot Water Tank)", shape=cylinder, height=1.2, width=0.8, style=filled, fillcolor=lightcyan];
    CVout -> TB;
    """
    else:
        pid += f"""
    TANK [label="Storage Tank\\n(Insulated)", shape=cylinder, height=1.2, width=0.8, style=filled, fillcolor=lightcyan];
    CVout -> TANK;
    """
    
    if has_backup:
        pid += f"""
    /* ========== BACKUP BOILER SECTION ========== */
    
    BOILER [label="Backup Boiler\\n(for T < {tout}°C)", shape=box, style=filled, fillcolor=lightcoral];
    BV [label="BV\\n(Block Valve)", shape=box, height=0.4, width=0.8];
    BOILER -> BV;
    
    HX2 [label="Booster HX", shape=box, style=filled, fillcolor=lightcoral];
    BV -> HX2;
    
    {"TB" if has_buffer else "TANK"} -> HX2;
    """
    
    pid += f"""
    /* ========== PROCESS/OUTPUT SECTION ========== """
    
    if has_cip:
        pid += f"""
    /* Dairy CIP Integration */
    PROCESS [label="CIP System\\n(Process Integration)", shape=box, style=filled, fillcolor=lightgreen];
    CIPpump [label="CIP Pump", shape=circle, height=0.6];
    {"TB" if has_buffer else "TANK"} -> CIPpump;
    CIPpump -> PROCESS;
    """
    elif has_process_control:
        pid += f"""
    /* Process Control Integration */
    PROCESS [label="Process Heat Exchanger\\n(Pharmaceutical/Chemical)", shape=box, style=filled, fillcolor=lightgreen];
    FC [label="FC\\n(Flow Control)", shape=box, height=0.4, width=0.8];
    {"TB" if has_buffer else "TANK"} -> FC;
    FC -> PROCESS;
    """
    else:
        pid += f"""
    /* Standard Process */
    PROCESS [label="Process Application\\n(Hot Water Supply)", shape=box, style=filled, fillcolor=lightgreen];
    {"TB" if has_buffer else "TANK"} -> PROCESS;
    """
    
    pid += f"""
    /* ========== EXPANSION & SAFETY ========== */
    
    EV [label="EV\\n(Expansion Tank)", shape=box, height=0.4, width=0.8];
    TEMP [label="TT\\n(System Temp)", shape=diamond, height=0.5, width=0.5];
    
    {"TB" if has_buffer else "TANK"} -> EV;
    {"TB" if has_buffer else "TANK"} -> TEMP;
    
    /* ========== LEGEND ========== */
    
    subgraph Legend {{
        label="ISA Symbols";
        PT [label="PT = Pressure Transmitter"];
        TT [label="TT = Temperature Transmitter"];
        FC [label="FC = Flow Controller"];
        CHV [label="CHV = Check Valve"];
        PSV [label="PSV = Pressure Safety Valve"];
        BV [label="BV = Block Valve"];
    }}
    
    /* Layout adjustments */
    {{ rank=same SC PT1 TT1 }}
    {{ rank=same PUMP PSV CVin }}
    {{ rank=same HX TT2 CVout }}
    {{ rank=same {"TB" if has_buffer else "TANK"} EV TEMP }}
    
}}
"""
    
    return pid
