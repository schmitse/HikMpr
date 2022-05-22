import tkinter as tk
import matplotlib.pyplot as plt
import contextily as ctx
#import pyproj
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from functools import partial


def show_map(root):

    name = entry_location.get()
    zoom = int(entry_zoom_val.get())
    fig.dpi = int(entry_dpi_val.get())

    print('Loading Map..')
    place_big = ctx.Place(name, source=ctx.providers.OpenTopoMap, zoom=zoom, zoom_adjust=8)
    print('..Loaded Map!')

    ax.clear()
    ax.axis('off')
    
    place_big.plot(ax)
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    ax.clear()

    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    print(f'Limits for detailed Map: {xlim}, {ylim}')
    print('Loading Detailed Map..')
    ctx.add_basemap(ax, source=ctx.providers.OpenTopoMap, zoom=zoom+10, crs='epsg:3857')
    print('..Loaded Detailed Map!')

    widget = canvas_figure.get_tk_widget().pack(side='top', fill=tk.BOTH, expand=1)

    return None


def move_up(): 
    print('Moving Up')
    zoom = int(entry_zoom_val.get())
    ylim = ax.get_ylim()
    dy = (ylim[1]-ylim[0])*0.05
    ax.set_ylim(ylim[0]+dy, ylim[1]+dy)
    ctx.add_basemap(ax, source=ctx.providers.OpenTopoMap, zoom=zoom+10, crs='epsg:3857')


def move_down(): 
    print('Moving Down')
    zoom = int(entry_zoom_val.get())
    ylim = ax.get_ylim()
    dy = (ylim[1]-ylim[0])*0.05
    ax.set_ylim(ylim[0]-dy, ylim[1]-dy)
    ctx.add_basemap(ax, source=ctx.providers.OpenTopoMap, zoom=zoom+10, crs='epsg:3857')


def move_right(): 
    print('Moving Right')
    zoom = int(entry_zoom_val.get())
    xlim = ax.get_xlim()
    dx = (xlim[1]-xlim[0])*0.05
    ax.set_xlim(xlim[0]+dx, xlim[1]+dx)
    ctx.add_basemap(ax, source=ctx.providers.OpenTopoMap, zoom=zoom+10, crs='epsg:3857')


def move_left(): 
    print('Moving Left')
    zoom = int(entry_zoom_val.get())
    xlim = ax.get_xlim()
    dx = (xlim[1]-xlim[0])*0.05
    ax.set_xlim(xlim[0]-dx, xlim[1]-dx)
    ctx.add_basemap(ax, source=ctx.providers.OpenTopoMap, zoom=zoom+10, crs='epsg:3857')


def zoom_in():
    print('Zooming In')
    zoom = int(entry_zoom_val.get())
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    dx = (xlim[1]-xlim[0])*0.05
    dy = (ylim[1]-ylim[0])*0.05
    ax.set_xlim(xlim[0]+dx, xlim[1]-dx)
    ax.set_ylim(ylim[0]+dy, ylim[1]-dy)
    ctx.add_basemap(ax, source=ctx.providers.OpenTopoMap, zoom=zoom+10, crs='epsg:3857')


def zoom_out():
    print('Zooming Out')
    zoom = int(entry_zoom_val.get())
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    dx = (xlim[1]-xlim[0])*0.05
    dy = (ylim[1]-ylim[0])*0.05
    ax.set_xlim(xlim[0]-dx, xlim[1]+dx)
    ax.set_ylim(ylim[0]-dy, ylim[1]+dy)
    ctx.add_basemap(ax, source=ctx.providers.OpenTopoMap, zoom=zoom+10, crs='epsg:3857')


def close_map(root):
    plt.close()
    #fig.clear()
    ax.clear()
    canvas_figure.draw()
    return None


def draw_line(event):
    print(f'ButtonPress: {event.type} at coords: {event.x, event.y}')
    if str(event.type)=='4':
        canvas.old_coords = event.x, event.y
    elif str(event.type)=='5':
        x, y = event.x, event.y
        x1, y1, = canvas.old_coords
        canvas.create_line(x, y, x1, y1)


def main():

    window = tk.Tk()
    window.title('HikMpr')
    window.geometry('1500x1000')

    global fig, ax, canvas_figure
    fig, ax = plt.subplots(figsize=(20,20))
    canvas_figure = FigureCanvasTkAgg(fig, window)
    canvas_figure.draw_idle()

    global canvas, canvas_window
    canvas = tk.Canvas(window, width=1400, height=100, relief='raised')
    canvas_window = tk.Canvas(window, width=1400, height=800, relief='raised')
    canvas.pack()
    #canvas_window.pack()

    hikmpr_label = tk.Label(window, text='HikMpr - Explore the World')
    hikmpr_label.config(font=('Times New Roman', 22))
    canvas.create_window(700, 20, window=hikmpr_label)

    location_label = tk.Label(window, text='Your Location: ')
    location_label.config(font=('Times New Roman', 18))
    canvas.create_window(200, 75, window=location_label)

    global entry_location
    entry_location = tk.Entry(window)
    entry_location.config(font=('Times New Roman', 18))
    canvas.create_window(400, 75, window=entry_location)

    global entry_zoom, entry_zoom_val
    zoom_levels = ['0', '1', '2', '3', '4', '5']
    entry_zoom_val = tk.StringVar(window)
    entry_zoom_val.set('3')
    entry_zoom = tk.OptionMenu(window, entry_zoom_val, *zoom_levels)
    entry_zoom.config(width=5, font=('Times New Roman', 18))
    canvas.create_window(600, 75, window=entry_zoom)

    global entry_dpi, entry_dpi_val
    dpi_levels = ['50', '75', '100', '150', '200', '500']
    entry_dpi_val = tk.StringVar(window)
    entry_dpi_val.set('100')
    entry_dpi = tk.OptionMenu(window, entry_dpi_val, *dpi_levels)
    entry_dpi.config(width=5, font=('Times New Roman', 18))
    canvas.create_window(800, 75, window=entry_dpi)

    args = {'root': window}

    plot_button = tk.Button(master=window, command=partial(show_map,**args), height=1, width=10, text='Display Map')
    plot_button.config(font=('Times New Roman', 18))
    canvas.create_window(1000, 75, window=plot_button)

    zoom_in_button = tk.Button(master=window, command=zoom_in, height=1, width=1, text='+')
    zoom_out_button = tk.Button(master=window, command=zoom_out, height=1, width=1, text='-')
    up_button = tk.Button(master=window, command=move_up, height=1, width=1, text='^')
    down_button = tk.Button(master=window, command=move_down, height=1, width=1, text='v')
    left_button = tk.Button(master=window, command=move_left, height=1, width=1, text='<')
    right_button = tk.Button(master=window, command=move_right, height=1, width=1, text='>')

    zoom_in_button.config(font=('Times New Roman', 18))
    zoom_out_button.config(font=('Times New Roman', 18))
    up_button.config(font=('Times New Roman', 18))
    down_button.config(font=('Times New Roman', 18))
    left_button.config(font=('Times New Roman', 18))
    right_button.config(font=('Times New Roman', 18))

    canvas.create_window(1130, 75, window=zoom_in_button)
    canvas.create_window(1110, 75, window=zoom_out_button)
    canvas.create_window(1150, 75, window=up_button)
    canvas.create_window(1170, 75, window=down_button)
    canvas.create_window(1190, 75, window=left_button)
    canvas.create_window(1210, 75, window=right_button)

    window.bind('<ButtonPress-1>', draw_line)
    window.bind('<ButtonRelease-1>', draw_line)

    #remove_button = tk.Button(master=window, command=partial(close_map,**args), height=1, width=10, text='Close Map')
    #remove_button.config(font=('Times New Roman', 18))
    #canvas.create_window(1150, 75, window=remove_button)

    destroy_button = tk.Button(master=window, command=window.quit, height=1, width=7, text='Quit')
    destroy_button.config(font=('Times New Roman', 18))
    canvas.create_window(1350, 75, window=destroy_button)

    window.mainloop()

    return None

if __name__ == '__main__':
    plt.rcParams['figure.dpi'] = 100
    main()