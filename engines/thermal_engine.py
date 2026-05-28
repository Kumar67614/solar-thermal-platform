# =====================================================
# THERMAL TAB (EXECUTIVE VISUALIZATION DISPLAY)
# =====================================================

with tabs[1]:
    st.header("Advanced Thermal Analysis & Proposal Metrics")
    st.markdown("---")

    # 1. Execute the comprehensive simulation calculations
    daily_plant_load, monthly_analytics_list = generate_proposal_analytics(
        lpd=daily_water,
        tin=tin,
        tout=tout,
        latitude=latitude,
        eta0=eta0,
        a1=a1,
        a2=a2,
        aperture_area=aperture_area
    )
    
    df_analytics = pd.DataFrame(monthly_analytics_list)

    # 2. Key Performance Metric Highlights
    st.subheader("Annualized Projected Savings Summary")
    summary_col1, summary_col2, summary_col3 = st.columns(3)
    
    total_annual_fuel_saved = df_analytics["Fuel Saved (Liters/month)"].sum()
    total_annual_co2_saved = df_analytics["CO2 Mitigated (kg/month)"].sum()
    average_solar_fraction = df_analytics["Solar Fraction (%)"].mean()

    summary_col1.metric(
        label="🔥 Total Fuel Displaced Annually",
        value=f"{total_annual_fuel_saved:,.0f} Liters / Year"
    )
    summary_col2.metric(
        label="🌱 Carbon Footprint Reduction",
        value=f"{(total_annual_co2_saved / 1000):,.1f} Metric Tons CO2"
    )
    summary_col3.metric(
        label="☀️ Average Solar Fraction",
        value=f"{average_solar_fraction:.1f} % Contribution"
    )
    
    st.markdown("---")

    # 3. Interactive Graphical Proposal Visualizations (Side-by-Side Panels)
    st.subheader("Executive Proposal Performance Dashboards")
    graph_col1, graph_col2 = st.columns(2)
    
    # Generate presentation charts from our upgraded plotting module
    fig_perf, fig_save = create_proposal_plots(df_analytics)
    
    with graph_col1:
        st.plotly_chart(fig_perf, use_container_width=True, key='proposal_seasonal_performance')
        
    with graph_col2:
        st.plotly_chart(fig_save, use_container_width=True, key='proposal_financial_sustainability')

    st.markdown("---")

    # 4. Verification Data Grid
    st.subheader("Seasonal Performance Matrix (Month-by-Month Simulation Verification)")
    st.dataframe(
        df_analytics,
        column_config={
            "Month": "Operational Month",
            "Efficiency (%)": st.column_config.NumberColumn("Avg Efficiency", format="%d%%"),
            "Collector Yield (kWh/day)": st.column_config.NumberColumn("Daily Energy Yield", format="%.1f kWh"),
            "Solar Fraction (%)": st.column_config.NumberColumn("Boiler Offset", format="%.1f%%"),
            "Fuel Saved (Liters/month)": st.column_config.NumberColumn("Fuel Saved", format="%d L"),
            "CO2 Mitigated (kg/month)": st.column_config.NumberColumn("CO2 Saved", format="%d kg"),
        },
        hide_index=True,
        use_container_width=True
    )
