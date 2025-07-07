import psutil

def update_stats():
    cpu_usage = psutil.cpu_percent()
    ram_usage = psutil.virtual_memory().percent

    print(cpu_usage, ram_usage)

update_stats()

