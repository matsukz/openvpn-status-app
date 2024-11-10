import re

def parse_openvpn_status(file_path):
    client_list = []
    
    # 正規表現でクライアントの情報を抽出する
    client_regex = re.compile(r"^CLIENT_LIST\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S*)\s+(\d+)\s+(\d+)\s+([\d\-]+\s[\d:]+)\s+(\d+)\s+(\S+)\s+(\d+)\s+(\d+)\s+(\S+)")
    
    # ステータスファイルを読み込む
    with open(file_path, "r") as file:
        for line in file:
            match = client_regex.match(line)
            if match:
                client_info = {
                    "Common_Name": match.group(1),
                    "Real_Address": match.group(2),
                    "Virtual_Address": match.group(3),
                    "Virtual_IPv6_Address": match.group(4),
                    "Bytes_Received": int(match.group(5)),
                    "Bytes_Sent": int(match.group(6)),
                    "Connected_Since": match.group(7),
                    "Connected_Since (time_t)": int(match.group(8)),
                    "Username": match.group(9),
                    "Client_ID": int(match.group(10)),
                    "Peer_ID": int(match.group(11)),
                    "Data_Channel_Cipher": match.group(12)
                }
                client_list.append(client_info)
        return client_list
    