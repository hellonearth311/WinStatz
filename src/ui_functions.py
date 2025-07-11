from customtkinter import *
from tkinter import messagebox
from stats import *

def open_settings(root):
    # settings window
    settings_window = CTkToplevel()

    # window config
    settings_window.title("Settings")
    settings_window.geometry("400x300")

    settings_window.grab_set()
    settings_window.resizable(False, False)

    # dark/light mode option
    darkLightModeLabel = CTkLabel(settings_window, text="Dark/Light Mode:")
    darkLightModeLabel.place(relx=0.1, rely=0.1, anchor="w")

    darkLightModeOption = CTkOptionMenu(settings_window, values=["Dark", "Light"], command=lambda x: my_set_appearance_mode(x))
    darkLightModeOption.place(relx=0.5, rely=0.1, anchor="w")

    # color theme option
    colorThemeLabel = CTkLabel(settings_window, text="Color Theme:")
    colorThemeLabel.place(relx=0.1, rely=0.2, anchor="w")

    colorThemeOption = CTkOptionMenu(settings_window, values=["Blue", "Green"], command=lambda x: set_color_theme(x.lower(), root))
    colorThemeOption.place(relx=0.5, rely=0.2, anchor="w")

def set_color_theme(theme, root):
    from ui import build_main_ui
    
    # ask the user to confirm the app restart
    confirm = messagebox.askyesno("Change Theme", f"Do you want to change the theme to {theme.capitalize()}? The app will restart.")

    if confirm:
        root.destroy()
        set_default_color_theme(theme)
        build_main_ui()
    else:
        messagebox.showinfo("Change Theme", "Theme change cancelled.")

def my_set_appearance_mode(mode):
    """
    Set the appearance mode of the app.
    :param mode: "Dark" or "Light"
    """
    from ui import update_graph_theme
    if mode == "Dark":
        set_appearance_mode("dark")
        update_graph_theme("#242424", "white")
    elif mode == "Light":
        set_appearance_mode("light")
        update_graph_theme("#ebebeb", "black")
    else:
        messagebox.showerror("Error", "Invalid appearance mode selected.")

def open_3_dots_details():
    # open the window
    three_dots_details = CTkToplevel()

    # details window config
    three_dots_details.title("Advanced Specifications")
    three_dots_details.geometry("1200x500")

    three_dots_details.grab_set()
    three_dots_details.resizable(False, False)

    # title
    title_label = CTkLabel(three_dots_details, text="Advanced Specifications", font=("Poppins", 30, "bold"))
    title_label.place(relx=0.5, rely=0.1, anchor="center")

    # some specs and information
    specs_list = get_specs()

    # cpu
    cpu_title = CTkLabel(three_dots_details, text="CPU Specifications", font=("Poppins", 20, "bold"))
    cpu_title.place(relx=0.15, rely=0.22, anchor="center")
    cpu_text = f"CPU Name: {specs_list[0]['name']}\n" \
                f"Manufacturer: {specs_list[0]['manufacturer']}\n" \
                f"Description: {specs_list[0]['description']}\n" \
                f"Cores: {specs_list[0]['coreCount']}\n" \
                f"Clock Speed: {specs_list[0]['clockSpeed']} MHz"
    cpu_label = CTkLabel(three_dots_details, text=cpu_text, font=("Poppins", 12))
    cpu_label.place(relx=0.15, rely=0.35, anchor="center")

    # gpu
    gpu_index = [0]
    gpu_list = specs_list[1]

    def update_gpu_label():
        gpu = gpu_list[gpu_index[0]]
        gpu_text = f"GPU Name: {gpu['name']}\n" \
                   f"Driver Version: {gpu['driverVersion']}\n" \
                   f"Video Processor: {gpu['videoProcessor']}\n" \
                   f"VRAM: {gpu['VRAM']} MB"
        gpu_label.configure(text=gpu_text)
        gpu_title.configure(text=f"GPU Specifications ({gpu_index[0]+1}/{len(gpu_list)})")
        prev_gpu_btn.configure(state="normal" if gpu_index[0] > 0 else "disabled")
        next_gpu_btn.configure(state="normal" if gpu_index[0] < len(gpu_list)-1 else "disabled")

    gpu_title = CTkLabel(three_dots_details, text=f"GPU Specifications (1/{len(gpu_list)})", font=("Poppins", 20, "bold"))
    gpu_title.place(relx=0.15, rely=0.6, anchor="center")
    gpu_label = CTkLabel(three_dots_details, text="", font=("Poppins", 12))
    gpu_label.place(relx=0.15, rely=0.71, anchor="center")

    prev_gpu_btn = CTkButton(three_dots_details, text="<", width=30, command=lambda: (gpu_index.__setitem__(0, gpu_index[0]-1), update_gpu_label()))
    prev_gpu_btn.place(relx=0.03, rely=0.6, anchor="center")
    next_gpu_btn = CTkButton(three_dots_details, text=">", width=30, command=lambda: (gpu_index.__setitem__(0, gpu_index[0]+1), update_gpu_label()))
    next_gpu_btn.place(relx=0.27, rely=0.6, anchor="center")
    update_gpu_label()

    # ram
    ram_index = [0]
    ram_list = specs_list[2]

    def update_ram_label():
        ram = ram_list[ram_index[0]]
        ram_text = f"Capacity: {ram['capacity']} GB\n" \
                   f"Speed: {ram['speed']} MHz\n" \
                   f"Manufacturer ID: {ram['manufacturer']}\n" \
                   f"Part Number: {ram['partNumber']}"
        ram_label.configure(text=ram_text)
        ram_title.configure(text=f"RAM Specifications ({ram_index[0]+1}/{len(ram_list)})")
        prev_ram_btn.configure(state="normal" if ram_index[0] > 0 else "disabled")
        next_ram_btn.configure(state="normal" if ram_index[0] < len(ram_list)-1 else "disabled")

    ram_title = CTkLabel(three_dots_details, text=f"RAM Specifications (1/{len(ram_list)})", font=("Poppins", 20, "bold"))
    ram_title.place(relx=0.5, rely=0.22, anchor="center")
    ram_label = CTkLabel(three_dots_details, text="", font=("Poppins", 12))
    ram_label.place(relx=0.5, rely=0.33, anchor="center")

    prev_ram_btn = CTkButton(three_dots_details, text="<", width=30, command=lambda: (ram_index.__setitem__(0, ram_index[0]-1), update_ram_label()))
    prev_ram_btn.place(relx=0.38, rely=0.22, anchor="center")
    next_ram_btn = CTkButton(three_dots_details, text=">", width=30, command=lambda: (ram_index.__setitem__(0, ram_index[0]+1), update_ram_label()))
    next_ram_btn.place(relx=0.62, rely=0.22, anchor="center")
    update_ram_label()

    # disk
    disk_index = [0]
    disk_list = specs_list[3]

    def update_disk_label():
        disk = disk_list[disk_index[0]]
        disk_text = f"Model: {disk['model']}\n" \
                    f"Interface Type: {disk['interfaceType']}\n" \
                    f"Media Type: {disk['mediaType']}\n" \
                    f"Size: {disk['size']} GB\n" \
                    f"Serial Number: {disk['serialNumber']}"
        disk_label.configure(text=disk_text)
        disk_title.configure(text=f"Disk Specifications ({disk_index[0]+1}/{len(disk_list)})")
        prev_disk_btn.configure(state="normal" if disk_index[0] > 0 else "disabled")
        next_disk_btn.configure(state="normal" if disk_index[0] < len(disk_list)-1 else "disabled")

    disk_title = CTkLabel(three_dots_details, text=f"Disk Specifications (1/{len(disk_list)})", font=("Poppins", 20, "bold"))
    disk_title.place(relx=0.5, rely=0.6, anchor="center")
    disk_label = CTkLabel(three_dots_details, text="", font=("Poppins", 12))
    disk_label.place(relx=0.5, rely=0.73, anchor="center")

    prev_disk_btn = CTkButton(three_dots_details, text="<", width=30, command=lambda: (disk_index.__setitem__(0, disk_index[0]-1), update_disk_label()))
    prev_disk_btn.place(relx=0.38, rely=0.6, anchor="center")
    next_disk_btn = CTkButton(three_dots_details, text=">", width=30, command=lambda: (disk_index.__setitem__(0, disk_index[0]+1), update_disk_label()))
    next_disk_btn.place(relx=0.62, rely=0.6, anchor="center")
    update_disk_label()

    # network card
    network_title = CTkLabel(three_dots_details, text=f"Network Card Specifications", font=("Poppins", 20, "bold"))
    network_title.place(relx=0.85, rely=0.22, anchor="center")

    network_text = (
    f"Name: {specs_list[4]['name']}\n"
    f"MAC Address: {specs_list[4]['macAddress']}\n"
    f"Manufacturer: {specs_list[4].get('manufacturer', 'N/A')}\n"
    f"Adapter Type: {specs_list[4].get('adapterType', 'N/A')}\n"
    f"Speed: {specs_list[4].get('speed', 'N/A')} Mbps"
    )

    network_label = CTkLabel(three_dots_details, text=network_text, font=("Poppins", 12))
    network_label.place(relx=0.85, rely=0.35, anchor="center")

    # battery
    battery_title = CTkLabel(three_dots_details, text=f"Battery Specifications", font=("Poppins", 20, "bold"))
    battery_title.place(relx=0.85, rely=0.6, anchor="center")

    battery_text = (
        f"Name: {specs_list[5]['name']}\n"
        f"Estimated Charge Remaining: {specs_list[5]['estimatedChargeRemaining']}%\n"
        f"Status: {specs_list[5]['batteryStatus']}\n"
        f"Design Capacity: {specs_list[5]['designCapacity']} mAh\n"
        f"Full Charge Capacity: {specs_list[5]['fullChargeCapacity']} mAh"
    )

    battery_label = CTkLabel(three_dots_details, text=battery_text, font=("Poppins", 12))
    battery_label.place(relx=0.85, rely=0.73, anchor="center")

