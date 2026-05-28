def generate_pid(industry="Dairy", collectors=5, tout=80, daily_water=5000, total_flow=250):
    """
    Generates a perfectly balanced, wide-format P&ID with clear separation 
    between active process loops and the system index key.
    
    Fixes layout issues by creating an isolated bottom-ranked cluster for the 
    HTML legend box, ensuring zero overlaps or clipping.
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
        splines=ortho;       # Clean 90-degree industrial piping lines
        nodesep=0.6;         # Balanced vertical padding between parallel pipes
        ranksep=0.8;         # Generous horizontal spacing for flow readability
        bgcolor=white;
        pad="0.5,0.5";
        
        # =====================================================
        # DESIGN SYSTEM STANDARD (ISA-COMPLIANT SHAPES)
        # =====================================================
        # Heavy Equipment Node Defaults
        node [fontname="Arial Bold", fontsize=10, shape=box, style="filled,rounded", fillcolor="#FFFFFF", color="#263238", penwidth=1.5];
        edge [fontname="Arial Bold", fontsize=9, labelfontcolor="#263238", penwidth=2.0];
        
        # Primary Equipment Assets
        SC     [label="SOLAR FIELD\\n({collectors} Collectors)", shape=box, style=filled, fillcolor="#FFFDE7", fixedsize=true, width=1.8, height=0.85];
        PUMP   [label="PRIMARY\\nPUMP", shape=circle, fixedsize=true, width=0.8, height=0.8, fillcolor="#ECEFF1"];
        HX     [label="PLATE HX\\n(Solar-to-Storage)", shape=box, style=filled, fillcolor="#E3F2FD", fixedsize=true, width=1.8, height=0.85];
        {tank_id}   [label="{tank_label}\\n({daily_water} LPD)", shape=cylinder, fixedsize=true, width=1.7, height=1.7, fillcolor="#E0F7FA"];
        
        # Precise Round Transmitter Instruments
        node [shape=circle, fixedsize=true, width=0.45, height=0.45, fillcolor="#FFFFFF", style=filled, fontsize=8, color="#37474F", penwidth=1.2];
        TT_field [label="TT\\n101"];
        PT_field [label="PT\\n101"];
        TT_hx    [label="TT\\n102"];
        TT_tank  [label="TT\\n103"];
        LT_tank  [label="LT\\n101"];
        
        # Compact Process Valves & Inline Hardware
        node [shape=box, fixedsize=true, width=0.75, height=0.35, fontsize=8, fillcolor="#FAFAFA", style="filled", color="#455A64"];
        CV_in  [label="Check Vlv"];
        PSV    [label="Safety Vlv"];
        EV     [label="Exp Tank"];
        
        # =====================================================
        # CLOSED LOOP FLUID PIPING (Primary Solar Circuit)
        # =====================================================
        
        # Hot Supply Outflow (Red Pipe Line)
        SC -> PT_field [color="#D32F2F", label=" Hot Fluid"];
        PT_field -> TT_field [color="#D32F2F"];
        TT_field -> HX [color="#D32F2F"];
        
        # Cooled Fluid Return Path (Blue Pipe Line)
        HX -> PUMP [color="#1976D2", label=" Cooled Return"];
        PUMP -> CV_in [color="#1976D2"];
        CV_in -> PSV [color="#1976D2"];
        PSV -> SC [color="#1976D2"];
        
        # Thermal Safety Relief Expansion Connection
        PSV -> EV [style=dashed, color="#78909C", arrowhead=none];
        
        # =====================================================
        # ENERGY STORAGE STORAGE & CHARGING LOOP
        # =====================================================
        
        # Thermal Transfer Path to Tank (Orange Pipe Line)
        HX -> TT_hx [color="#E65100", label=" Charging Heat"];
        TT_hx -> {tank_id} [color="#E65100"];
        
        # Secure Instruments onto Tank Wall Without Layout Disruption
        TT_tank -> {tank_id} [style=dotted, color="#78909C", arrowhead=none, constraint=false];
        LT_tank -> {tank_id} [style=dotted, color="#78909C", arrowhead=none, constraint=false];
        
        # =====================================================
        # OPTIONAL INTEGRATED BACKUP HEATING SUBSYSTEM
        # =====================================================
        """
        
    if has_backup:
        pid += f"""
        node [shape=box, fontname="Arial Bold", fontsize=10, style=filled, fixedsize=true, width=1.6, height=0.75, color="#263238"];
        BOILER [label="BACKUP BOILER\\n(Spikes to {tout}°C)", fillcolor="#FFEBEE"];
        BV     [label="Control\\nValve", shape=box, fixedsize=true, width=0.65, height=0.35, fontsize=8, fillcolor="#FAFAFA"];
        
        {tank_id} -> BOILER [color="#D32F2F", style=dashed, label=" Temp Drop "];
        BOILER -> BV [color="#D32F2F"];
        BV -> {tank_id} [color="#D32F2F"];
        """
        
    pid += f"""
        # =====================================================
        # END APPLICATION DEMAND RUNS
        # =====================================================
        """
        
    if has_cip:
        pid += f"""
        node [shape=box, fontname="Arial Bold", fontsize=10, style=filled, fixedsize=true, width=2.4, height=0.85, color="#263238"];
        PROCESS [label="CLEAN-IN-PLACE (CIP) SYSTEM\\n{industry} Plant Process Loop", fillcolor="#E8F5E9"];
        CIPpump [label="CIP\\nPUMP", shape=circle, fixedsize=true, width=0.7, height=0.7, fillcolor="#ECEFF1"];
        
        {tank_id} -> CIPpump [color="#D32F2F", label=" Process Supply "];
        CIPpump -> PROCESS [color="#D32F2F"];
        """
    elif has_process_control:
        pid += f"""
        node [shape=box, fontname="Arial Bold", fontsize=10, style=filled, fixedsize=true, width=2.4, height=0.85, color="#263238"];
        PROCESS [label="PRODUCTION HEAT EXCHANGER\\nPlant Delivery Floor Integration", fillcolor="#E8F5E9"];
        FC      [label="Flow Ctrl", shape=box, fixedsize=true, width=0.65, height=0.35, fontsize=8, fillcolor="#FAFAFA"];
        
        {tank_id} -> FC [color="#D32F2F", label=" Regulated "];
        FC -> PROCESS [color="#D32F2F"];
        """
    else:
        pid += f"""
        node [shape=box, fontname="Arial Bold", fontsize=10, style=filled, fixedsize=true, width=2.4, height=0.85, color="#263238"];
        PROCESS [label="PLANT UTILITY SUPPLY\\nHot Water Delivery Outlets", fillcolor="#E8F5E9"];
        
        {tank_id} -> PROCESS [color="#D32F2F", label=" Hot Water Draw "];
        """
        
    pid += f"""
        # =====================================================
        # LOCKED VISUAL FOOTER LEGEND (STRUCTURAL BOUNDARY)
        # =====================================================
        subgraph cluster_legend_box {{
            style=none;
            peripheries=0;
            
            LEGEND [
                shape=plaintext,
                style=none,
                label=<
                    <TABLE BORDER="2" CELLBORDER="0" CELLSPACING="10" CELLPADDING="6" BGCOLOR="#FFFFFF" COLOR="#78909C" STYLE="ROUNDED">
                        <TR>
                            <TD COLSPAN="6" ALIGN="CENTER"><B><FONT POINT-SIZE="12" COLOR="#263238">DIAGRAM KEY &amp; SYSTEM LEGEND</FONT></B></TD>
                        </TR>
                        <TR>
                            <TD BGCOLOR="#FFFDE7" BORDER="1" COLOR="#37474F"><B> TT </B> Temperature Sensor</TD>
                            <TD BGCOLOR="#E3F2FD" BORDER="1" COLOR="#37474F"><B> PT </B> Pressure Sensor</TD>
                            <TD BGCOLOR="#E0F7FA" BORDER="1" COLOR="#37474F"><B> LT </B> Tank Level Sensor</TD>
                            <TD><FONT COLOR="#D32F2F" POINT-SIZE="14"><B>━━━━▶</B></FONT> Hot Supply Loop</TD>
                            <TD><FONT COLOR="#1976D2" POINT-SIZE="14"><B>━━━━▶</B></FONT> Cold Return Loop</TD>
                            <TD><FONT COLOR="#E65100" POINT-SIZE="14"><B>━━━━▶</B></FONT> Heat Charging Loop</TD>
                        </TR>
                    </TABLE>
                >
            ];
        }}
        
        # Enforces absolute alignment: anchors the legend cleanly beneath the main diagram
        {{ rank=sink; LEGEND; }}
        SC -> LEGEND [style=invis, minlen=2];
    }}
    """
    return pid
