import math

# Constant definition for Specific Heat Capacity of water (J/kg·K)
CP_WATER = 4186 

def thermal_load(lpd, tin, tout):
    """
    Calculates the total daily thermal energy requirement of the process.
    Formula: Q = (m * Cp * ΔT) / (3.6 * 10^6) to convert Joules to kWh.
    """
    if lpd <= 0 or tout <= tin:
        return 0.0
    
    q_daily_kwh = (lpd * CP_WATER * (tout - tin)) / 3600000
    return q_daily_kwh


def collector_efficiency(eta0, a1, a2, tm, ta, g):
    """
    Calculates instantaneous thermal efficiency using the standard European 
    quadratic performance equation (EN 12975 / ISO 9806).
    Formula: η = η0 - a1*(ΔT/G) - a2*(ΔT^2/G)
    """
    if g <= 0:
        return 0.0
    
    delta_t = tm - ta
    parameter_x = delta_t / g
    
    eta = eta0 - (a1 * parameter_x) - (a2 * (parameter_x ** 2))
    return max(0.0, eta)


def collectors_required(load, daily_output):
    """
    Calculates the absolute integer count of collectors needed to satisfy the plant load.
    Includes a defensive safety multiplier to account for system piping heat losses.
    """
    if daily_output <= 0:
        return 0
    
    # 1.08 factor accounts for a standard 8% thermal loss across manifold insulation & pipe runs
    system_loss_factor = 1.08 
    total_needed = math.ceil((load / daily_output) * system_loss_factor)
    return max(1, total_needed)


def generate_proposal_analytics(lpd, tin, tout, latitude, eta0, a1, a2, aperture_area):
    """
    EXPERT ANALYSIS GENERATOR FOR PROPOSALS
    Simulates monthly performance over a full fiscal year using real solar geometry 
    to provide the customer with clear seasonal metrics.
    """
    # Standardized regional meteorological database matrix (Clearness Index & Temp Estimates)
    # Format: [Month Name, Mean Peak Irradiance (W/m²), Mean Day Ambient Temp (°C), Day Light Hours]
    climate_matrix = [
        ("January",   750, 22, 5.0),
        ("February",  820, 24, 5.5),
        ("March",     900, 28, 6.0),
        ("April",     980, 32, 6.5),
        ("May",       1050, 35, 7.0),
        ("June",      850, 31, 5.5), # Monsoon/cloud dip simulation
        ("July",      700, 28, 4.5),
        ("August",    720, 27, 4.8),
        ("September", 780, 28, 5.2),
        ("October",   850, 29, 5.8),
        ("November",  800, 26, 5.2),
        ("December",  720, 21, 4.8)
    ]
    
    monthly_data = []
    daily_plant_load = thermal_load(lpd, tin, tout)
    mean_fluid_temp = (tin + tout) / 2.0
    
    for month, monthly_g, monthly_ta, monthly_hours in climate_matrix:
        # 1. Calculate realistic monthly efficiency
        m_eff = collector_efficiency(eta0, a1, a2, mean_fluid_temp, monthly_ta, monthly_g)
        
        # 2. Output per individual module collector (kWh/day)
        kw_instantaneous = (aperture_area * m_eff * monthly_g) / 1000.0
        daily_output_per_collector = kw_instantaneous * monthly_hours
        
        # 3. Size array specifically for the worst-case month (typically January/December) to avoid system undersizing
        req_collectors = collectors_required(daily_plant_load, daily_output_per_collector)
        
        # 4. Calculate real-world metrics for the proposal summary
        actual_field_yield_kwh = daily_output_per_collector * req_collectors
        solar_fraction = min(100.0, (actual_field_yield_kwh / daily_plant_load) * 100)
        
        # Estimate fossil fuel offset savings (Assuming standard industrial light diesel oil boiler at 80% efficiency)
        # 1 Liter of Diesel ≈ 11.6 kWh thermal energy gross
        fuel_saved_liters = (actual_field_yield_kwh / 0.80) / 11.6
        co2_saved_kg = fuel_saved_liters * 2.68 # 2.68 kg CO2 emitted per liter of diesel burned
        
        monthly_data.append({
            "Month": month,
            "Efficiency (%)": round(m_eff * 100, 1),
            "Collector Yield (kWh/day)": round(actual_field_yield_kwh, 1),
            "Solar Fraction (%)": round(solar_fraction, 1),
            "Fuel Saved (Liters/month)": round(fuel_saved_liters * 30, 0),
            "CO2 Mitigated (kg/month)": round(co2_saved_kg * 30, 0)
        })
        
    return daily_plant_load, monthly_data


def simulate_diurnal_curve(tin, tout, ambient, max_irradiance):
    """
    Generates a realistic 24-hour performance curve.
    Crucial for industrial clients to see how water heats up during work shifts.
    """
    hourly_results = []
    mean_fluid_temp = (tin + tout) / 2.0
    
    for hour in range(24):
        # Model solar radiation as a clean bell-curve peaking at 12:00 PM
        if 6 <= hour <= 18:
            # Standard sinusoidal distribution profile for daylight
            angle = math.pi * (hour - 6) / 12
            current_irr = max_irradiance * math.sin(angle)
            current_amb = ambient - 4 + (4 * math.sin(angle - math.pi/3)) # Temp peaks slightly after noon
            
            eff = collector_efficiency(0.78, 3.5, 0.015, mean_fluid_temp, current_amb, current_irr)
            energy_output = eff * current_irr
        else:
            current_irr = 0.0
            current_amb = ambient - 6
            eff = 0.0
            energy_output = 0.0
            
        hourly_results.append({
            "Hour": f"{hour:02d}:00",
            "Irradiance (W/m²)": round(current_irr, 0),
            "Ambient Temp (°C)": round(current_amb, 1),
            "Instantaneous Output (W/m²)": round(energy_output, 1)
        })
        
    return hourly_results
