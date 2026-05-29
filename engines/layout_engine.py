import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

def draw_layout(rows, cols, width, height, pitch, tilt=30, latitude=23.5):
    """
    Generates an industrial-standard solar thermal field engineering layout blueprint.
    Completely responsive: automatically adjusts spacing dimensions, checking for 
    structural overlaps and shifting boundaries dynamically based on input coordinates.
    """
    # 1. DYNAMIC RESPONSIVE GEOMETRIC MATH
    # Convert panel slant length into true ground shadow/footprint projection
    panel_ground_footprint = height * math.cos(math.radians(tilt))
    
    # Calculate the exact midday solar altitude angle on the Winter Solstice (worst case)
    winter_solstice_altitude = 90.0 - abs(latitude + 23.45)
    vertical_rise = height * math.sin(math.radians(tilt))
    
    # Calculate minimum shading clearance window based on the sun's trajectory
    minimum_shading_space = vertical_rise / math.tan(math.radians(winter_solstice_altitude))
    ideal_anti_shading_pitch = panel_ground_footprint + minimum_shading_space
    
    # Automatically handle geometric collisions if input pitch is invalid/overlapping
    min_physical_pitch = panel_ground_footprint + 0.15 # Minimum 15cm structural safety block
    is_shading_risk = False
    
    if pitch < min_physical_pitch:
        # Override to safe mathematical default if pitch physically clips structures
        pitch = round(ideal_anti_shading_pitch, 2)
        is_shading_risk = False
    elif pitch < ideal_anti_shading_pitch:
        is_shading_risk = True

    # Definitive ground separation window
    calculated_clear_space = pitch - panel_ground_footprint
    col_gap = 0.40  # Standardized maintenance walkway between module strings (columns)
    
    # Calculate comprehensive system outer plant bounds dynamically
    field_width = (cols * width) + ((cols - 1) * col_gap)
    field_depth = ((rows - 1) * pitch) + height

    # 2. RESPONSIVE PLOT CANVAS BUILD (Adapts safely to massive arrays vs small arrays)
    fig = plt.figure(figsize=(16, 8.5), facecolor="#ffffff")
    gs = fig.add_gridspec(1, 4, wspace=0.35)
    
    ax_main = fig.add_subplot(gs[0, 0:3])   # 2D CAD Plan View Map Grid
    ax_side = fig.add_subplot(gs[0, 3])     # Mechanical Side-Profile Elevation Map

    # 3. RENDER 2D PLAN MATRIX (TOP-DOWN VIEW)
    for r in range(rows):
        y_pos = r * pitch
        for c in range(cols):
            x_pos = c * (width + col_gap)
            
            # Create responsive collector block layout patch
            collector_block = patches.Rectangle(
                (x_pos, y_pos), width, height,
                linewidth=1.2, edgecolor='#1E3A8A', facecolor='#bae6fd', alpha=0.9, zorder=2
            )
            ax_main.add_patch(collector_block)
            
            # Add micro absorber pipe textures to visually denote solar engineering panels
            for step in range(1, 5):
                grid_x = x_pos + (step * width / 5)
                ax_main.plot([grid_x, grid_x], [y_pos, y_pos + height], 
                             color='#0284c7', linewidth=0.5, alpha=0.3, zorder=3)

    # 4. MARGIN DIMENSION LINES (Dynamically shift offset targets based on input scale)
    if cols > 1:
        line_y = field_depth + (field_depth * 0.05)
        ax_main.plot([width, width], [field_depth, line_y + (field_depth * 0.01)], color='#DC2626', linestyle=':', linewidth=1)
        ax_main.plot([width + col_gap, width + col_gap], [field_depth, line_y + (field_depth * 0.01)], color='#DC2626', linestyle=':', linewidth=1)
        ax_main.annotate('', xy=(width, line_y), xytext=(width + col_gap, line_y),
                         arrowprops=dict(arrowstyle='<->', color='#DC2626', linewidth=1.2))
        ax_main.text(width + (col_gap / 2), line_y + (field_depth * 0.005), f"{col_gap}m Gap", 
                     color='#DC2626', fontsize=9, ha='center', va='bottom', weight='bold')

    if rows > 1:
        left_offset = -(field_width * 0.08)
        ax_main.plot([0, left_offset - (field_width * 0.01)], [0, 0], color='#1E40AF', linestyle=':', linewidth=1)
        ax_main.plot([0, left_offset - (field_width * 0.01)], [pitch, pitch], color='#1E40AF', linestyle=':', linewidth=1)
        ax_main.annotate('', xy=(left_offset, 0), xytext=(left_offset, pitch),
                         arrowprops=dict(arrowstyle='<->', color='#1E40AF', linewidth=1.5))
        ax_main.text(left_offset - (field_width * 0.01), pitch / 2, f"Row Pitch\n= {pitch:.2f} m", 
                     color='#1E40AF', fontsize=10, ha='right', va='center', weight='bold')

        right_offset = field_width + (field_width * 0.08)
        ax_main.plot([field_width, right_offset + (field_width * 0.01)], [height, height], color='#16A34A', linestyle=':', linewidth=1)
        ax_main.plot([field_width, right_offset + (field_width * 0.01)], [pitch, pitch], color='#16A34A', linestyle=':', linewidth=1)
        ax_main.annotate('', xy=(right_offset, height), xytext=(right_offset, pitch),
                         arrowprops=dict(arrowstyle='<->', color='#16A34A', linewidth=1.5))
        
        status_label = "⚠️ Shading Risk" if is_shading_risk else "✓ Zero Shading"
        status_color = "#D97706" if is_shading_risk else "#15803D"
        ax_main.text(right_offset + (field_width * 0.01), (height + pitch) / 2, 
                     f"Clear Space: {calculated_clear_space:.2f} m\n{status_label}", 
                     color=status_color, fontsize=10, ha='left', va='center', weight='bold')

    # Adaptive canvas boundaries
    pad_x = max(field_width * 0.18, 2.0)
    pad_y = max(field_depth * 0.12, 1.5)
    ax_main.set_xlim(-pad_x, field_width + pad_x)
    ax_main.set_ylim(-pad_y, field_depth + pad_y)
    ax_main.set_aspect('equal')
    
    ax_main.set_title("SOLAR FIELD PLAN VIEW (RESPONSIVE CAD GRID)", color='#0F172A', fontsize=12, weight='bold', pad=15)
    ax_main.set_xlabel("Field Width Footprint (meters)", fontsize=10, color='#475569')
    ax_main.set_ylabel("Field Depth Flow Distance (meters)", fontsize=10, color='#475569')
    ax_main.grid(True, linestyle='--', alpha=0.2, color='#64748B')

    # 5. RENDER ELEVATION PROFILE
    ax_side.axhline(0, color='#334155', linewidth=3, zorder=1)
    
    angle_rad = math.radians(tilt)
    dx = height * math.cos(angle_rad)
    dy = height * math.sin(angle_rad)
    
    ax_side.plot([0, dx], [0, dy], color='#1E3A8A', linewidth=4, zorder=3, label='Collector Slant')
    ax_side.plot([dx, dx], [0, dy], color='#94A3B8', linestyle=':', linewidth=1)
    ax_side.plot([pitch, pitch + dx], [0, dy], color='#1E3A8A', linewidth=4, zorder=3)
    ax_side.plot([pitch + dx, pitch + dx], [0, dy], color='#94A3B8', linestyle=':', linewidth=1)

    solstice_rad = math.radians(winter_solstice_altitude)
    projected_ray_length = dy / math.tan(solstice_rad)
    ax_side.plot([dx, dx + projected_ray_length], [dy, 0], color='#EA580C', linestyle='--', linewidth=1.8, label='Solstice Sun Ray')
    
    shadow_zone = patches.Polygon([[dx, 0], [dx, dy], [dx + projected_ray_length, 0]], facecolor='#F8FAFC', alpha=0.8, zorder=2)
    ax_side.add_patch(shadow_zone)
    
    ax_side.annotate('', xy=(dx, -0.08), xytext=(pitch, -0.08),
                     arrowprops=dict(arrowstyle='<->', color='#16A34A', linewidth=1.2))
    ax_side.text((dx + pitch) / 2, -0.15, f"Clear space\n{calculated_clear_space:.2f}m", 
                 color='#15803D', fontsize=9, ha='center', va='top', weight='bold')

    ax_side.text(dx * 0.3, 0.05, f"{tilt}°", color='#1D4ED8', fontsize=9, weight='bold')

    ax_side.set_xlim(-0.5, max(pitch + dx + 0.8, dx + projected_ray_length + 0.5))
    ax_side.set_ylim(-0.4, dy + 0.6)
    ax_side.set_aspect('equal')
    ax_side.set_title("ELEVATION SHADOW MAP", color='#0F172A', fontsize=11, weight='bold', pad=15)
    ax_side.axis('off')
    ax_side.legend(loc='upper right', fontsize=8, framealpha=0.9)

    return fig

# --- DYNAMIC CUSTOMER DATA CALL ---
# 52 total units split across 4 rows = 13 columns.
# Standard industrial module size assumed: 1.2m width x 1.2m height.
# Row Pitch set exactly to customer specifications: 3.15 meters.
fig = draw_layout(rows=4, cols=13, width=1.2, height=1.2, pitch=3.15, tilt=30, latitude=23.5)
plt.show()
