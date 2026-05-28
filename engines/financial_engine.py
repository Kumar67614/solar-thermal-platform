import numpy as np
import pandas as pd

def calculate_market_project_cost(total_area, collector_type="Flat Plate Collector"):
    """
    Calculates commercial project costs using real industrial market rates in India.
    Includes base collector arrays, support structures, plumbing, and integration labor.
    """
    # Market cost per square meter (including structural engineering and integration)
    if collector_type == "Flat Plate Collector":
        rate_per_m2 = 11500  # Average base cost for premium copper FPC systems
    else:
        rate_per_m2 = 14500  # Average cost for pressurized, high-grade industrial ETC systems
        
    base_cost = total_area * rate_per_m2
    
    # Industrial project overhead multipliers
    civil_and_mounting_labor = base_cost * 0.12  # 12% on-site labor cost
    freight_and_engineering = base_cost * 0.06   # 6% logistics & structural sign-off
    
    total_estimated_investment = base_cost + civil_and_mounting_labor + freight_and_engineering
    return total_estimated_investment


def calculate_real_annual_savings(annual_energy_yield_kwh, fuel_cost_per_kwh):
    """
    Calculates year-one gross cash savings derived directly from displaced boiler fuel.
    """
    if annual_energy_yield_kwh <= 0 or fuel_cost_per_kwh <= 0:
        return 0.0
    return float(annual_energy_yield_kwh * fuel_cost_per_kwh)


def calculate_dynamic_payback(initial_investment, year_one_savings, fuel_escalation=0.06, annual_degradation=0.01, opex_rate=0.02):
    """
    Calculates true breakeven payback by running an iterative timeline loop.
    Accounts for fuel inflation, system degradation, and ongoing maintenance costs.
    """
    if year_one_savings <= 0:
        return float('inf')
        
    cumulative_cash_position = -initial_investment
    current_year_savings = year_one_savings
    running_years = 0.0
    
    # Iterate through a standard 25-year operational lifecycle window
    for year in range(1, 26):
        # Subtract annual maintenance costs (typically 2% of initial hardware cost)
        annual_maintenance_opex = initial_investment * opex_rate
        
        net_cash_flow_this_year = current_year_savings - annual_maintenance_opex
        
        if cumulative_cash_position + net_cash_flow_this_year >= 0:
            # Linear interpolation for fractional payback year accuracy
            fractional_year_remaining = abs(cumulative_cash_position) / net_cash_flow_this_year
            return float(running_years + fractional_year_remaining)
            
        cumulative_cash_position += net_cash_flow_this_year
        running_years += 1.0
        
        # Advance economic parameters for the following year
        current_year_savings *= (1.0 + fuel_escalation)   # Fuel gets more expensive
        current_year_savings *= (1.0 - annual_degradation) # Collectors lose minor efficiency
        
    return float(running_years)


def calculate_comprehensive_npv(initial_investment, year_one_savings, lifecycle_years=20, discount_rate=0.08, fuel_escalation=0.06, annual_degradation=0.01, opex_rate=0.02):
    """
    Computes Net Present Value using a compound model that matches standard accounting practices.
    """
    discounted_cash_flows = []
    current_year_savings = year_one_savings
    
    for year in range(1, lifecycle_years + 1):
        annual_maintenance_opex = initial_investment * opex_rate
        net_cash_flow = current_year_savings - annual_maintenance_opex
        
        # Discount future cash values back to present terms
        present_value_factor = (1.0 + discount_rate) ** year
        discounted_cash_flow = net_cash_flow / present_value_factor
        
        # FIXED: Variable name typo corrected here to match properly
        discounted_cash_flows.append(discounted_cash_flow)
        
        # Advance economic parameters for the following year
        current_year_savings *= (1.0 + fuel_escalation)
        current_year_savings *= (1.0 - annual_degradation)
        
    net_present_value = -initial_investment + sum(discounted_cash_flows)
    return float(net_present_value)


def generate_financial_timeline_dataframe(initial_investment, year_one_savings, lifecycle_years=15, discount_rate=0.08, fuel_escalation=0.06, annual_degradation=0.01, opex_rate=0.02):
    """
    Generates a structured timeline matrix used to feed the platform's Plotly graphs.
    """
    timeline_records = []
    cumulative_net_benefit = -initial_investment
    current_year_savings = year_one_savings
    
    # Year 0: Initial Capital Outlay
    timeline_records.append({
        "Year": 0,
        "Annual Cash Flow (₹)": -initial_investment,
        "Cumulative Cash Position (₹)": cumulative_net_benefit
    })
    
    for year in range(1, lifecycle_years + 1):
        annual_maintenance_opex = initial_investment * opex_rate
        net_cash_flow = current_year_savings - annual_maintenance_opex
        cumulative_net_benefit += net_cash_flow
        
        timeline_records.append({
            "Year": year,
            "Annual Cash Flow (₹)": round(net_cash_flow, 2),
            "Cumulative Cash Position (₹)": round(cumulative_net_benefit, 2)
        })
        
        current_year_savings *= (1.0 + fuel_escalation)
        current_year_savings *= (1.0 - annual_degradation)
        
    return pd.DataFrame(timeline_records)
