$(document).ready(function(){

    var url = new URL(window.location.href);
    var host = url.hostname;

    document.getElementById("gettime").innerText = new Date().toLocaleString({ timeZone: 'Asia/Tokyo' });

    let server_status_bool = false

    $.ajax({
        type: "GET",
        url: "http://" + host + ":9004/ovpn/api/status/",
        contentType: "application/json",
        cache: false
    }).done(function(response){
        console.log(response.server_status);
        if(response.server_status){
            change_status("アクティブ");
        }else{
            change_status("ダウン");
        }
        server_status_bool = response.server_status;
    }).fail(function(response_status){
        change_status("不明");
    })

    //ボタンの形式を決める
    start_button = document.getElementById("btn_start");
    switch (server_status_bool){
        case true:
            start_button.classList.replace("btn-success", "btn-danger");
            start_button.textContent = "停止";
            break;
        default:
            start_button.classList.replace("btn-danger", "btn-success");
            start_button.textContent = "開始";
            break;

    }

    $.ajax({
        type: "GET",
        url: "http://" + host + ":9004/ovpn/api/client/",
        contentType: "application/json",
        cache: false
    }).done(function(response){

        const tablebody = document.querySelector("#maintable");
        console.log(response)

        response.forEach(person => {

            const row = document.createElement("tr");

            const cell_user = document.createElement("td");
            cell_user.textContent = person.Username;
            row.appendChild(cell_user);

            const cell_realaddress = document.createElement("td");
            cell_realaddress.textContent = person.Real_Address;
            row.appendChild(cell_realaddress);

            const cell_Connected_Since = document.createElement("td");
            cell_Connected_Since.textContent = person.Connected_Since;
            row.appendChild(cell_Connected_Since);

            const cell_virtual_Address = document.createElement("td");
            cell_virtual_Address.textContent = person.Virtual_Address;
            row.appendChild(cell_virtual_Address);

            const cell_Client_ID = document.createElement("td");
            cell_Client_ID.textContent = person.Client_ID;
            row.appendChild(cell_Client_ID);

            const cell_Bytes_Sent = document.createElement("td");
            cell_Bytes_Sent.textContent = person.Bytes_Sent / 100000;
            row.appendChild(cell_Bytes_Sent);
            
            const cell_Bytes_Received = document.createElement("td");
            cell_Bytes_Received.textContent = person.Bytes_Received /1000000;
            row.appendChild(cell_Bytes_Received);

            tablebody.appendChild(row);
        });

    }).fail(function(response){
        console.log(response);
    })

    function change_status(msg){
        document.getElementById("status").innerText = msg;
    }

})