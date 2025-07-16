from ui_functions import *
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque
import time
from concurrent.futures import ThreadPoolExecutor

# Performance constants
MAX_DATA_POINTS = 50  # Limit data history to save memory

# Thread pool for better performance
executor = ThreadPoolExecutor(max_workers=2)

selected_disk_idx = 0
window_bg = "#242424"

# Performance-optimized data storage using deque
cpu_data = deque(maxlen=MAX_DATA_POINTS)
ram_data = deque(maxlen=MAX_DATA_POINTS)
disk_data = deque(maxlen=MAX_DATA_POINTS)
network_data = deque(maxlen=MAX_DATA_POINTS)

# Update frequency optimization
_last_battery_update = 0
BATTERY_UPDATE_INTERVAL = 10.0  # Update battery every 10 seconds

def on_closing(root):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        exit(0)

def update_usage_labels(cpuLabel, ramLabel, diskLabel, networkLabel):
    def fetch_and_update():
        usage = get_usage()

        # cpu usage
        cpu_total_usage = sum(usage[0].values())
        cpu_average_usage = round(cpu_total_usage / len(usage[0]), 1)

        cpuLabel.after(0, lambda: cpuLabel.configure(text=f"CPU Usage = {cpu_average_usage}%"))

        # ram usage
        used_ram = usage[1]['used']
        ramLabel.after(0, lambda: ramLabel.configure(text=f"RAM Usage = {used_ram} MB"))

        # disk usage
        disk_usage = [usage[2][1]["readSpeed"], usage[2][1]["writeSpeed"]]
        diskLabel.after(0, lambda: diskLabel.configure(text=f"Disk Usage = {disk_usage[0]} MBps (Read), {disk_usage[1]} MBps (Write)"))

        # network usage
        network_usage = usage[3]
        networkLabel.after(0, lambda: networkLabel.configure(text=f"Network Usage = {network_usage['up']} Mbps (Up), {network_usage['down']} Mbps (Down)"))

    threading.Thread(target=fetch_and_update, daemon=True).start()

fig = None
axs = None
battery_fig = None
battery_ax = None
canvas = None
battery_canvas = None

def update_graph_theme(bg_color, text_color="white"):
    global fig, axs, battery_fig, battery_ax, canvas, battery_canvas
    # other graphs color
    if fig is not None:
        fig.patch.set_facecolor(bg_color)
        for i, ax in enumerate(axs.flat):
            ax.set_facecolor(bg_color)
            ax.tick_params(colors=text_color)
            ax.yaxis.label.set_color(text_color)
            ax.xaxis.label.set_color(text_color)
            if i == 2:
                ax.set_title(ax.get_title(), color=text_color)
            else:
                ax.title.set_color(text_color)
        if canvas is not None:
            canvas.draw()
    # battery color
    if battery_fig is not None:
        battery_fig.patch.set_facecolor(bg_color)
        if battery_ax is not None:
            battery_ax.set_facecolor(bg_color)
            for text in battery_ax.texts:
                text.set_color(text_color)
        if battery_canvas is not None:
            battery_canvas.draw()

def build_main_ui():
    import os
    import sys
    from PIL import Image, ImageTk

    root = CTk()
    root.geometry("1000x1000")
    root.title("WinStatz")
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))
    root.resizable(False, False)

    # Set app icon
    script_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(script_dir, "..", "assets", "icon.png")
    if os.path.exists(icon_path):
        try:
            if sys.platform.startswith("win"):
                ico_path = os.path.join(script_dir, "..", "assets", "icon.ico")
                if os.path.exists(ico_path):
                    root.iconbitmap(ico_path)
                else:
                    img = Image.open(icon_path)
                    icon_img = ImageTk.PhotoImage(img)
                    root.iconphoto(True, icon_img)
            else:
                img = Image.open(icon_path)
                icon_img = ImageTk.PhotoImage(img)
                root.iconphoto(True, icon_img)
        except Exception as e:
            print(f"Could not set app icon: {e}")

    # title label
    titleLabel = CTkLabel(root, text="WinStatz", font=("Poppins", 48, "bold"))
    titleLabel.place(relx=0.5, rely=0.05, anchor="center")

    # settings button
    settingsButton = CTkButton(root, text="⚙️", command=lambda: open_settings(root), width=40, height=40)
    settingsButton.place(relx=0.02, rely=0.02, anchor="nw")

    # 3 dots
    threeDotsButton = CTkButton(root, text="⋮", command=open_3_dots_details, width=40, height=40, bg_color="transparent", fg_color="transparent", hover_color="gray")
    threeDotsButton.place(relx=0.95, rely=0.02, anchor="ne")

    # style
    plt.style.use('dark_background')
    global fig, axs
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    fig.patch.set_facecolor(window_bg)
    plt.tight_layout(pad=6.0)

    # create the graphs
    axs[0,0].set_title("CPU Usage (%)", color='white')
    axs[0,1].set_title("RAM Usage (MB)", color='white')
    axs[1,0].set_title("Disk Usage (MBps)", color='white')
    axs[1,1].set_title("Network Usage (Mbps)", color='white')

    for ax in axs.flat:
        ax.set_facecolor(window_bg)
        ax.tick_params(colors='white')
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')

    cpu_bar = axs[0,0].bar(["Avg"], [0], color="#3498db")
    ram_bar = axs[0,1].bar(["Used", "Free"], [0,0], color=["#27ae60", "#7f8c8d"])
    disk_bar = axs[1,0].bar(["Read", "Write"], [0,0], color=["#9b59b6", "#e67e22"])
    net_bar = axs[1,1].bar(["Up", "Down"], [0,0], color=["#e74c3c", "#1abc9c"])

    import matplotlib.patches as mpatches
    global battery_fig, battery_ax
    battery_fig, battery_ax = plt.subplots(figsize=(4, 2))
    battery_fig.patch.set_facecolor(window_bg)
    battery_ax.set_facecolor(window_bg)
    battery_ax.axis('off')
    battery_icon = mpatches.FancyBboxPatch((0.2, 0.4), 0.6, 0.2,
        boxstyle="round,pad=0.05", ec="black", fc="#27ae60", mutation_aspect=2)
    battery_ax.add_patch(battery_icon)
    battery_tip = mpatches.FancyBboxPatch((0.82, 0.48), 0.08, 0.04,
        boxstyle="round,pad=0.05", ec="black", fc="#27ae60", mutation_aspect=2)
    battery_ax.add_patch(battery_tip)
    battery_ax.set_xlim(0, 1)
    battery_ax.set_ylim(0, 1)
    battery_ax.text(0.5, 0.5, "Battery", color='white', fontsize=14, ha='center', va='center')

    global canvas, battery_canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center")
    battery_canvas = FigureCanvasTkAgg(battery_fig, master=root)
    battery_canvas.get_tk_widget().place(relx=0.5, rely=0.95, anchor="center")

    # update the bar graphs
    def update_bars_threaded():
        def fetch_and_update():
            try:
                usage = get_usage()
                if not usage:
                    return
            except Exception as e:
                print(f"Error getting usage data: {e}")
                return
                
            def update_plot():
                global _last_battery_update
                current_time = time.time()
                
                try:
                    # Always update CPU, RAM, disk, network (basic stats)
                    # CPU
                    if usage[0] and len(usage[0]) > 0:
                        cpu_total_usage = sum(usage[0].values())
                        cpu_average_usage = round(cpu_total_usage / len(usage[0]), 1)
                        cpu_data.append(cpu_average_usage)
                    else:
                        cpu_average_usage = 0
                        cpu_data.append(0)
                    cpu_bar[0].set_height(cpu_average_usage)
                    axs[0,0].set_ylim(0, 100)

                    # RAM
                    if usage[1]:
                        used_ram = usage[1].get('used', 0)
                        free_ram = usage[1].get('free', 0)
                        total_ram = usage[1].get('total', used_ram + free_ram)
                        ram_data.append(used_ram)
                        ram_bar[0].set_height(used_ram)
                        ram_bar[1].set_height(free_ram)
                        axs[0,1].set_ylim(0, total_ram)
                    else:
                        ram_data.append(0)
                        ram_bar[0].set_height(0)
                        ram_bar[1].set_height(0)
                        axs[0,1].set_ylim(0, 100)

                    # Disk
                    disk_title = f"Disk {selected_disk_idx + 1} Usage (MBps)"
                    axs[1,0].set_title(disk_title)  # Only update the text, not the color
                    if usage[2] and len(usage[2]) > 0:
                        disk = usage[2][selected_disk_idx % len(usage[2])]
                        disk_read = disk.get("readSpeed", 0)
                        disk_write = disk.get("writeSpeed", 0)
                        disk_data.append(disk_read + disk_write)
                    else:
                        disk_read = 0
                        disk_write = 0
                        disk_data.append(0)
                    disk_bar[0].set_height(disk_read)
                    disk_bar[1].set_height(disk_write)
                    axs[1,0].set_ylim(0, max(100, disk_read, disk_write))

                    # Network
                    net_up = usage[3].get("up", 0) if usage[3] else 0
                    net_down = usage[3].get("down", 0) if usage[3] else 0
                    network_data.append(net_up + net_down)
                    net_bar[0].set_height(net_up)
                    net_bar[1].set_height(net_down)
                    axs[1,1].set_ylim(0, max(100, net_up, net_down))

                    # Battery - update less frequently
                    if current_time - _last_battery_update > BATTERY_UPDATE_INTERVAL:
                        battery_percent = usage[4].get("percent", 0) if usage[4] else 0
                        battery_icon.set_width(0.6 * (battery_percent / 100))
                        if battery_percent > 20:
                            battery_icon.set_facecolor("#27ae60")  # green
                        else:
                            battery_icon.set_facecolor("#e74c3c")  # red for low battery
                        battery_canvas.draw()
                        _last_battery_update = current_time

                    # Single canvas draw for all main plots
                    canvas.draw()
                except Exception as e:
                    print(f"Error updating plots: {e}")
            root.after(0, update_plot)
            root.after(1000, update_bars_threaded)
        # Use thread pool instead of creating new threads
        executor.submit(fetch_and_update)

    def show_disk(idx):
        global selected_disk_idx
        try:
            selected_disk_idx = idx
            update_bars_threaded()
        except Exception as e:
            print(f"Error showing disk {idx}: {e}")

    def next_disk():
        global selected_disk_idx
        try:
            usage = get_usage()
            if usage and usage[2] and len(usage[2]) > 0:
                selected_disk_idx = (selected_disk_idx + 1) % len(usage[2])
            update_bars_threaded()
        except Exception as e:
            print(f"Error switching to next disk: {e}")

    def prev_disk():
        global selected_disk_idx
        try:
            usage = get_usage()
            if usage and usage[2] and len(usage[2]) > 0:
                selected_disk_idx = (selected_disk_idx - 1) % len(usage[2])
            update_bars_threaded()
        except Exception as e:
            print(f"Error switching to previous disk: {e}")

    # buttons for going to next disk and previous disk
    nextDiskBtn = CTkButton(root, text="Next Disk", command=next_disk)
    nextDiskBtn.place(relx=0.3, rely=0.83)
    prevDiskBtn = CTkButton(root, text="Prev Disk", command=prev_disk)
    prevDiskBtn.place(relx=0.12, rely=0.83)

    update_bars_threaded()
    root.mainloop()