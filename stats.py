import psutil
import wmi
import time

# TODO
# - add support for multiple RAM sticks, multiple GPUs, and multiple disks
# - check all details in update_stats()
# - add better error handling for individual hardware components in the get_specs() function
# - check if i can make something in c or c++ that can get gpu usage for all gpu types
# - make docstring code by typing
# - make gui (make sure to use matplotlib for graphs n shit)

def get_usage():
    '''
    Get real-time usage data for most system components. \n
    GPU Usage is **not** supported due to lack of a Python binding for AMD and Intel GPUs.\n

    This function returns a list of 4 dictionaries and 1 list.\n
    [cpu_usage (dict), ram_usage (dict), disk_usages (list of dicts), network_usage (dict), battery_usage (dict)] \n
    
    ### Below is an index of every element in every dictionary/list
    #### cpu_usage
    {\n
    "core1": (usage),\n
    "core2": (usage),\n
    [Repeats for every core]\n
    }
    #### ram_usage,
    {\n
    "total": total ram,\n
    "used": amount of ram used,\n
    "free": amount of ram that is free,\n
    "percent": percentage utilization of memory\n
    }
    #### disk_usages
    [\n
    {\n
    "device": ex: C:// (pretend they are backslashes), \n
    "mountpoint": same as above, \n
    "fstype": file system. eg. NTFS, APFS, \n
    "total": total amount in GB, \n
    "used": amount used in GB, \n
    "free": amount unused in GB, \n
    "percentUsed": amount used as a percentage \n
    }\n
    (this repeats for every disk/partition)
    ]
    #### network_usage
    {\n
    "up": upload speed in mbps,\n
    "down": download speed in mbps,\n
    }
    #### battery_usage
    {\n
    "percent": percent left,\n
    "pluggedIn": is the battery plugged in,\n
    "timeLeftMins": time left in minutes, if it returns 2147483640 that means unlimited,\n
    }
    '''
    # cpu usage
    cpu_usage_list = psutil.cpu_percent(percpu=True)

    cpu_usage = {}
    i = 1
    for core in cpu_usage_list:
        cpu_usage[f"core{i}"] = core
        i += 1

    print("cpu_usage")
    print(cpu_usage)

    # ram usage
    ram = psutil.virtual_memory()

    ram_usage = {
        "total": round(ram.total / (1024 ** 2), 1),
        "used": round(ram.used / (1024 ** 2), 1),
        "free": round(ram.available / (1024 ** 2), 1),
        "percent": ram.percent
    }

    print("ram usage")
    print(ram_usage)

    # disk usage
    disk_usages = []

    partitions = psutil.disk_partitions(all=False)
    for part in partitions:
        try:
            usage = psutil.disk_usage(part.mountpoint)
            disk_usages.append({
                "device": part.device,
                "mountpoint": part.mountpoint,
                "fstype": part.fstype,
                "total": round(usage.total / (1024 ** 3), 2),
                "used": round(usage.used / (1024 ** 3), 2),
                "free": round(usage.free / (1024 ** 3), 2),
                "percentUsed": usage.percent
            })
        except PermissionError:
            pass
    
    print("disk usages")
    for disk in disk_usages:
        print(disk)

    # network usage
    net1 = psutil.net_io_counters()
    time.sleep(1)
    net2 = psutil.net_io_counters()

    upload_speed = (net2.bytes_sent - net1.bytes_sent) / 125
    download_speed = (net2.bytes_recv - net1.bytes_recv) / 125

    network_usage = {
        "up": upload_speed,
        "down": download_speed
    }

    print("network usage")
    print(network_usage)

    # battery stats
    battery = psutil.sensors_battery()
    battery_usage = {
        "percent": battery.percent,
        "pluggedIn": battery.power_plugged,
        "timeLeftMins": battery.secsleft // 60 if battery.secsleft != psutil.POWER_TIME_UNLIMITED else 2147483640
    }

    print("battery usage")
    print(battery_usage)

def get_specs():
    '''
    Get all of the specifications of your system. \n
    It returns a list called specs. Inside the list, there are 6 dictionaries: \n
    [cpu_data, gpu_data, ram_data, storage_data, network_data, battery_data]. \n

    ### Below is an index of each element in every dictionary.
    #### cpu_data
    {\n
    "name": The name of your CPU. Ex. 11th Gen Intel(R) Core(TM) i5-1135G7 @2.40GHz\n
    "manufacturer": Manufacturer of your CPU. Ex. GenuineIntel\n
    "description": Some architecture information about your CPU. Ex. Intel64 Family 6 Model 140 Stepping 1\n
    "coreCount": Core count of your CPU. Ex. 4\n
    "clockSpeed": The clock speed of your CPU in megahertz. Ex. 2419\n
    }
    #### gpu_data
    {\n
    "name": The name of your GPU. Ex. Intel(R) Iris(R) Xe Graphics\n
    "driverVersion": The driver version that your GPU is on. Ex. 31.0.101.5333\n
    "videoProcessor": The chipset behind your GPU. Ex. Intel(R) Iris(R) Xe Graphics\n
    "videoModeDesc": The resolution and color coverage your GPU is currently running at. Ex. 1920 x 1080 x 4294967296 colors\n
    "VRAM": The amount of VRAM (Video Memory) your GPU has in MB. Ex. 128\n
    }
    #### ram_data
    {\n
    "capacity": The capacity of your RAM in MB. Ex. 8192\n
    "speed": The speed of your RAM in megahertz. Ex. 3200\n
    "manufacturer": The manufacturer ID of your RAM. Ex 80AD000080AD\n
    "partNumber": The part number of your RAM. Ex. HMAA1GS6CJR6N-XN\n
    }
    #### storage_data
    {\n
    "model": The model of your disk. Ex. NVMe BC711 NVMe SK hynix 256GB\n
    "interfaceType": How your storage device connects to your system. Ex. SCSI\n
    "mediaType": What kind of storage media the device is. Ex. Fixed hard disk media\n
    "size": The available storage space in GB. Ex. 238\n
    "serialNumber": The serial number of the storage device. Ex. JSB9D018264825J8H_00000001\n
    }
    #### network_data
    {\n
    "name": The name of the network adapter. Ex. Intel(R) Wireless-AC 9462\n
    "macAddress": Your MAC Address. Ex. DC:21:48:DF:E9:68\n
    "manufacturer": Who made the device. Ex. Intel Corporation\n
    "adapterType": The type of the adapter, like Ethernet or WiFi. Ex. Ethernet 802.3\n
    "speed": The speed of the adapter in MBPS. Ex. 433.3\n
    }
    #### battery_data
    {\n
    "name": The model of your battery. Ex. NVMe BC711 NVMe SK hynix 256GB\n
    "estimatedChargeRemaining": How much percentage battery you have left. Ex. SCSI\n
    "batteryStatus": Status of the battery. Ex. Charging\n
    "designCapacity": The design capacity of the battery. Ex. 5000 mWh\n
    "fullChargeCapacity": The current capacity of the battery. Ex. 4950 mWh\n
    } \n

    ### Notes:
    * If anything returns None, it means it could not be found.
    * For the GPU, RAM, Storage, and Network Adapters, it will return a list with all of your hardware of that category in
    '''
    try:
        # main system component
        c = wmi.WMI()

        # get cpu info
        cpu_data = {}
        for cpu in c.Win32_Processor():
            cpu_data["name"] = cpu.Name
            cpu_data["manufacturer"] = cpu.Manufacturer
            cpu_data["description"] = cpu.Description
            cpu_data["coreCount"] = cpu.NumberOfCores
            cpu_data["clockSpeed"] = cpu.MaxClockSpeed

        print("cpu info")
        print(cpu_data)

        # get gpu info
        gpu_data = {}
        for gpu in c.Win32_VideoController():
            gpu_data["name"] = gpu.Name
            gpu_data["driverVersion"] = gpu.DriverVersion
            gpu_data["videoProcessor"] = gpu.Description
            gpu_data["videoModeDesc"] = gpu.VideoModeDescription
            gpu_data["VRAM"] = int(gpu.AdapterRAM) // (1024 ** 2)

        print("gpu info")
        print(gpu_data)

        # get ram info
        ram_data = {}
        for ram in c.Win32_PhysicalMemory():
            ram_data["capacity"] = int(ram.Capacity) // (1024 ** 2)
            ram_data["speed"] = ram.Speed
            ram_data["manufacturer"] = ram.Manufacturer.strip()
            ram_data["partNumber"] = ram.PartNumber.strip()
        
        print("ram info")
        print(ram_data)

        # get storage info
        storage_data = {}
        for disk in c.Win32_DiskDrive():
            storage_data["model"] = disk.Model
            storage_data["interfaceType"] = disk.InterfaceType
            storage_data["mediaType"] = getattr(disk, "MediaType", "Unknown")
            storage_data["size"] = int(disk.Size) // (1024**3) if disk.Size else None
            storage_data["serialNumber"] = disk.SerialNumber.strip() if disk.SerialNumber else "N/A"
        
        print("disk info")
        print(storage_data)
        
        # get network/wifi info
        network_data = {}
        for nic in c.Win32_NetworkAdapter():
            if nic.PhysicalAdapter and nic.NetEnabled:
                network_data["name"] = nic.Name
                network_data["macAddress"] = nic.MACAddress
                network_data["manufacturer"] = nic.Manufacturer
                network_data["adapterType"] = nic.AdapterType
                network_data["speed"] = int(nic.Speed) / 1000000
        
        print("network info")
        print(network_data)

        # get battery info
        battery_data = {}
        for batt in c.Win32_Battery():
            battery_data["name"] = batt.Name
            battery_data["estimatedChargeRemaining"] = batt.EstimatedChargeRemaining

            # interpret battery status
            match int(batt.BatteryStatus):
                case 1:
                    battery_data["batteryStatus"] = "Discharging"
                case 2:
                    battery_data["batteryStatus"] = "Plugged In, Fully Charged"
                case 3:
                    battery_data["batteryStatus"] = "Fully Charged"
                case 4:
                    battery_data["batteryStatus"] = "Low Battery"
                case 5:
                    battery_data["batteryStatus"] = "Critical Battery"
                case 6:
                    battery_data["batteryStatus"] = "Charging"
                case 7:
                    battery_data["batteryStatus"] = "Charging (High)"
                case 8:
                    battery_data["batteryStatus"] = "Charging (Low)"
                case 9:
                    battery_data["batteryStatus"] = "Charging (Critical)"
                case 10:
                    battery_data["batteryStatus"] = "Unknown"
                case 11:
                    battery_data["batteryStatus"] = "Partially Charged"
                case _:
                    battery_data["batteryStatus"] = "Unknown"
                
            battery_data["designCapacity"] = getattr(batt, "DesignCapacity", "N/A")
            battery_data["fullChargeCapacity"] = getattr(batt, "FullChargeCapacity", "N/A")

        
        print("battery_info")
        print(battery_data)

        # return everything
        return [cpu_data, gpu_data, ram_data, storage_data, network_data, battery_data]
    except Exception as e:
        print(f"Error getting data: {e}")
        return [None, None, None, None, None, None]

if __name__ == "__main__":
    get_specs()
    print("------------------------------------------------------------------------------------------------")
    get_usage()

