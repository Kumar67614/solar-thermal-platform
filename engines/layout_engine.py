import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math

def spacing(
    height,
    tilt,
    latitude
):

    winter_altitude = (
        90 -
        abs(latitude+23.45)
    )

    s = (
        height *
        math.sin(
            math.radians(tilt)
        )
    ) / math.tan(
        math.radians(
            winter_altitude
        )
    )

    return s+0.5


def draw_layout(
    rows,
    cols,
    width,
    height,
    pitch
):

    fig, ax = plt.subplots(
        figsize=(14,8)
    )

    for r in range(rows):

        for c in range(cols):

            x = c*(width+0.3)

            y = r*pitch

            rect = patches.Rectangle(
                (x,y),
                width,
                height,
                linewidth=1,
                edgecolor='black',
                facecolor='skyblue'
            )

            ax.add_patch(rect)

    ax.set_xlim(0,cols*2)

    ax.set_ylim(0,rows*pitch+3)

    ax.set_aspect('equal')

    ax.set_title(
        "Solar Collector Field Layout"
    )

    return fig