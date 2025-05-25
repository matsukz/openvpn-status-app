import json
import time
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- 差分比較関数 ---
def compare_list_of_dicts(old_list, new_list, key_field="id"):
    old_dict = {item[key_field]: item for item in old_list}
    new_dict = {item[key_field]: item for item in new_list}

    added = {k: v for k, v in new_dict.items() if k not in old_dict}
    removed = {k: v for k, v in old_dict.items() if k not in new_dict}
    modified = {
        k: {"old": old_dict[k], "new": new_dict[k]}
        for k in old_dict.keys() & new_dict.keys()
        if old_dict[k] != new_dict[k]
    }

    return added, removed, modified

# --- イベントハンドラー ---
class ChangeHandler(FileSystemEventHandler):
    def __init__(self, watch_file, api_url, key_field="id"):
        self.watch_file = watch_file
        self.api_url = api_url
        self.key_field = key_field
        self.previous_data = self.fetch_json()

    def fetch_json(self):
        try:
            response = requests.get(self.api_url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print("API取得エラー:", e)
            return []

    def on_modified(self, event):
        if not event.src_path.endswith(self.watch_file):
            return

        print(f"\n[変更検知] {self.watch_file} が変更されました。WebAPIを呼び出します…")
        new_data = self.fetch_json()
        added, removed, modified = compare_list_of_dicts(self.previous_data, new_data, self.key_field)

        if added:
            print("=== 追加 ===")
            print(json.dumps(added, indent=4, ensure_ascii=False))

        if removed:
            print("=== 削除 ===")
            print(json.dumps(removed, indent=4, ensure_ascii=False))

        if modified:
            print("=== 変更 ===")
            print(json.dumps(modified, indent=4, ensure_ascii=False))

        if not (added or removed or modified):
            print("差分なし。")

        self.previous_data = new_data

# --- メイン処理 ---
WATCH_FILE = "/var/log/openvpn-status.log"  # 監視対象のダミーファイル名
API_URL = "http://fastapi:9004/ovpn/api/client/"  # WebAPIのURL
KEY_FIELD = "id"  # 比較に使う一意キー

observer = Observer()
handler = ChangeHandler(WATCH_FILE, API_URL, KEY_FIELD)
observer.schedule(handler, path=".", recursive=False)

print(f"[監視開始] ファイル '{WATCH_FILE}' の変更を検知して WebAPI の差分を確認します…")

observer.start()
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()