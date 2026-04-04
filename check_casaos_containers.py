import subprocess
import sys

def run_ssh_command(host, command):
    """Runs a command on the remote host via SSH."""
    ssh_cmd = ["ssh", host, command]
    try:
        result = subprocess.run(ssh_cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error connecting to {host}: {e.stderr.strip()}"
    except FileNotFoundError:
        return "Error: 'ssh' command not found."

def check_containers():
    host = "casaos-direct"
    print(f"--- [ CasaOS Docker Container Status ({host}) ] ---")

    # Command to get container names and their status
    # --format uses Go templates to get clean, tab-separated output
    docker_cmd = "docker ps -a --format '{{.Names}}\t{{.Status}}'"
    
    output = run_ssh_command(host, docker_cmd)

    if "Error" in output:
        print(f"   {output}")
        return

    if not output:
        print("   No Docker containers found.")
        return

    # Print header
    print(f"{'Container Name':<30} | {'Status'}")
    print("-" * 50)

    # Parse and print each container
    lines = output.split('\n')
    for line in lines:
        if '\t' in line:
            name, status = line.split('\t')
            # Add a visual indicator for running vs stopped
            indicator = "✅" if "Up" in status else "❌"
            print(f"{name:<30} | {indicator} {status}")
        else:
            print(f"   Could not parse line: {line}")

if __name__ == "__main__":
    check_containers()
