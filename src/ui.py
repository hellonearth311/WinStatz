from ui_functions import *
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

selected_disk_idx = 0

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

def build_main_ui():
    root = CTk()
    root.geometry("1100x1100")
    root.title("WinStatz")
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    # app design
    # title at top
    # cpu graph, ram graph
    # disk graph, network graph
    # battery icon on top right, hover over to reveal more info
    # settings button in top left
    # settings menu - color theme, dark/light mode


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
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    plt.tight_layout(pad=6.0)

    # create the graphs
    axs[0,0].set_title("CPU Usage (%)", color='white')
    axs[0,1].set_title("RAM Usage (MB)", color='white')
    axs[1,0].set_title("Disk Usage (MBps)", color='white')
    axs[1,1].set_title("Network Usage (Mbps)", color='white')

    for ax in axs.flat:
        ax.set_facecolor('#222222')
        ax.tick_params(colors='white')
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')

    cpu_bar = axs[0,0].bar(["Avg"], [0], color="#3498db")
    ram_bar = axs[0,1].bar(["Used", "Free"], [0,0], color=["#27ae60", "#7f8c8d"])
    disk_bar = axs[1,0].bar(["Read", "Write"], [0,0], color=["#9b59b6", "#e67e22"])
    net_bar = axs[1,1].bar(["Up", "Down"], [0,0], color=["#e74c3c", "#1abc9c"])

    import matplotlib.patches as mpatches
    battery_fig, battery_ax = plt.subplots(figsize=(4, 2))
    battery_ax.set_facecolor('#222222')
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

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().place(relx=0.5, rely=0.45, anchor="center")
    battery_canvas = FigureCanvasTkAgg(battery_fig, master=root)
    battery_canvas.get_tk_widget().place(relx=0.5, rely=0.85, anchor="center")

    # update the bar graphs
    def update_bars_threaded():
        def fetch_and_update():
            usage = get_usage()
            def update_plot():
                # CPU
                cpu_total_usage = sum(usage[0].values())
                cpu_average_usage = round(cpu_total_usage / len(usage[0]), 1)
                cpu_bar[0].set_height(cpu_average_usage)
                axs[0,0].set_ylim(0, 100)

                # RAM
                used_ram = usage[1]['used']
                free_ram = usage[1]['free']
                ram_bar[0].set_height(used_ram)
                ram_bar[1].set_height(free_ram)
                axs[0,1].set_ylim(0, usage[1]['total'])

                # Disk
                disk_title = f"Disk {selected_disk_idx + 1} Usage (MBps)"
                axs[1,0].set_title(disk_title, color='white')
                if usage[2] and len(usage[2]) > 0:
                    disk = usage[2][selected_disk_idx % len(usage[2])]
                    disk_read = disk["readSpeed"]
                    disk_write = disk["writeSpeed"]
                else:
                    disk_read = 0
                    disk_write = 0
                disk_bar[0].set_height(disk_read)
                disk_bar[1].set_height(disk_write)
                axs[1,0].set_ylim(0, max(100, disk_read, disk_write))

                # Network
                net_up = usage[3]["up"] if usage[3] else 0
                net_down = usage[3]["down"] if usage[3] else 0
                net_bar[0].set_height(net_up)
                net_bar[1].set_height(net_down)
                axs[1,1].set_ylim(0, max(100, net_up, net_down))

                # Battery
                battery_percent = usage[4]["percent"] if usage[4] and "percent" in usage[4] else 0
                battery_icon.set_width(0.6 * (battery_percent / 100))
                if battery_percent > 20:
                    battery_icon.set_facecolor("#27ae60")  # green
                else:
                    battery_icon.set_facecolor("#e74c3c")  # red for low battery
                battery_canvas.draw()

                canvas.draw()
            root.after(0, update_plot)
            root.after(1000, update_bars_threaded)
        threading.Thread(target=fetch_and_update, daemon=True).start()

    def show_disk(idx):
        global selected_disk_idx
        selected_disk_idx = idx
        update_bars_threaded()

    def next_disk():
        global selected_disk_idx
        usage = get_usage()
        if usage[2] and len(usage[2]) > 0:
            selected_disk_idx = (selected_disk_idx + 1) % len(usage[2])
        update_bars_threaded()

    def prev_disk():
        global selected_disk_idx
        usage = get_usage()
        if usage[2] and len(usage[2]) > 0:
            selected_disk_idx = (selected_disk_idx - 1) % len(usage[2])
        update_bars_threaded()

    # buttons for going to next disk and previous disk
    nextDiskBtn = CTkButton(root, text="Next Disk", command=next_disk)
    nextDiskBtn.place(relx=0.33, rely=0.75)
    prevDiskBtn = CTkButton(root, text="Prev Disk", command=prev_disk)
    prevDiskBtn.place(relx=0.15, rely=0.75)

    update_bars_threaded()
    root.mainloop()

    # style
    plt.style.use('dark_background')
    fig, axs = plt.subplots(2, 2, figsize=(10, 8))
    plt.tight_layout(pad=6.0)

    # create the graphs
    axs[0,0].set_title("CPU Usage (%)", color='white')
    axs[0,1].set_title("RAM Usage (MB)", color='white')
    axs[1,0].set_title(f"Disk {selected_disk_idx + 1} Usage (MBps)", color='white')
    axs[1,1].set_title("Network Usage (Mbps)", color='white')

    for ax in axs.flat:
        ax.set_facecolor('#222222')
        ax.tick_params(colors='white')
        ax.yaxis.label.set_color('white')
        ax.xaxis.label.set_color('white')

    cpu_bar = axs[0,0].bar(["Avg"], [0], color="#3498db")
    ram_bar = axs[0,1].bar(["Used", "Free"], [0,0], color=["#27ae60", "#7f8c8d"])
    disk_bar = axs[1,0].bar(["Read", "Write"], [0,0], color=["#9b59b6", "#e67e22"])
    net_bar = axs[1,1].bar(["Up", "Down"], [0,0], color=["#e74c3c", "#1abc9c"])

    import matplotlib.patches as mpatches
    battery_fig, battery_ax = plt.subplots(figsize=(4, 2))
    battery_ax.set_facecolor('#222222')
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

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.get_tk_widget().place(relx=0.5, rely=0.45, anchor="center")
    battery_canvas = FigureCanvasTkAgg(battery_fig, master=root)
    battery_canvas.get_tk_widget().place(relx=0.5, rely=0.85, anchor="center")

    # update the bar graphs
    def update_bars_threaded():
        def fetch_and_update():
            usage = get_usage()
            def update_plot():
                # CPU
                cpu_total_usage = sum(usage[0].values())
                cpu_average_usage = round(cpu_total_usage / len(usage[0]), 1)
                cpu_bar[0].set_height(cpu_average_usage)
                axs[0,0].set_ylim(0, 100)

                # RAM
                used_ram = usage[1]['used']
                free_ram = usage[1]['free']
                ram_bar[0].set_height(used_ram)
                ram_bar[1].set_height(free_ram)
                axs[0,1].set_ylim(0, usage[1]['total'])

                # Disk
                if usage[2] and len(usage[2]) > 0:
                    disk = usage[2][selected_disk_idx % len(usage[2])]
                    disk_read = disk["readSpeed"]
                    disk_write = disk["writeSpeed"]
                else:
                    disk_read = 0
                    disk_write = 0
                disk_bar[0].set_height(disk_read)
                disk_bar[1].set_height(disk_write)
                axs[1,0].set_ylim(0, max(100, disk_read, disk_write))

                # Network
                net_up = usage[3]["up"] if usage[3] else 0
                net_down = usage[3]["down"] if usage[3] else 0
                net_bar[0].set_height(net_up)
                net_bar[1].set_height(net_down)
                axs[1,1].set_ylim(0, max(100, net_up, net_down))

                # Battery
                battery_percent = usage[4]["percent"] if usage[4] and "percent" in usage[4] else 0
                battery_icon.set_width(0.6 * (battery_percent / 100))
                if battery_percent > 20:
                    battery_icon.set_facecolor("#27ae60")  # green
                else:
                    battery_icon.set_facecolor("#e74c3c")  # red for low battery
                battery_canvas.draw()

                canvas.draw()
            root.after(0, update_plot)
            root.after(1000, update_bars_threaded)
        threading.Thread(target=fetch_and_update, daemon=True).start()
        
    def next_disk():
        global selected_disk_idx
        usage = get_usage()
        if usage[2] and len(usage[2]) > 0:
            selected_disk_idx = (selected_disk_idx + 1) % len(usage[2])
        update_bars_threaded()

    def prev_disk():
        global selected_disk_idx
        usage = get_usage()
        if usage[2] and len(usage[2]) > 0:
            selected_disk_idx = (selected_disk_idx - 1) % len(usage[2])
        update_bars_threaded()

    update_bars_threaded()
    root.mainloop()