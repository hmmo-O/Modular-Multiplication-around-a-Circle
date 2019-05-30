import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

is_manual = False # True if user has taken control of the animation
interval = 50 # ms, time between animation frames
loop_len = 0.1 # seconds per loop
scale = interval / 1000 / loop_len

#Defining Modular Multiplier and Plotting system
def ModMul(nums, mul):
    for a in range(nums):
        coord = (a*2*np.pi/nums, mul*a*2*np.pi/nums)
        subPlt.plot(np.sin(coord), np.cos(coord), 'b')

    t = np.arange(0, 2*np.pi, 2*np.pi/nums)
    x= np.sin(t)
    y= np.cos(t)
    subPlt.plot(x, y, 'b.')
    subPlt.axes.get_xaxis().set_visible(False)
    subPlt.axes.get_yaxis().set_visible(False)

#Updating the plot w.r.t change in value of slider
def update(val):
    subPlt.cla()
    nums = int(round(s_num.val))
    mul = s_mul.val

    ModMul(nums, mul)

#Updating manual control if a mouse click happens on the slider
def update_slider(val):
    global is_manual
    is_manual = True
    update(val)

#Continuously updating the plot when auto
def update_plot(num):
    global is_manual
    if is_manual == True:
        return
        
    val = (s_num.val + scale) % s_num.valmax
    s_num.set_val(val)
    is_manual = False
    return

#Defining a click event happening on the Number slider    
def on_click(event):
     # Check where the click happened
    (nxm, nym),(nxM, nyM) = s_num.label.clipbox.get_points()
    if nxm < event.x < nxM and nym < event.y < nyM:
        return
    else:
        global is_manual
        is_manual = False

### Main Loop ###
root = tk.Tk()
root.title("Test")

fig = plt.Figure()
canvas = FigureCanvasTkAgg(fig, root)
canvas.show()
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

subPlt = fig.add_subplot(111)
fig.subplots_adjust(bottom=0.25)

num_loc = fig.add_axes([0.12, 0.1, 0.78, 0.03])
mul_loc = fig.add_axes([0.12, 0.05, 0.70, 0.03])

s_num = Slider(num_loc, 'Points', 1, 100, valinit = 1, valfmt = '%0.0f')
s_mul = Slider(mul_loc, 'Multiplier', 1, 100, valinit = 1)

s_num.on_changed(update_slider)
s_mul.on_changed(update_slider)

fig.canvas.mpl_connect('button_press_event', on_click)

ani = animation.FuncAnimation(fig, update_plot, interval=interval)

root.mainloop()