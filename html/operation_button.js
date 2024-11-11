document.getElementById("btn_reboot").addEventListener("click",put_reboot);
document.getElementById("btn_start").addEventListener("click",btn_start);

function put_reboot(){

    let confirm = window.confirm("OpenVPNを再起動しますか？\n【警告】全てのセッションが切断されます");

    var url = new URL(window.location.href);
    var host = url.hostname;

    if(!confirm){
        return
    }

    $.ajax({
        type: "PUT",
        url: "http://" + host + ":9004/ovpn/api/status/?action=restart",
        cache: false 
    }).done(function(response){
       alert("再起動が完了しました!\n※反映には時間を要する場合があります");
       location.reload()
    }).fail(function(response){
        alert("リクエストに失敗しました");
        console.log(response)
    })
}

function btn_start(){


}