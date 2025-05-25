document.getElementById("btn_reboot").addEventListener("click",put_reboot);
document.getElementById("btn_start").addEventListener("click",btn_start);

function put_reboot(){

    if(window.confirm("OpenVPNを再起動しますか？\n【警告】全てのセッションが切断されます")){
        var op_key = window.prompt("オペーレーションキーを入力してください", "");
        if(op_key == "" || op_key == null){
            window.alert('キャンセルされました');
            return
        }
    } else {
        return
    }

    var url = new URL(window.location.href);
    var host = url.hostname;
    const api = "http://" + host + ":9004/ovpn/api/status/";

    $.ajax({
        type: "PUT",
        url: api,
        cache: false,
        contentType: 'application/json',
        data: JSON.stringify({
            "action": "restart",
            "key": op_key
        })
    }).done(function(response){
        alert("再起動が完了しました!\n※反映には時間を要する場合があります");
        location.reload();
        return
    }).fail(function(response){
        console.log(response);
        alert("リクエストに失敗しました");
        return
    })

}

function btn_start(){

    const server_status = document.getElementById("btn_start").textContent;
    let action_query = "";
    let confirm = false;
    switch(server_status){
        case "開始":
            action_query = "start";
            confirm = window.confirm("OpenVPNを起動しますか？");
            break;
        default:
            action_query = "stop";
            confirm = window.confirm("OpenVPNを停止しますか？\n【警告】全てのセッションが切断されます");
            break;
    }

    if(!confirm){return;}

    var op_key = window.prompt("オペーレーションキーを入力してください", "");
    if(op_key == "" || op_key == null){
        window.alert('キャンセルされました');
        return
    }

    var url = new URL(window.location.href);
    var host = url.hostname;

    $.ajax({
        type: "PUT",
        url: "http://" + host + ":9004/ovpn/api/status/",
        cache: false,
        contentType: 'application/json',
        data: JSON.stringify({
            "action": action_query,
            "key": op_key
        })
    }).done(function(response){
       alert("操作が完了しました。\n※反映には時間を要する場合があります");
       location.reload()
    }).fail(function(response){
        alert("リクエストに失敗しました");
        console.log(response)
    })
}