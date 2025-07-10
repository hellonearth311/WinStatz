from ui_functions import *

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

    root.mainloop()