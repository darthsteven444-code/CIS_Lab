import subprocess
import sys

def run_ssh_command(host, command):
    """Executes a command on a remote host via SSH."""
    ssh_cmd = ["ssh", host, command]
    try:
        result = subprocess.run(ssh_cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error connecting to {host}: {e.stderr}")
        return None
    except FileNotFoundError:
        print("Error: 'ssh' command not found. Please ensure SSH is installed.")
        return None

def get_health():
    host = "proxmox-remote"
    print(f"--- [ {host} Health Report ] ---")

    # Get CPU Temperature (usually in millidegrees Celsius)
    # This reads all thermal zones; usually zone 0 or 1 is the CPU.
    temp_raw = run_ssh_command(host, "cat /sys/class/thermal/thermal_zone*/temp")
    if temp_raw:
        temps = temp_raw.split('\n')
        for i, t in enumerate(temps):
            try:
                celsius = int(t) / 1000
                print(f"CPU Temp (Zone {i}): {celsius:.1f}°C")
            except ValueError:
                continue
    else:
        print("CPU Temp: Could not retrieve (ensure sensors are accessible).")

    # Get RAM Usage
    ram_info = run_ssh_command(host, "free -h")
    if ram_info:
        print("\nRAM Usage:")
        print(ram_info)
    else:
        print("RAM Usage: Could not retrieve.")

if __name__ == "__main__":
    get_health()
