def generate_pid(industry="Dairy", collectors=5, tout=80, daily_water=5000, total_flow=250):
    """
    Generate a standard-compliant, human-readable P&ID diagram.
    Uses Graphviz with true ISA circular instrument bubbles and directional fluid routing.
    """
    
    # Process Flags
    has_backup = tout > 60
    has_cip = industry == "Dairy"
    has_buffer = industry == "Textile"
    has_process_control = industry in ["Pharmaceutical", "Chemical", "Food"]
    
    # Target tank variable mapping
    tank_id = "TB" if has_buffer else "TANK"
    tank_label = "Thermal Buffer Tank" if has_buffer else "Insulated Storage Tank"

    pid = f"""
    digraph IndustrialSolarPID {{
        rankdir=LR;
        splines=true;
        nodesep=0.4;
        ranksep=0.7;
        bgcolor=white;
        
        # Global Node Styles (ISA Standard)
        node [fontname="Arial", fontsize=10, shape=box, style=filled, fillcolor=white];
        edge [fontname="Arial", fontsize=9, labelfontcolor="darkblue"];
        
        # =====================================================
        # MAIN EQUIPMENT (Physical Assets)
        # =====================================================
        
        SC     [label="SOLAR FIELD\\nSolar Collectors\\n({collectors} Units)", fillcolor="#FFFDE7", penwidth=2];
        PUMP   [label="PRIMARY PUMP\\n(Solar Loop)", shape=circle, fixedsize=true, width=0.9, fillcolor="#ECEFF1"];
        HX     [label="PLATE HEAT EXCHANGER\\n(Solar-to-Storage)", fillcolor="#E3F2FD", penwidth=2];
        {tank_id}   [label="{tank_label}\\n({daily_water} LPD Capacity)", shape=cylinder, width=1.2, height=1.5, fillcolor="#E0F7FA", penwidth=2];
        
        # =====================================================
        # ISA STANDARD INSTRUMENTATION BUBBLES (Circular Transmitters)
        # =====================================================
        node [shape=circle, fixedsize=true, width=0.4, height=0.4, fillcolor="#FFFFFF", style=filled, fontsize=8];
        
        # Loop Transmitters
        TT_field [label="TT\\n101"];
        PT_field [label="PT\\n101"];
        TT_hx    [label="TT\\n102"];
        
        # Storage Transmitters
        TT_tank  [label="TT\\n103"];
        LT_tank  [label="LT\\n101"]; # Level transmitter for a real tank
        
        # =====================================================
        # VALVES AND INLINE COMPONENTS
        # =====================================================
        node [shape=box, fixedsize=false, width=0.6, height=0.3, fontsize=8, fillcolor="#F5F5F5"];
        
        CV_in  [label="Check\\nValve"];
        PSV    [label="Safety\\nValve (PSV)"];
        EV     [label="Expansion\\nTank"];
        
        # =====================================================
        # LIQUID FLOW PIPING PATHWAYS (Left to Right)
        # =====================================================
        
        # 1. Primary Closed Loop (Solar Collector Circuit)
        SC -> PT_field [color="#D32F2F", penwidth=2, label=" Hot Fluid"];
        PT_field -> TT_field [color="#D32F2F", penwidth=2];
        TT_field -> HX [color="#D32F2F", penwidth=2];
        
        # Cold return line back to array
        HX -> PUMP [color="#1976D2", penwidth=2, label=" Cooled Return"];
        PUMP -> CV_in [color="#1976D2", penwidth=2];
        CV_in -> PSV [color="#1976D2", penwidth=2];
        PSV -> SC [color="#1976D2", penwidth=2];
        
        # Hook up the Expansion Tank to cold line safety
        PSV -> EV [style=dashed, color=gray, arrowhead=none];
        
        # 2. Charging the Storage Tank System
        HX -> TT_hx [color="#E65100", penwidth=2, label=" Charged Heat"];
        TT_hx -> {tank_id} [color="#E65100", penwidth=2];
        
        # Attach Instrument indicators directly to the Tank body
        {tank_id} -> TT_tank [style=dotted, arrowhead=none];
        {tank_id} -> LT_tank [style=dotted, arrowhead=none];
        
        # =====================================================
        # BACKUP SYSTEMS SECTION
        # =====================================================
        """
        
    if has_backup:
        pid += f"""
        node [shape=box, fontname="Arial", fontsize=10, style=filled];
        BOILER [label="BACKUP BOILER\\n(Activates below {tout}°C)", fillcolor="#FFEBEE", penwidth=1.5];
        BV     [label="Modulating\\nControl Valve", shape=box, fontsize=8, fillcolor="#F5F5F5"];
        
        {tank_id} -> BOILER [color="#D32F2F", penwidth=1.5, style=dashed, label=" Low Temp Loop"];
        BOILER -> BV [color="#D32F2F", penwidth=1.5];
        BV -> {tank_id} [color="#D32F2F", penwidth=1.5];
        """
        
    pid += f"""
        # =====================================================
        # PROCESS & END USER DELIVERY LOOP
        # =====================================================
        """
        
    if has_cip:
        pid += f"""
        node [shape=box, fontname="Arial", fontsize=10, style=filled];
        PROCESS [label="CLEAN-IN-PLACE (CIP) SYSTEM\\n{industry} Industry Automation", fillcolor="#E8F5E9", penwidth=2];
        CIPpump [label="CIP DELIVERY\\nPUMP", shape=circle, fixedsize=true, width=0.8, fillcolor="#ECEFF1"];
        
        {tank_id} -> CIPpump [color="#D32F2F", penwidth=2, label=" Process Supply"];
        CIPpump -> PROCESS [color="#D32F2F", penwidth=2];
        """
    elif has_process_control:
        pid += f"""
        node [shape=box, fontname="Arial", fontsize=10, style=filled];
        PROCESS [label="PROCESS HEAT EXCHANGER\\nProduction Floor Integration", fillcolor="#E8F5E9", penwidth=2];
        FC      [label="Automated Flow\\nController (FC)", shape=box, fontsize=8, fillcolor="#F5F5F5"];
        
        {tank_id} -> FC [color="#D32F2F", penwidth=2, label=" Regulated Supply"];
        FC -> PROCESS [color="#D32F2F", penwidth=2];
        """
    else:
        pid += f"""
        node [shape=box, fontname="Arial", fontsize=10, style=filled];
        PROCESS [label="HOT WATER DISTRIBUTION\\nGeneral Plant Utilities", fillcolor="#E8F5E9", penwidth=2];
        
        {tank_id} -> PROCESS [color="#D32F2F", penwidth=2, label=" Hot Water Draw"];
        """
        
    pid += f"""
        # =====================================================
        # LEGEND SUBGRAPH (Keeps diagram plain English)
        # =====================================================
        subgraph cluster_legend {{
            label="Diagram Key & ISA Legend";
            fontname="Arial Bold";
            fontsize=11;
            color=gray;
            style=dashed;
            
            leg_tt [label="TT = Temperature Transmitter Bubble", shape=circle, width=0.4, fontsize=7];
            leg_pt [label="PT = Pressure Transmitter Bubble", shape=circle, width=0.4, fontsize=7];
            leg_lt [label="LT = Tank Level Indicator", shape=circle, width=0.4, fontsize=7];
            leg_red [label="Hot Water Fluid Pipe Path", shape=line, color="#D32F2F", penwidth=2];
            leg_blue [label="Cold Return Water Fluid Path", shape=line, color="#1976D2", penwidth=2];
        }}
    }}
    """
    return pid
