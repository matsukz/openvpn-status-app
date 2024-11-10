# OpenVPNセッション情報確認Webアプリ

* FastAPIのドキュメント使えます

## デプロイ
1. `/var/www`の中でgit cloneを実行します
2. nginxのインストールします
3. ドキュメントルートを`/var/www/openvpn-status-app/html`にします
4. `service`ファイルを`/etc/systemd/system`に移動します
5. サービスを再読込させます
    ```bash
    $ sudo systemctl daemon-reload
    ```

6. nginxを再起動します
   ```bash
   $ sudo systemctl restart nginx
   ```

7. FastAPIを起動します
   ```bash
   $ sudo systemctl start check-openvpn.service
   ```