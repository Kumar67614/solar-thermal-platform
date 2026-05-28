def generate_pid(industry="Dairy", collectors=5, tout=80, daily_water=5000, total_flow=250):
    """
    Generate a high-visibility, standard-compliant P&ID diagram.
    Fixed layout balance issues: minimizes instrument nodes, balances aspect ratios, 
    and keeps the operational diagram large, centered, and crystal clear.
    """
    
    # Process Logic Flags
    has_backup = tout > 60
    has_cip = industry == "Dairy"
    has_buffer = industry == "Textile"
    has_process_control = industry in ["Pharmaceutical", "Chemical", "Food"]
    
    tank_id = "TB" if has_buffer else "TANK"
    tank_label = "Thermal Buffer Tank" if has_buffer else "Insulated Storage Tank"

    pid = f"""
    digraph IndustrialSolarPID {{
        rankdir=LR;
        splines=ortho;  # Straight, clean perpendicular pipes instead of messy curves
        nodesep=0.6;
        ranksep=0.8;
        bgcolor=white;
        concentrate=true;
        
        # Global Design Tokens
        node [fontname="Arial Bold", fontsize=10, shape=box, style="filled,rounded", fillcolor="#FFFFFF", color="#37474F", penwidth=1.5];
        edge [fontname="Arial", fontsize=9, labelfontcolor="#263238", penwidth=2];
        
        # =====================================================
        # CORE EQUIPMENT (PROPORTIONAL SIZING)
        # =====================================================
        SC     [label="SOLAR FIELD\\n({collectors} Collectors)", shape=box, style=filled, fillcolor="#FFFDE7", width=1.8, height=1.0];
        PUMP   [label="PRIMARY\\nPUMP", shape=circle, fixedsize=true, width=0.8, height=0.8, fillcolor="#ECEFF1"];
        HX     [label="PLATE HX\\n(Solar-to-Storage)", shape=box, style=filled, fillcolor="#E3F2FD", width=1.6, height=1.0];
        {tank_id}   [label="{tank_label}\\n({daily_water} LPD)", shape=cylinder, fixedsize=true, width=1.6, height=1.8, fillcolor="#E0F7FA"];
        
        # =====================================================
        # SLEEK INSTRUMENTATION BUBBLES (EXACT SIZE CONTROL)
        # =====================================================
        node [shape=circle, fixedsize=true, width=0.45, height=0.45, fillcolor="#FFFFFF", style=filled, fontsize=8, color="#455A64"];
        TT_field [label="TT\\n101"];
        PT_field [label="PT\\n101"];
        TT_hx    [label="TT\\n102"];
        TT_tank  [label="TT\\n103"];
        LT_tank  [label="LT\\n101"];
        
        # =====================================================
        # INLINE INVENTORY / VALVES (COMPACT SHAPES)
        # =====================================================
        node [shape=box, fixedsize=true, width=0.7, height=0.35, fontsize=8, fillcolor="#FAFAFA", style="filled"];
        CV_in  [label="Check Vlv"];
        PSV    [label="Safety Vlv"];
        EV     [label="Exp Tank"];
        
        # =====================================================
        # FLUID PIPING ENGINE (Left to Right High-Speed Paths)
        # =====================================================
        
        # Primary Loop Heating Cycle
        SC -> PT_field [color="#D32F2F", label=" Hot Fluid "];
        PT_field -> TT_field [color="#D32F2F"];
        TT_field -> HX [color="#D32F2F"];
        
        # Primary Loop Cold Return Path
        HX -> PUMP [color="#1976D2", label=" Cooled Return "];
        PUMP -> CV_in [color="#1976D2"];
        CV_in -> PSV [color="#1976D2"];
        PSV -> SC [color="#1976D2"];
        
        # Closed-loop Safety Connections
        PSV -> EV [style=dashed, color="#78909C", arrowhead=none];
        
        # Secondary Tank Charging Circuit
        HX -> TT_hx [color="#E65100", label=" Hot Charging "];
        TT_hx -> {tank_id} [color="#E65100"];
        
        # Transmitters bound clearly to Storage
        {tank_id} -> TT_tank [style=dotted, color="#546E7A", arrowhead=none, weight=2];
        {tank_id} -> LT_tank [style=dotted, color="#546E7A", arrowhead=none, weight=2];
        
        # =====================================================
        # BACKUP SUBSYSTEMS
        # =====================================================
        """
        
    if has_backup:
        pid += f"""
        node [shape=box, fontname="Arial Bold", fontsize=10, style=filled, fixedsize=false];
        BOILER [label="BACKUP BOILER\\n(Spikes to {tout}°C)", fillcolor="#FFEBEE", width=1.5, height=0.8];
        BV     [label="Control\\nValve", shape=box, fixedsize=true, width=0.6, height=0.35, fontsize=8, fillcolor="#FAFAFA"];
        
        {tank_id} -> BOILER [color="#D32F2F", style=dashed, label=" Boost Circuit "];
        BOILER -> BV [color="#D32F2F"];
        BV -> {tank_id} [color="#D32F2F"];
        """
        
    pid += f"""
        # =====================================================
        # END USER RECIPIENT APPLICATION LOOP
        # =====================================================
        """
        
    if has_cip:
        pid += f"""
        node [shape=box, fontname="Arial Bold", fontsize=10, style=filled, fixedsize=false];
        PROCESS [label="CLEAN-IN-PLACE (CIP) SYSTEM\\n{industry} Process Loop", fillcolor="#E8F5E9", width=2.2, height=0.9];
        CIPpump [label="CIP\\nPUMP", shape=circle, fixedsize=true, width=0.7, height=0.7, fillcolor="#ECEFF1"];
        
        {tank_id} -> CIPpump [color="#D32F2F", label=" Process Out "];
        CIPpump -> PROCESS [color="#D32F2F"];
        """
    elif has_process_control:
        pid += f"""
        node [shape=box, fontname="Arial Bold", fontsize=10, style=filled, fixedsize=false];
        PROCESS [label="PRODUCTION HEAT EXCHANGER\\nPlant Delivery Floor", fillcolor="#E8F5E9", width=2.2, height=0.9];
        FC      [label="Flow Ctrl", shape=box, fixedsize=true, width=0.6, height=0.35, fontsize=8, fillcolor="#FAFAFA"];
        
        {tank_id} -> FC [color="#D32F2F", label=" Regulated "];
        FC -> PROCESS [color="#D32F2F"];
        """
    else:
        pid += f"""
        node [shape=box, fontname="Arial Bold", fontsize=10, style=filled, fixedsize=false];
        PROCESS [label="PLANT UTILITY SUPPLY\\nHot Water Outlets", fillcolor="#E8F5E9", width=2.2, height=0.9];
        
        {tank_id} -> PROCESS [color="#D32F2F", label=" General Demands "];
        """
        
    pid += f"""
        # =====================================================
        # COMPACT ROW-SINK LEGEND (Prevents Graph Stretching)
        # =====================================================
        subgraph cluster_legend {{
            label="DIAGRAM UTILITY KEY / LEGEND";
            fontname="Arial Bold";
            fontsize=11;
            color="#90A4AE";
            style=dashed;
            rank=sink; # Pushes the legend strictly out of the way to the bottom row
            
            node [shape=box, fixedsize=false, fontsize=9, style=filled, fillcolor=white, color="#CFD8DC"];
            leg_tt   [label="TT = Temp Sensor Bubble", shape=circle, width=0.35, height=0.35];
            leg_pt   [label="PT = Pressure Sensor Bubble", shape=circle, width=0.35, height=0.35];
            leg_red  [label="Hot Supply Piping Loop", fontcolor="#D32F2F", color="#D32F2F", penwidth=2.5];
            leg_blue [label="Cold Return Piping Loop", fontcolor="#1976D2", color="#1976D2", penwidth=2.5];
        }}
    }}
    """
    return pid
