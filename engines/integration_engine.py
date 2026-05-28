def calculate_pipe_diameter(total_flow):
    """Calculates standard industrial pipe size (DN) based on flow."""
    if total_flow <= 150: return "20"
    elif total_flow <= 400: return "25"
    elif total_flow <= 900: return "32"
    elif total_flow <= 1500: return "40"
    elif total_flow <= 3000: return "50"
    elif total_flow <= 6000: return "65"
    elif total_flow <= 12000: return "80"
    else: return "100"

def recommendations(industry="Dairy", tout=80, tinlet=25, tambient=30, daily_water=5000, total_flow=250):
    """
    Simplified Industrial Proposal Engine.
    Uses pictorial bars and simple English to explain technical design.
    """
    recommended_dn = calculate_pipe_diameter(total_flow)
    
    # Logic for Heat Lift Visual
    approach_delta = tout - tinlet
    heat_lift_pct = min(100, int((approach_delta / 100) * 100))
    
    # 1. FLOW STYLE (Pictorial Indicator)
    if total_flow >= 500:
        flow_style = "High-Efficiency Fast Flow"
        flow_color = "#2E7D32"
        flow_desc = "Water moves fast to <b>soak up maximum heat</b> from the panels. Keeps the system clean and prevents scale buildup."
        flow_bar = "75%"
    else:
        flow_style = "Steady Consistent Flow"
        flow_color = "#1565C0"
        flow_desc = "Water moves slowly to <b>save on electricity</b>. Best for smaller daily needs without wasting pump power."
        flow_bar = "30%"

    # 2. WEATHER PROTECTION
    if tambient < 15:
        weather_style = "Winter & Cold Protection"
        weather_icon = "❄️"
        weather_desc = "The system will automatically <b>protect itself from freezing</b>. No risk of pipe bursts during cold nights."
    else:
        weather_style = "Summer & Heat Optimization"
        weather_icon = "☀️"
        weather_desc = "Designed to <b>shed extra heat</b> safely when the sun is too strong. Keeps the system running cool and safe."

    # 3. INSTALLATION SPACE
    if daily_water >= 6000:
        load_style = "Industrial Ground/Roof Mount"
        load_desc = "The system is heavy (6+ Tons). We will use <b>reinforced steel frames</b> to keep the panels steady in high winds."
        load_bar = "90%"
    else:
        load_style = "Compact Platform Mount"
        load_desc = "A lightweight setup that fits easily on <b>existing roof spaces</b> or maintenance racks with no extra construction."
        load_bar = "45%"

    # Branded Themes
    profiles = {
        "Dairy": {"color": "#1e4620", "accent": "#2E7D32", "bg": "#f4f9f4", "icon": "🥛"},
        "Textile": {"color": "#0d3c61", "accent": "#1565C0", "bg": "#f0f5fa", "icon": "🧵"},
        "Pharmaceutical": {"color": "#4a154b", "accent": "#6A1B9A", "bg": "#faf2fa", "icon": "🧪"},
        "Chemical": {"color": "#E65100", "accent": "#E65100", "bg": "#FFF3E0", "icon": "⚗️"},
        "Food": {"color": "#D32F2F", "accent": "#D32F2F", "bg": "#FFEBEE", "icon": "🍲"}
    }
    p = profiles.get(industry, profiles["Food"])

    # START HTML
    html = f"""
    <div style="font-family: 'Segoe UI', Tahoma, sans-serif; background-color: #fff; padding: 10px; border-radius: 15px; border: 1px solid #eee;">
        
        <div style="background: linear-gradient(135deg, {p['color']}, {p['accent']}); color: white; padding: 30px; border-radius: 12px; margin-bottom: 25px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 style="margin: 0; font-size: 26px;">{industry} Solar Proposal</h1>
                    <p style="margin: 5px 0 0 0; opacity: 0.9;">System Sizing for {daily_water:,} Liters per day</p>
                </div>
                <div style="font-size: 40px;">{p['icon']}</div>
            </div>
            
            <div style="display: flex; gap: 20px; margin-top: 25px; background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; text-align: center;">
                <div style="flex: 1;">
                    <div style="font-size: 11px; opacity: 0.8; text-transform: uppercase;">Heat Gain Goal</div>
                    <div style="font-size: 18px; font-weight: bold;">+{approach_delta}°C</div>
                    <div style="background: #fff; height: 6px; border-radius: 3px; margin-top: 5px; overflow: hidden;">
                        <div style="background: #ffeb3b; width: {heat_lift_pct}%; height: 100%;"></div>
                    </div>
                </div>
                <div style="flex: 1; border-left: 1px solid rgba(255,255,255,0.2);">
                    <div style="font-size: 11px; opacity: 0.8; text-transform: uppercase;">Pipe Thickness</div>
                    <div style="font-size: 18px; font-weight: bold;">DN {recommended_dn}</div>
                    <p style="font-size: 10px; margin: 0;">Standard Size</p>
                </div>
                <div style="flex: 1; border-left: 1px solid rgba(255,255,255,0.2);">
                    <div style="font-size: 11px; opacity: 0.8; text-transform: uppercase;">Climate Health</div>
                    <div style="font-size: 18px; font-weight: bold;">{tambient}°C</div>
                    <p style="font-size: 10px; margin: 0;">Good for Solar</p>
                </div>
            </div>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
            
            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0;">
                <h3 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 18px;">🛠️ Pipe & Infrastructure</h3>
                <div style="background: #fff; padding: 10px; border-radius: 5px; margin-bottom: 10px; font-weight: bold; border-left: 4px solid {p['accent']};">
                    Material: Food-Grade Stainless Steel
                </div>
                <p style="font-size: 13px; color: #555;">High-quality pipes that won't rust and keep your water 100% clean for {industry} use.</p>
            </div>

            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0;">
                <h3 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 18px;">💧 Water Flow Style</h3>
                <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 5px;">
                    <span>Slow</span><span style="color: {flow_color}; font-weight: bold;">{flow_style}</span><span>Fast</span>
                </div>
                <div style="background: #ddd; height: 12px; border-radius: 6px; margin-bottom: 15px;">
                    <div style="background: {flow_color}; width: {flow_bar}; height: 100%; border-radius: 6px;"></div>
                </div>
                <p style="font-size: 13px; color: #555;">{flow_desc}</p>
            </div>

            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0;">
                <h3 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 18px;">{weather_icon} Weather Ready</h3>
                <div style="background: #fff; padding: 10px; border-radius: 5px; margin-bottom: 10px; font-weight: bold; border-left: 4px solid #f44336;">
                    Strategy: {weather_style}
                </div>
                <p style="font-size: 13px; color: #555;">{weather_desc}</p>
            </div>

            <div style="background: {p['bg']}; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0;">
                <h3 style="margin: 0 0 10px 0; color: {p['color']}; font-size: 18px;">🏗️ Installation Type</h3>
                <div style="font-size: 12px; margin-bottom: 5px;"><b>Support Level:</b> {load_style}</div>
                <div style="background: #ddd; height: 12px; border-radius: 6px; margin-bottom: 15px;">
                    <div style="background: #333; width: {load_bar}; height: 100%; border-radius: 6px;"></div>
                </div>
                <p style="font-size: 13px; color: #555;">{load_desc}</p>
            </div>

        </div>

        <div style="margin-top: 25px; padding: 15px; background: #fffde7; border-left: 5px solid #fbc02d; font-size: 12px;">
            <b>Note for Customer:</b> This setup replaces expensive electricity or diesel with free sun energy. It is designed to work for 15-20 years with low maintenance.
        </div>
    </div>
    """
    return html
