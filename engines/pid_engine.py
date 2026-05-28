def generate_pid(industry="Dairy", collectors=5, tout=80, daily_water=5000, total_flow=250):
    """
    Generates a perfectly balanced, wide-format P&ID diagram.
    Replaces the bulky sidebar legend cluster with a compact horizontal HTML footer.
    This forces the main engineering system components to scale up massively across the screen.
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
        splines=ortho;       # Straight, professional perpendicular pipe lines
        nodesep=0.5;         # Vertical space between paths
        ranksep=0.7;         # Horizontal space between equipment
        bgcolor=white;
        pad="0.5,0.5";
        
        # =====================================================
        # DESIGN TOKENS (Strictly Controlled Dimensions)
        # =====================================================
        # Standard equipment style
        node [fontname="Arial Bold", fontsize=10, shape=box, style="filled,rounded", fillcolor="#FFFFFF", color="#263238", penwidth=1.5];
        edge [fontname="Arial", fontsize=9, labelfontcolor="#263238", penwidth=1.75];
        
        # Core Process Assets
        SC     [label="SOLAR FIELD\\n({collectors} Collectors)", shape=box, style=filled, fillcolor="#FFFDE7", fixedsize=true, width=1.8, height=0.8];
        PUMP   [label="PRIMARY\\nPUMP", shape=circle, fixedsize=true, width=0.75, height=0.75, fillcolor="#ECEFF1"];
        HX     [label="PLATE HX\\n(Solar-to-Storage)", shape=box, style=filled, fillcolor="#E3F2FD", fixedsize=true, width=1.6, height=0.8];
        {tank_id}   [label="{tank_label}\\n({daily_water} LPD)", shape=cylinder, fixedsize=true, width=1.6, height=1.6, fillcolor="#E0F7FA"];
        
        # Sleek Instrument Bubbles (Locked small)
        node [shape=circle, fixedsize=true, width=0.4, height=0.4, fillcolor="#FFFFFF", style=filled, fontsize=8, color="#37474F", penwidth=1.2];
        TT_field [label="TT\\n101"];
        PT_field [label="PT\\n101"];
        TT_hx    [label="TT\\n102"];
        TT_tank  [label="TT\\n103"];
        LT_tank  [label="LT\\n101"];
        
        # Inline Fittings & Valves (Locked small)
        node [shape=box, fixedsize=true, width=0.7, height=0.3, fontsize=8, fillcolor="#FAFAFA", style="filled", color="#455A64"];
        CV_in  [label="Check Vlv"];
        PSV    [label="Safety Vlv"];
        EV     [label="Exp Tank"];
        
        # =====================================================
        # PROCESS FLOW PIPING JUNCTIONS
        # =====================================================
        
        # Primary Loop (Hot Side)
        SC -> PT_field [color="#D32F2F", label=" Hot Fluid "];
        PT_field -> TT_field [color="#D32F2F"];
        TT_field -> HX [color="#D32F2F"];
        
        # Primary Loop (Cold Return)
        HX -> PUMP [color="#1976D2", label=" Cooled Fluid "];
        PUMP -> CV_in [color="#1976D2"];
        CV_in -> PSV [color="#1976D2"];
        PSV -> SC [color="#1976D2"];
        
        # Safety Expansion
        PSV -> EV [style=dashed, color="#78909C", arrowhead=none];
        
        # Charging Circuit
        HX -> TT_hx [color="#E65100", label=" Charging "];
        TT_hx -> {tank_id} [color="#E65100"];
        
        # Instrumentation ties to Tank
        {tank_id} -> TT_tank [style=dotted, color="#78909C", arrowhead=none];
        {tank_id} -> LT_tank [style=dotted, color="#78909C", arrowhead=none];
        
        # =====================================================
        # OPTIONAL BACKUP SUBSYSTEM
        # =====================================================
        """
        
    if has_backup:
        pid += f"""
        node [shape=box, fontname="Arial Bold", fontsize=10, style=filled, fixedsize=true, width=1.5, height=0.7, color="#263238"];
        BOILER [label="BACKUP BOILER\\n(Spikes to {tout}°C)", fillcolor="#FFEBEE"];
        BV     [label="Control\\nValve", shape=box, fixedsize=true, width=0.6, height=0.3, fontsize=8, fillcolor="#FAFAFA"];
        
        {tank_id} -> BOILER [color="#D32F2F", style=dashed, label=" Temp Drop "];
        BOILER -> BV [color="#D32F2F"];
        BV -> {tank_id} [color="#D32F2F"];
        """
        
    pid += f"""
        # =====================================================
        # USER DELIVERY APPLICATION LOOP
        # =====================================================
        """
        
    if has_cip:
        pid += f"""
        node [shape=box, fontname="Arial Bold", fontsize=10, style=filled, fixedsize=true, width=2.2, height=0.8, color="#263238"];
        PROCESS [label="CLEAN-IN-PLACE (CIP) SYSTEM\\n{industry} Process Automation", fillcolor="#E8F5E9"];
        CIPpump [label="CIP\\nPUMP", shape=circle, fixedsize=true, width=0.65, height=0.65, fillcolor="#ECEFF1"];
        
        {tank_id} -> CIPpump [color="#D32F2F", label=" Process Out "];
        CIPpump -> PROCESS [color="#D32F2F"];
        """
    elif has_process_control:
        pid += f"""
        node [shape=box, fontname="Arial Bold", fontsize=10, style=filled, fixedsize=true, width=2.2, height=0.8, color="#263238"];
        PROCESS [label="PRODUCTION HEAT EXCHANGER\\nPlant Delivery Floor", fillcolor="#E8F5E9"];
        FC      [label="Flow Ctrl", shape=box, fixedsize=true, width=0.6, height=0.3, fontsize=8, fillcolor="#FAFAFA"];
        
        {tank_id} -> FC [color="#D32F2F", label=" Regulated "];
        FC -> PROCESS [color="#D32F2F"];
        """
    else:
        pid += f"""
        node [shape=box, fontname="Arial Bold", fontsize=10, style=filled, fixedsize=true, width=2.2, height=0.8, color="#263238"];
        PROCESS [label="PLANT UTILITY SUPPLY\\nHot Water Outlets", fillcolor="#E8F5E9"];
        
        {tank_id} -> PROCESS [color="#D32F2F", label=" General Load "];
        """
        
    pid += f"""
        # =====================================================
        # COMPACT HORIZONTAL LEGEND BLOCK (FORCES FULL-WIDTH RESIZE)
        # =====================================================
        LEGEND [
            shape=plaintext,
            style=none,
            label=<
                <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="8" CELLPADDING="4" BGCOLOR="#FFFFFF" COLOR="#90A4AE" STYLE="ROUNDED">
                    <TR>
                        <TD COLSPAN="6" ALIGN="CENTER"><B>DIAGRAM KEY &amp; ISA SYSTEM LEGEND</B></TD>
                    </TR>
                    <TR>
                        <TD BGCOLOR="#FFFDE7" BORDER="1" COLOR="#263238"><B> TT </B> Temperature Transmitter</TD>
                        <TD BGCOLOR="#E3F2FD" BORDER="1" COLOR="#263238"><B> PT </B> Pressure Transmitter</TD>
                        <TD BGCOLOR="#E0F7FA" BORDER="1" COLOR="#263238"><B> LT </B> Level Transmitter</TD>
                        <TD><FONT COLOR="#D32F2F"><B>━━━━▶</B></FONT> Hot Supply Pipe</TD>
                        <TD><FONT COLOR="#1976D2"><B>━━━━▶</B></FONT> Cold Return Pipe</TD>
                        <TD><FONT COLOR="#E65100"><B>━━━━▶</B></FONT> Heat Charging Pipe</TD>
                    </TR>
                </TABLE>
            >
        ];
        
        # Pins the legend down cleanly at the center baseline
        {{ rank=sink; LEGEND }}
    }}
    """
    return pid
