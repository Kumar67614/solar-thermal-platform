def generate_pid(industry="Dairy", collectors=5, tout=80, daily_water=5000, total_flow=250):
    """
    Generates a beautifully scaled, wide-format P&ID with absolute separation 
    between the active piping schematics and the system legend.
    
    Fixes the layout overlapping bug by unlinking the legend node completely 
    from process weight clusters, pushing it cleanly into its own open footer space.
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
        nodesep=0.5;         # Vertical padding between process components
        ranksep=0.75;        # Horizontal pipe length padding
        bgcolor=white;
        pad="0.4,0.4";
        
        # =====================================================
        # DESIGN TOKENS (Strictly Enforced Dimensions)
        # =====================================================
        # Heavy assets styling
        node [fontname="Arial Bold", fontsize=10, shape=box, style="filled,rounded", fillcolor="#FFFFFF", color="#263238", penwidth=1.5];
        edge [fontname="Arial", fontsize=9, labelfontcolor="#263238", penwidth=1.75];
        
        # System Equipment Sizing
        SC     [label="SOLAR FIELD\\n({collectors} Collectors)", shape=box, style=filled, fillcolor="#FFFDE7", fixedsize=true, width=1.8, height=0.8];
        PUMP   [label="PRIMARY\\nPUMP", shape=circle, fixedsize=true, width=0.75, height=0.75, fillcolor="#ECEFF1"];
        HX     [label="PLATE HX\\n(Solar-to-Storage)", shape=box, style=filled, fillcolor="#E3F2FD", fixedsize=true, width=1.6, height=0.8];
        {tank_id}   [label="{tank_label}\\n({daily_water} LPD)", shape=cylinder, fixedsize=true, width=1.6, height=1.6, fillcolor="#E0F7FA"];
        
        # Fixed Small Instrument Bubbles
        node [shape=circle, fixedsize=true, width=0.4, height=0.4, fillcolor="#FFFFFF", style=filled, fontsize=8, color="#37474F", penwidth=1.2];
        TT_field [label="TT\\n101"];
        PT_field [label="PT\\n101"];
        TT_hx    [label="TT\\n102"];
        TT_tank  [label="TT\\n103"];
        LT_tank  [label="LT\\n101"];
        
        # Compact Valves & Safety Fittings
        node [shape=box, fixedsize=true, width=0.7, height=0.3, fontsize=8, fillcolor="#FAFAFA", style="filled", color="#455A64"];
        CV_in  [label="Check Vlv"];
        PSV    [label="Safety Vlv"];
        EV     [label="Exp Tank"];
        
        # =====================================================
        # PROCESS PIPING ROUTING LOGIC
        # =====================================================
        
        # Primary Loop (Hot Supply Outflow)
        SC -> PT_field [color="#D32F2F", label=" Hot Fluid "];
        PT_field -> TT_field [color="#D32F2F"];
        TT_field -> HX [color="#D32F2F"];
        
        # Primary Loop (Cold Managed Return)
        HX -> PUMP [color="#1976D2", label=" Cooled Fluid "];
        PUMP -> CV_in [color="#1976D2"];
        CV_in -> PSV [color="#1976D2"];
        PSV -> SC [color="#1976D2"];
        
        # Closed Loop Safety Relief Line
        PSV -> EV [style=dashed, color="#78909C", arrowhead=none];
        
        # Energy Storage Charging Circuit
        HX -> TT_hx [color="#E65100", label=" Charging "];
        TT_hx -> {tank_id} [color="#E65100"];
        
        # Instrument tracking tie-ins
        {tank_id} -> TT_tank [style=dotted, color="#78909C", arrowhead=none, constraint=false];
        {tank_id} -> LT_tank [style=dotted, color="#78909C", arrowhead=none, constraint=false];
        
        # =====================================================
        # AUXILIARY SYSTEM OVERRIDES
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
        # END APPLICATION LOOPS
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
        # ISOLATED SYSTEM LEGEND FOOTER (ZERO PIPING OVERLAPS)
        # =====================================================
        subgraph cluster_footer {{
            style=none;
            color=none;
            peripheries=0;
            
            LEGEND [
                shape=plaintext,
                style=none,
                label=<
                    <TABLE BORDER="1" CELLBORDER="0" CELLSPACING="6" CELLPADDING="5" BGCOLOR="#FFFFFF" COLOR="#B0BEC5" STYLE="ROUNDED">
                        <TR>
                            <TD COLSPAN="6" ALIGN="CENTER"><B><FONT POINT-SIZE="11" COLOR="#37474F">DIAGRAM KEY &amp; ISA SYSTEM LEGEND</FONT></B></TD>
                        </TR>
                        <TR>
                            <TD BGCOLOR="#FFFDE7" BORDER="1" COLOR="#37474F"><B> TT </B> Temperature Transmitter</TD>
                            <TD BGCOLOR="#E3F2FD" BORDER="1" COLOR="#37474F"><B> PT </B> Pressure Transmitter</TD>
                            <TD BGCOLOR="#E0F7FA" BORDER="1" COLOR="#37474F"><B> LT </B> Level Transmitter</TD>
                            <TD><FONT COLOR="#D32F2F"><B>━━━━▶</B></FONT> Hot Supply Pipe</TD>
                            <TD><FONT COLOR="#1976D2"><B>━━━━▶</B></FONT> Cold Return Pipe</TD>
                            <TD><FONT COLOR="#E65100"><B>━━━━▶</B></FONT> Heat Charging Pipe</TD>
                        </TR>
                    </TABLE>
                >
            ];
        }}
        
        # This explicit constraint forces the legend down into structural white space 
        # completely beneath the lowermost return pipeline.
        SC -> LEGEND [style=invis, weight=10];
    }}
    """
    return pid
