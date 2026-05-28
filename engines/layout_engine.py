import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

def spacing(height, tilt, latitude):
    """
    Calculates the minimum safe inter-row distance to prevent mutual shading 
    during the Winter Solstice (worst-case solar altitude angle).
    """
    winter_altitude = 90 - abs(latitude + 23.45)
    
    # Shadow length cast past the base of the collector panel
    s = (height * math.sin(math.radians(tilt))) / math.tan(math.radians(winter_altitude))
    
    # Return calculated spacing with a standard maintenance clearance buffer
    return s + 0.5

def draw_layout(rows, cols, width, height, pitch, tilt=30, latitude=23.5):
    """
    Generates a professional, non-overlapping architectural layout map 
    with clear visual dimension markings on outer margins.
    """
    # 1. Canvas Setup
    fig = plt.figure(figsize=(16, 8), facecolor="#ffffff")
    gs = fig.add_gridspec(1, 4, wspace=0.35)
    
    ax_main = fig.add_subplot(gs[0, 0:3])   # Top-Down Aerial Grid Map
    ax_side = fig.add_subplot(gs[0, 3])     # Side Profile Elevation View
    
    col_gap = 0.35  # Set gap distance between modules in a row
    
    # Compute system geometric physical limits
    panel_ground_projection = height * math.cos(math.radians(tilt))
    calculated_spacing = pitch - panel_ground_projection
    
    field_width = cols * width + (cols - 1) * col_gap
    field_length = (rows - 1) * pitch + height
    
    # --- PLOT 1: CLEAN AERIAL FIELD MATRIX ---
    for r in range(rows):
        y_base = r * pitch
        for c in range(cols):
            x_base = c * (width + col_gap)
            
            # Draw primary collector frame structure
            rect = patches.Rectangle(
                (x_base, y_base), width, height,
                linewidth=1.2, edgecolor='#1E3A8A', facecolor='#bae6fd', zorder=2
            )
            ax_main.add_patch(rect)
            
            # Internal tube texture lines for an industrial look
            for step in range(1, 4):
                line_x = x_base + (step * width / 4)
                ax_main.plot([line_x, line_x], [y_base, y_base + height], 
                             color='#0284c7', linewidth=0.6, alpha=0.3, zorder=3)

    # --- EXTERIOR MARGIN DIMENSION LINES (Prevents Internal Overlapping) ---
    # 1. Inter-Module Side Gap Dimension Label
    if cols > 1:
        gap_x1 = width
        gap_x2 = width + col_gap
        gap_y = field_length + (height * 0.15)
        
        ax_main.plot([gap_x1, gap_x1], [field_length, gap_y + 0.1], color='#dc2626', linestyle=':', linewidth=1)
        ax_main.plot([gap_x2, gap_x2], [field_length, gap_y + 0.1], color='#dc2626', linestyle=':', linewidth=1)
        ax_main.annotate('', xy=(gap_x1, gap_y), xytext=(gap_x2, gap_y),
                         arrowprops=dict(arrowstyle='<->', color='#dc2626', linewidth=1.2))
        ax_main.text((gap_x1 + gap_x2) / 2, gap_y + 0.05, f"{col_gap}m Gap", 
                     color='#dc2626', fontsize=9, ha='center', va='bottom', weight='bold')

    # 2. Total Row Pitch Dimension Label (Placed on Left Margin)
    if rows > 1:
        pitch_x = -(field_width * 0.12)
        ax_main.plot([0, pitch_x - 0.1], [0, 0], color='#2563eb', linestyle=':', linewidth=1)
        ax_main.plot([0, pitch_x - 0.1], [pitch, pitch], color='#2563eb', linestyle=':', linewidth=1)
        ax_main.annotate('', xy=(pitch_x, 0), xytext=(pitch_x, pitch),
                         arrowprops=dict(arrowstyle='<->', color='#2563eb', linewidth=1.5))
        ax_main.text(pitch_x - 0.05, pitch / 2, f"Total Row Pitch\n= {pitch:.2f} m", 
                     color='#1d4ed8', fontsize=10, ha='right', va='center', weight='bold')

        # 3. Clean Clearance Space Dimension Label (Placed on Right Margin)
        clear_x = field_width + (field_width * 0.12)
        ax_main.plot([field_width, clear_x + 0.1], [height, height], color='#16a34a', linestyle=':', linewidth=1)
        ax_main.plot([field_width, clear_x + 0.1], [pitch, pitch], color='#16a34a', linestyle=':', linewidth=1)
        ax_main.annotate('', xy=(clear_x, height), xytext=(clear_x, pitch),
                         arrowprops=dict(arrowstyle='<->', color='#16a34a', linewidth=1.5))
        
        status_text = "Zero Shading" if calculated_spacing >= 0.4 else "Warning: Shading Risk"
        ax_main.text(clear_x + 0.05, (height + pitch) / 2, 
                     f"Clear Space: {calculated_spacing:.2f} m\n({status_text})", 
                     color='#15803d', fontsize=10, ha='left', va='center', weight='bold')

    # Polish Aerial Map Frame Boundaries
    margin_factor_x = max(field_width * 0.25, 1.5)
    margin_factor_y = max(field_length * 0.15, 1.0)
    ax_main.set_xlim(-margin_factor_x, field_width + margin_factor_x)
    ax_main.set_ylim(-margin_factor_y, field_length + margin_factor_y)
    ax_main.set_aspect('equal')
    
    ax_main.set_title("SOLAR FIELD LAYOUT PLAN VIEW", color='#0f172a', fontsize=13, weight='bold', pad=15)
    ax_main.set_xlabel("Field Width Footprint (meters)", fontsize=10, color='#475569')
    ax_main.set_ylabel("Field Depth Flow Distance (meters)", fontsize=10, color='#475569')
    ax_main.grid(True, linestyle='--', alpha=0.25, color='#cbd5e1')

    # --- PLOT 2: SIDE-PROFILE SHADOW ELEVATION MAP ---
    ax_side.axhline(0, color='#475569', linewidth=2.5, zorder=1)
    
    # Calculate geometric coordinate deltas for slant profiles
    slant_rad = math.radians(tilt)
    dx = height * math.cos(slant_rad)
    dy = height * math.sin(slant_rad)
    
    # Draw Row 1 Slant Frame
    ax_side.plot([0, dx], [0, dy], color='#1e3a8a', linewidth=3.5, zorder=3, label='Collector')
    ax_side.plot([dx, dx], [0, dy], color='#94a3b8', linestyle=':', linewidth=1.2)
    
    # Draw Row 2 Slant Frame
    ax_side.plot([pitch, pitch + dx], [0, dy], color='#1e3a8a', linewidth=3.5, zorder=3)
    ax_side.plot([pitch + dx, pitch + dx], [0, dy], color='#94a3b8', linestyle=':', linewidth=1.2)

    # Trace winter solar ray shadow paths
    winter_alt_rad = math.radians(90 - abs(latitude + 23.45))
    ray_length = dy / math.tan(winter_alt_rad)
    ax_side.plot([dx, dx + ray_length], [dy, 0], color='#ea580c', linestyle='--', linewidth=1.8, label='Solstice Sun Ray')
    
    # Add a visual ground shade patch zone safely underneath the arrays
    shade_patch = patches.Polygon([[dx, 0], [dx, dy], [dx + ray_length, 0]], facecolor='#f8fafc', alpha=0.7, zorder=2)
    ax_side.add_patch(shade_patch)
    
    # Dimension lines for clearance space
    ax_side.annotate('', xy=(dx, -0.08), xytext=(pitch, -0.08),
                     arrowprops=dict(arrowstyle='<->', color='#16a34a', linewidth=1.2))
    ax_side.text((dx + pitch) / 2, -0.15, f"Clear space\n{calculated_spacing:.2f}m", 
                 color='#15803d', fontsize=9, ha='center', va='top', weight='bold')

    # Draw Tilt Angle Text cleanly at the base pivot point
    ax_side.text(0.12, 0.05, f"{tilt}°", color='#1d4ed8', fontsize=9, weight='bold')

    # Polish Profile View Frame Properties
    ax_side.set_xlim(-0.3, pitch + dx + 0.6)
    ax_side.set_ylim(-0.4, dy + 0.6)
    ax_side.set_aspect('equal')
    ax_side.set_title("ELEVATION SHADOW MAP", color='#0f172a', fontsize=11, weight='bold', pad=15)
    ax_side.axis('off') # Clean representation without frame borders
    ax_side.legend(loc='upper right', fontsize=8, framealpha=0.9)

    return fig
