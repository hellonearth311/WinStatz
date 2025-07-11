from ui_functions import *
import threading

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
    root.geometry("600x600")
    root.title("WinStatz")

    # app design
    # title at top
    # cpu graph, ram graph
    # disk graph, network graph
    # battery icon on top right, hover over to reveal more info
    # settings button in top left
    # settings menu - color theme, dark/light mode
    # specs of each thing are shown near the graph, for more detailed specs press 3 dots icon


    # title label
    titleLabel = CTkLabel(root, text="WinStatz", font=("Poppins", 48, "bold"))
    titleLabel.place(relx=0.5, rely=0.05, anchor="center")

    # settings button
    settingsButton = CTkButton(root, text="⚙️", command=lambda: open_settings(root), width=40, height=40)
    settingsButton.place(relx=0.02, rely=0.02, anchor="nw")

    # 3 dots
    threeDotsButton = CTkButton(root, text="⋮", command=open_3_dots_details, width=40, height=40, bg_color="transparent", fg_color="transparent", hover_color="gray")
    threeDotsButton.place(relx=0.95, rely=0.02, anchor="ne")


    # cpu usage info
    cpuLabel = CTkLabel(root, text=f"CPU Usage = ", font=("Poppins", 20))
    cpuLabel.place(relx=0.5, rely=0.15, anchor="center")

    # ram usage info
    ramLabel = CTkLabel(root, text=f"RAM Usage = ", font=("Poppins", 20))
    ramLabel.place(relx=0.5, rely=0.25, anchor="center")   

    # disk usage info
    diskLabel = CTkLabel(root, text=f"Disk Usage = ", font=("Poppins", 20))
    diskLabel.place(relx=0.5, rely=0.35, anchor="center")

    # network usage info
    networkLabel = CTkLabel(root, text=f"Network Usage = ", font=("Poppins", 20))
    networkLabel.place(relx=0.5, rely=0.45, anchor="center")

    def periodic_update():
        update_usage_labels(cpuLabel, ramLabel, diskLabel, networkLabel)
        root.after(1000, periodic_update)

    periodic_update()
    root.mainloop()