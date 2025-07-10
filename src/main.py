from ui import build_main_ui

# TODO
# - add support for multiple RAM sticks, multiple GPUs, and multiple disks
# - check all details in update_stats()
# - add better error handling for individual hardware components in the get_specs() function
# - check if i can make something in c or c++ that can get gpu usage for all gpu types
# - make docstring code by typing
# - make gui (make sure to use matplotlib for graphs n shit)

if __name__ == "__main__":
    build_main_ui()