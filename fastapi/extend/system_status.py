import subprocess

def check_service_status(service_name) -> bool:
    try:
        result = subprocess.run(
            ['systemctl', 'is-active', service_name],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        # コマンドの出力結果をチェック
        if result.stdout.strip() == 'active':
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking service status: {e}")
        return False