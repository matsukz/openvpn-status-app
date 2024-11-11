import subprocess

def restart(service_name) -> bool:
    result = subprocess.run(
        ["systemctl", "restart", service_name],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        return True
    else:
        print(f"{service_name} Restart Fail. {result.stderr}")
        return False