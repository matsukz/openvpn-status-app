import subprocess

def start(service_name) -> bool:
    result = subprocess.run(
        ["systemctl", "start", service_name],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        return True
    else:
        print(f"{service_name} Restart Fail. {result.stderr}")
        return False

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
    
def stop(service_name) -> bool:
    result = subprocess.run(
        ["systemctl", "stop", service_name],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        return True
    else:
        print(f"{service_name} Restart Fail. {result.stderr}")
        return False