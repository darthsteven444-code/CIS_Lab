import subprocess
import sys

def run_remote_cmd(command):
    """Runs a command on the 'proxmox-remote' host via SSH."""
    ssh_command = ["ssh", "proxmox-remote", command]
    try:
        result = subprocess.run(ssh_command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"
    except FileNotFoundError:
        return "Error: 'ssh' command not found."

def main():
    print("--- [ proxmox-remote Vitals ] ---")

    # 1. CPU Temperature (Xeon)
    # We try 'sensors' first as it's more descriptive for Xeons, 
    # then fall back to thermal zones.
    temp_info = run_remote_cmd("sensors | grep 'Core' || cat /sys/class/thermal/thermal_zone*/temp")
    print("\n1. CPU Temperature:")
    if "Error" in temp_info:
        print(f"   {temp_info}")
    else:
        # If it's raw thermal zone data, convert to Celsius
        lines = temp_info.split('\n')
        for line in lines:
            if line.isdigit():
                print(f"   Core Temp: {int(line)/1000:.1f}°C")
            else:
                print(f"   {line}")

    # 2. Total RAM Usage
    ram_info = run_remote_cmd("free -h")
    print("\n2. RAM Usage:")
    print(ram_info if ram_info else "   Could not retrieve RAM info.")

    # 3. ZFS 'rpool' Status
    zfs_info = run_remote_cmd("zpool status rpool")
    print("\n3. ZFS 'rpool' Status:")
    if "Error" in zfs_info:
        print(f"   {zfs_info}")
    else:
        # Extracting the 'state' and 'errors' lines for a quick summary
        summary = [line.strip() for line in zfs_info.split('\n') if "state:" in line or "errors:" in line]
        if summary:
            for s in summary:
                print(f"   {s}")
        else:
            print("   rpool found, but could not parse status summary.")

if __name__ == "__main__":
    main()
