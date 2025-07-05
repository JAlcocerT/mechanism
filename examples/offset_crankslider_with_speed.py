# Performs an analysis on an offset crank slider and displays the slider speed on the animation
from mechanism import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define joints first
O, A = get_joints('O A')
P = Joint(name='P', exclude=True)
B = Joint(name='B', follow=True)

# Define vectors
a = Vector((O, A), r=6)
b = Vector((A, B), r=10)
c = Vector((P, B), r=3, theta=np.pi/2, style='ground')
d = Vector((O, P), theta=0, style='ground')

# Define the loop equation(s)
def loop(x, inp):
    return a(inp) + b(x[0]) - c() - d(x[1])

# --- Animation settings for YouTube Short (9:16, 13 seconds) ---
desired_duration_sec = 13
fps = 30
num_frames = desired_duration_sec * fps
# You may adjust the time range (here, 0 to 0.1 min) as needed for your mechanism
# This keeps the same simulation range but at higher frame density
# If you want to slow down or speed up the simulation, adjust the 0.1 value
# For now, we'll keep it as in the original

t = np.linspace(0, 0.1, num_frames)  # time
th2 = 20*np.pi*t
w2 = np.full(th2.size, 20*np.pi)
a2 = np.zeros(th2.size)
pos_guess = np.array([np.pi/4, 10])
vel_guess = np.array([10, 10])
acc_guess = np.array([10, 10])

# Define the mechanism
mechanism = Mechanism(vectors=[a, b, c, d], origin=O, loops=loop, pos=th2, vel=w2, acc=a2,
                      guess=(pos_guess, vel_guess, acc_guess))
mechanism.iterate()

# Get the animation, figure, and axes objects
ani, fig, ax = mechanism.get_animation(velocity=True, acceleration=True, scale=0.2)
fig.set_size_inches(5, 8.88)  # 9:16 aspect ratio for YouTube Shorts
ax.set_title('Offset Crank Slider with Speed Display')

# --- Unit conversions ---
INCHES_TO_METERS = 0.0254
MINUTES_TO_SECONDS = 1/60
CONVERSION = INCHES_TO_METERS * MINUTES_TO_SECONDS  # inches/min to m/s

# Convert slider speed to m/s
slider_speed_mps = d.vel.r_dots * CONVERSION  # array

# Crank speed: v = r * omega (omega in rad/min, r in inches)
crank_radius = 6  # inches (constant crank length)
crank_omega = w2    # in rad/min (array)
crank_speed_mps = crank_radius * crank_omega * CONVERSION  # array

# Add a text annotation for both speeds (top right)
speed_text = ax.text(0.98, 0.98, '', transform=ax.transAxes,
                     ha='right', va='top', fontsize=12,
                     bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

# Patch FuncAnimation to update speed text dynamically
orig_func = ani._func if hasattr(ani, '_func') else None

# Try to get the underlying matplotlib FuncAnimation object
if hasattr(ani, '_draw_next_frame'):
    orig_draw_next_frame = ani._draw_next_frame
    def _draw_next_frame(frame, blit):
        # Update speed text with both values in m/s
        if frame < len(slider_speed_mps):
            speed_text.set_text(
                f"Slider speed: {slider_speed_mps[frame]:.3f} m/s\nCrank speed: {crank_speed_mps[frame]:.3f} m/s"
            )
        else:
            speed_text.set_text("")
        return orig_draw_next_frame(frame, blit)
    ani._draw_next_frame = _draw_next_frame

# Save animation with speed overlay
i = ani.save('./animations/offset_crankslider_with_speed-YTShort.gif', writer='pillow', fps=fps)

plt.show()
