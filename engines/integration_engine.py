def generate_integration_report(process_load_kwh, modules_count, field_area_m2, flow_rate_lph, main_pipe_dn):
    """
    Generates a dynamic pictorial system blueprint diagram and customized 
    integration instructions matching the customer's exact site metrics.
    """
    
    # 1. Dynamically build the pictorial layout block based on customer footprint size
    # We alter the visual size of the collector array block to represent system scale.
    if modules_count >= 50:
        array_visual = "│   [===] [===] [===] [===]   │ (Large Field Array)"
        scale_label  = "LARGE INDUSTRIAL SYSTEM"
    elif modules_count >= 40:
        array_visual = "│      [===] [===] [===]      │ (Medium Field Array)"
        scale_label  = "MEDIUM INDUSTRIAL SYSTEM"
    else:
        array_visual = "│         [===] [===]         │ (Small Field Array)"
        scale_label  = "SMALL COMMERCIAL SYSTEM"

    # 2. Construct the customized pictorial diagram string
    diagram = f"""
    ========================================================================================
    PICTORIAL INTEGRATION SCHEMATIC: {scale_label}
    ========================================================================================
    
       [ SUNLIGHT ] ──> (Target Load: {process_load_kwh} kWh/Day)
            │
            ▼
      ┌──────────────────────────────┐
      │     SOLAR COLLECTOR FIELD    │
      {array_visual}
      │   Total Modules: {modules_count} Units     │ Size: {field_area_m2} m²
      └──────────────────────────────┘
            │                                         
            │ Hot Water Outflow ({flow_rate_lph} LPH via DN {main_pipe_dn} Pipe)
            ▼                                         
      ┌──────────────────────────────┐                ┌──────────────────────────────┐
      │   AUTOMATIC 3-WAY VALVES     │──────────────> │   CENTRAL HEAT EXCHANGER     │
      │ (Air & Pressure Relief Safety)│                │ (Isolates Solar & Boiler Eco)│
      └──────────────────────────────┘                └──────────────────────────────┘
            ▲                                                         │
            │                                                         │ Closed Loop
            │ Pumped Cold Return Fluid                                │ Clean Return
      ┌──────────────────────────────┐                                │
      │  HYDRAULIC LOOP WATER PUMP   │ <──────────────────────────────┘
      └──────────────────────────────┘
    ========================================================================================
    """

    # 3. Generate tailored, clear on-site instructions that ingest the real metrics
    steps = [
        {
            "phase": "Phase 1: Collector Field Foundation & Assembly",
            "action": (
                f"Assemble the metal support frames to host exactly {modules_count} Solar Thermal Units. "
                f"Ensure the structural footprint safely spans across the designated {field_area_m2} m² area. "
                "Secure all ground anchor bolts to handle crosswind load parameters securely."
            )
        },
        {
            "phase": "Phase 2: Main Hydraulic Plumbing Network",
            "action": (
                f"Plumb the primary distribution headers using heavy-duty DN {main_pipe_dn} piping. "
                f"This thickness ensures a balanced fluid velocity for the target loop delivery flow rate of {flow_rate_lph} LPH. "
                "Wrap all external hot-water conduits with thick foam insulation shielding to stop heat loss."
            )
        },
        {
            "phase": "Phase 3: Thermal Loop Integration",
            "action": (
                f"Tie the system into the factory hot water line via the central heat exchanger. "
                f"Verify that the system can reliably harvest up to {process_load_kwh} kWh of daily solar heat. "
                "Position the safety pressure and automated 3-way air-release valves at the highest physical bends."
            )
        },
        {
            "phase": "Phase 4: Sensor Controls Calibration & Startup",
            "action": (
                "Insert thermal monitoring probes inside the module headers and clean water tanks. "
                "Boot up the control screen dashboard panel, verify active valve switching ranges, "
                "and execute an initial 60-minute continuous water pressure test to eliminate plumbing leaks."
            )
        }
    ]

    return {
        "diagram": diagram,
        "steps": steps
    }


# ==========================================
# SIMULATING DIFFERENT CUSTOMER APPLICATIONS
# ==========================================
if __name__ == "__main__":
    print("\n--- SIMULATION 1: RUNNING CUSTOMER CASE A (FROM DASHBOARD DATA) ---")
    # Simulating data matching the 42 Collector dashboard display
    customer_a_report = generate_integration_report(
        process_load_kwh=279.1,
        modules_count=42,
        field_area_m2=512.4,
        flow_rate_lph=2100.0,
        main_pipe_dn=25
    )
    
    print(customer_a_report["diagram"])
    for step in customer_a_report["steps"]:
        print(f"[*] {step['phase']}\n    {step['action']}\n")


    print("\n--- SIMULATION 2: RUNNING CUSTOMER CASE B (LARGE SCALED FIELD) ---")
    # Simulating data matching the 52 Collector high-yield dashboard display
    customer_b_report = generate_integration_report(
        process_load_kwh=348.8,
        modules_count=52,
        field_area_m2=634.4,
        flow_rate_lph=2600.0,
        main_pipe_dn=25
    )
    
    print(customer_b_report["diagram"])
    for step in customer_b_report["steps"]:
        print(f"[*] {step['phase']}\n    {step['action']}\n")
