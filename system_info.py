import platform
import winreg
import psutil
import GPUtil
import pyperclip
from cpuinfo import get_cpu_info


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


def get_windows_version():
    window_info = {"Edition": "", "Version": "", "Build": ""}
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion")
    window_info["Edition"] = f'Windows {platform.release()} {platform.win32_edition()}'
    window_info["Version"] = winreg.QueryValueEx(key, "DisplayVersion")[0]
    window_info["Build"] = f'{winreg.QueryValueEx(key, "CurrentBuild")[0]}.{winreg.QueryValueEx(key, "UBR")[0]}'
    return window_info


def get_motherboard_info():
    motherboard = {"Motherboard": "", "Bios": ""}
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"Hardware\Description\System\BIOS")
    motherboard["Motherboard"] = winreg.QueryValueEx(key, "BaseBoardProduct")[0]
    motherboard["Bios"] = winreg.QueryValueEx(key, "BIOSVersion")[0]
    return motherboard


def get_cpuinfo():
    cpu_info = get_cpu_info()
    cpu = {"Processor": cpu_info["brand_raw"],
           "Cores": psutil.cpu_count(logical=False),
           "Threads": psutil.cpu_count(logical=True)}
    return cpu


def get_gpu_info():
    gpu_info = GPUtil.getGPUs()
    gpu = {"GPU": gpu_info[0].name,
           "Memory": get_size(int(gpu_info[0].memoryTotal) << 20),
           "Driver Version": gpu_info[0].driver}
    return gpu


def pretty_print_system_info(info):
    output = []
    cpu_info = info["CPU"]
    output.append("CPU Information:")
    output.append(f"  Processor: {cpu_info['Processor']}")
    output.append(f"  Cores: {cpu_info['Cores']} | Threads: {cpu_info['Threads']}\n")

    motherboard_info = info["Motherboard"]
    output.append("Motherboard Information:")
    output.append(f"  Motherboard: {motherboard_info['Motherboard']}")
    output.append(f"  BIOS Version: {motherboard_info['Bios']}\n")

    gpu_info = info["GPU"]
    output.append("GPU Information:")
    output.append(f"  GPU: {gpu_info['GPU']}")
    output.append(f"  Memory: {gpu_info['Memory']}")
    output.append(f"  Driver Version: {gpu_info['Driver Version']}\n")

    os_info = info["OS"]
    output.append("Operating System Information:")
    output.append(f"  Edition: {os_info['Edition']}")
    output.append(f"  Version: {os_info['Version']}")
    output.append(f"  Build: {os_info['Build']}\n")

    # Join all lines into a single string
    return "\n".join(output)


def copy_to_clipboard(text):
    pyperclip.copy(text)
    print("System information copied to clipboard!")


def fetch_system_info():
    """Fetch all system information and return it as a formatted string."""
    combined_info = {
        "CPU": get_cpuinfo(),
        "Motherboard": get_motherboard_info(),
        "GPU": get_gpu_info(),
        "OS": get_windows_version()
    }
    return pretty_print_system_info(combined_info)