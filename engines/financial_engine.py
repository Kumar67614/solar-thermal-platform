import numpy as np
import pandas as pd

def calculate_market_project_cost(total_area, collector_type="Flat Plate Collector"):
    """
    Calculates realistic industrial project costs using step-down commercial brackets.
    Accounts for volume discounts on large installations to prevent inflated costs.
    """
    if total_area <= 0:
        return 0.0
        
    # Step-down pricing per m2 based on system scale (Economy of Scale)
    if collector_type == "Flat Plate Collector":
        if total_area < 50:
            rate_per_m2 = 8500
        elif total_area < 150:
            rate_per_m2 = 7000
        else:
            rate_per_m2 = 5500  # Large commercial rate for bulk FPC installations
    else:  # Evacuated Tube Collectors (ETC)
        if total_area < 50:
            rate_per_m2 = 10500
        elif total_area < 150:
            rate_per_m2 = 9000
        else:
            rate_per_m2 = 7200  # Large commercial rate for bulk ETC installations
            
    # Base hardware cost calculation
    base_hardware_cost = total_area * rate_per_m2
    
    # Standard industrial overhead percentages calculated from base hardware cost
    civil_mounting_structure = base_hardware_cost * 0.10  # 10% for steel support racking
    piping_pumps_valves = base_hardware_cost * 0.08       # 8% for the hydraulic loop plumbing
    labor_integration_commissioning = base_hardware_cost * 0.07 # 7% engineering setup labor
    
    total_project_capex = (
        base_hardware_cost + 
        civil_mounting_structure + 
        piping_pumps_valves + 
        labor_integration_commissioning
    )
    
    return float(total_project_capex)


def calculate_real_annual_savings(annual_energy_yield_kwh, fuel_cost_per_kwh):
    """Calculates year-one gross cash savings derived from displaced boiler fuel."""
    if annual_energy_yield_kwh <= 0 or fuel_cost_per_kwh <= 0:
        return 0.0
    return float(annual_energy_yield_kwh * fuel_cost_per_kwh)


def calculate_dynamic_payback(initial_investment, year_one_savings, fuel_escalation=0.06, annual_degradation=0.01, opex_rate=0.015):
    """Calculates dynamic breakeven payback period with fuel escalation and maintenance costs."""
    if year_one_savings <= 0 or initial_investment <= 0:
        return float('inf')
        
    cumulative_cash_position = -initial_investment
    current_year_savings = year_one_savings
    running_years = 0.0
    
    for year in range(1, 26):
        # Industrial maintenance cost (1.5% of initial hardware cost)
        annual_opex = initial_investment * opex_rate
        net_cash_flow = current_year_savings - annual_opex
        
        if cumulative_cash_position + net_cash_flow >= 0:
            fractional_year = abs(cumulative_cash_position) / net_cash_flow
            return float(running_years + fractional_year)
            
        cumulative_cash_position += net_cash_flow
        running_years += 1.0
        
        current_year_savings *= (1.0 + fuel_escalation)
        current_year_savings *= (1.0 - annual_degradation)
        
    return float(running_years)


def calculate_comprehensive_npv(initial_investment, year_one_savings, lifecycle_years=20, discount_rate=0.08, fuel_escalation=0.06, annual_degradation=0.01, opex_rate=0.015):
    """Computes Net Present Value (NPV) across system lifecycle window."""
    if initial_investment <= 0:
        return 0.0
    discounted_cash_flows = []
    current_year_savings = year_one_savings
    
    for year in range(1, lifecycle_years + 1):
        annual_opex = initial_investment * opex_rate
        net_cash_flow = current_year_savings - annual_opex
        
        present_value_factor = (1.0 + discount_rate) ** year
        discounted_cash_flow = net_cash_flow / present_value_factor
        discounted_cash_flows.append(discounted_cash_flow)
        
        current_year_savings *= (1.0 + fuel_escalation)
        current_year_savings *= (1.0 - annual_degradation)
        
    return float(-initial_investment + sum(discounted_cash_flows))


def generate_financial_timeline_dataframe(initial_investment, year_one_savings, lifecycle_years=15, discount_rate=0.08, fuel_escalation=0.06, annual_degradation=0.01, opex_rate=0.015):
    """Generates financial matrix dataframe for plot timelines."""
    timeline_records = []
    cumulative_net_benefit = -initial_investment
    current_year_savings = year_one_savings
    
    timeline_records.append({
        "Year": 0,
        "Annual Cash Flow (₹)": -initial_investment,
        "Cumulative Cash Position (₹)": cumulative_net_benefit
    })
    
    for year in range(1, lifecycle_years + 1):
        annual_opex = initial_investment * opex_rate
        net_cash_flow = current_year_savings - annual_opex
        cumulative_net_benefit += net_cash_flow
        
        timeline_records.append({
            "Year": year,
            "Annual Cash Flow (₹)": round(net_cash_flow, 2),
            "Cumulative Cash Position (₹)": round(cumulative_net_benefit, 2)
        })
        
        current_year_savings *= (1.0 + fuel_escalation)
        current_year_savings *= (1.0 - annual_degradation)
        
    return pd.DataFrame(timeline_records)
