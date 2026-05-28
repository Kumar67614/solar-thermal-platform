import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

def spacing(height, tilt, latitude):
    """
    Calculates the minimum safe inter-row distance to prevent mutual shading 
    during the Winter Solstice (worst-case solar altitude angle).
    """
    # Winter Solstice solar altitude angle at noon
    winter_altitude = 90 - abs(latitude + 23.45)
    
    # Calculate shadow length based on the elevated height of the collector slant
    s = (height * math.sin(math.radians(tilt))) / math.tan(math.radians(winter_altitude))
    
    # Return calculated spacing with a standard 0.5m maintenance clearance buffer
    return s + 0.5

def draw_layout(rows, cols, width, height, pitch, tilt=30, latitude=23.5):
    """
    Generates a professional, dual-perspective architectural engineering layout map 
    illustrating row-pitch metrics and inter-collector spacing parameters.
    """
    # 1. Initialize a professional, clean canvas layout
    fig = plt.figure(figsize=(15, 9), facecolor="#ffffff")
    
    # Use GridSpec to present a main field overview alongside a clear side-profile key
    gs = fig.add_gridspec(1, 4, wspace=0.4)
    ax_main = fig.add_subplot(gs[0, 0:3])   # 2D Aerial Field Map Matrix
    ax_side = fig.add_subplot(gs[0, 3])     # 1D Mechanical Elevation Cross-Section
    
    col_gap = 0.35  # Inter-module maintenance gap within the same row line
    
    # --- PLOT 1: AERIAL FIELD VIEW ARRAY ---
    # Render collectors systematically across rows and columns
    for r in range(rows):
        for c in range(cols):
            x = c * (width + col_gap)
            y = r * pitch
            
            # Draw industrial collector module shell layout
            rect = patches.Rectangle(
                (x, y), width, height,
                linewidth=1.5, edgecolor='#1E3A8A', facecolor='#60A5FA', alpha=0.85
            )
            ax_main.add_patch(rect)
            
            # Subtle grid panel lines to mimic commercial solar thermal tubes
            for step in range(1, 5):
                ax_main.plot(
                    [x + (step * width / 5), x + (step * width / 5)], 
                    [y, y + height], 
                    color='#1D4ED8', linewidth=0.5, alpha=0.4
                )

    # Calculate real-world bounds based on cumulative component values
    field_width = cols * (width + col_gap) - col_gap
    calculated_spacing = pitch - height

    # Dimension Indicator Lines: Inter-Module Maintenance Gap (Within Row Line)
    if cols > 1:
        gap_x = width
        gap_y = height / 2
        ax_main.annotate('', xy=(gap_x, gap_y), xytext=(gap_x + col_gap, gap_y),
                         arrowprops=dict(arrowstyle='<->', color='#DC2626', linewidth=1.5))
        ax_main.text(gap_x + (col_gap / 2), gap_y + 0.1, f"{col_gap}m\nGap", 
                     color='#DC2626', fontsize=9, ha='center', va='bottom', weight='bold')

    # Dimension Indicator Lines: Inter-Row Spacing (Minimum Safe Distance Window)
    if rows > 1:
        dim_x = field_width * 0.4
        ax_main.annotate('', xy=(dim_x, height), xytext=(dim_x, pitch),
                         arrowprops=dict(arrowstyle='<->', color='#16A34A', linewidth=2))
        ax_main.text(dim_x + 0.15, (height + pitch) / 2, f"Safe Distance: {calculated_spacing:.2f} m\n(Zero Shading Zone)", 
                     color='#15803D', fontsize=10, ha='left', va='center', weight='bold')

        # Dimension Indicator Lines: Total Core Row Pitch Boundary Tracking
        pitch_x = field_width * 0.85
        ax_main.annotate('', xy=(pitch_x, 0), xytext=(pitch_x, pitch),
                         arrowprops=dict(arrowstyle='<->', color='#2563EB', linewidth=2))
        ax_main.text(pitch_x + 0.15, pitch / 2, f"Total Row Pitch\n= {pitch:.2f} m", 
                     color='#1D4ED8', fontsize=11, ha='left', va='center', weight='bold')

    # Polish Aerial Map Frame Environment
    ax_main.set_xlim(-0.5, max(field_width + 1.0, 5))
    ax_main.set_ylim(-0.5, max((rows - 1) * pitch + height + 1.5, 5))
    ax_main.set_aspect('equal')
    ax_main.set_title("SOLAR COLLECTOR FIELD LAYOUT (TOP-DOWN VIEW)", color='#1E293B', fontsize=13, weight='bold', pad=15)
    ax_main.set_xlabel("Horizontal Field Footprint Distance (meters)", fontsize=10, color='#475569')
    ax_main.set_ylabel("Vertical Field Flow Distance (meters)", fontsize=10, color='#475569')
    ax_main.grid(True, linestyle='--', alpha=0.3, color='#94A3B8')

    # --- PLOT 2: SIDE-PROFILE SHADOW ELEVATION MAP ---
    # Structural Ground Baseline Representation
    ax_side.axhline(0, color='#475569', linewidth=3, zorder=1)
    
    # Calculate triangular trigonometry for tilt representation
    slant_radians = math.radians(tilt)
    dx = height * math.cos(slant_radians)
    dy = height * math.sin(slant_radians)
    
    # Draw Row 1 slant profile layout
    ax_side.plot([0, dx], [0, dy], color='#1E3A8A', linewidth=4, label='Collector Slant')
    ax_side.plot([dx, dx], [0, dy], color='#94A3B8', linestyle=':', linewidth=1.5) # Support bracket line
    
    # Draw Row 2 slant profile layout positioned at the calculated pitch marker
    ax_side.plot([pitch, pitch + dx], [0, dy], color='#1E3A8A', linewidth=4)
    ax_side.plot([pitch + dx, pitch + dx], [0, dy], color='#94A3B8', linestyle=':', linewidth=1.5)

    # Trace critical winter solar shadow ray vector paths
    winter_alt_rad = math.radians(90 - abs(latitude + 23.45))
    ray_length = dy / math.tan(winter_alt_rad)
    ax_side.plot([dx, dx + ray_length], [dy, 0], color='#EA580C', linestyle='--', linewidth=2, label='Lowest Solstice Sun Ray')
    
    # Safe Inter-Row Distance Callout
    ax_side.annotate('', xy=(dx, -0.1), xytext=(pitch, -0.1),
                     arrowprops=dict(arrowstyle='<->', color='#16A34A', linewidth=1.5))
    ax_side.text((dx + pitch) / 2, -0.2, f"Clear Space\n{calculated_spacing:.2f}m", 
                 color='#15803D', fontsize=9, ha='center', va='top', weight='bold')

    # Angle Marker Curved Representation Arc
    ax_side.text(0.3, 0.1, f"{tilt}°", color='#1E3A8A', fontsize=9, weight='bold')

    # Polish Elevation Frame Environment
    ax_side.set_xlim(-0.5, pitch + dx + 0.5)
    ax_side.set_ylim(-0.5, dy + 0.8)
    ax_side.set_aspect('equal')
    ax_side.set_title("ELEVATION SHADOW ANALYSIS", color='#1E293B', fontsize=11, weight='bold', pad=15)
    ax_side.get_xaxis().set_ticks([]) # Remove clean canvas labels to emphasize spacing dimensions
    ax_side.get_yaxis().set_ticks([])
    ax_side.legend(loc='upper right', fontsize=8)
    ax_side.spines['top'].set_visible(False)
    ax_side.spines['right'].set_visible(False)
    ax_side.spines['left'].set_visible(False)
    ax_side.spines['bottom'].set_visible(False)

    return fig
