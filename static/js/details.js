$(document).ready(function () {

    $("#send").click(function () {
            const amount = $("#send_amount").val();
            const addr = $("#send_addr").val();
            const asset = $(this).data("asset");

            const data = {amount: parseFloat(amount), addr: addr};
            send_tx(data,asset);

        }
    );
    $("#burn").click(function () {
            const amount = $("#burn_amount").val();
            const asset = $(this).data("asset");
            const data = {amount: parseFloat(amount)};
            send_burn(data,asset);

        }
    );

    function send_tx(sendData, asset) {
        tx(sendData, '/assets/send/'+asset)
    }

    function send_burn(sendData, asset) {
        tx(sendData, '/assets/burn/'+asset)
    }

    function tx(sendData, url) {
        $.ajax({
            type: "POST",
            data: JSON.stringify(sendData),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            url: url,

        }).done(function (data) { //same as .success (depricated as of 1.8)
            alert("Data: " + JSON.stringify(data))
        })
            .fail(function (jqXHR, textStatus, errorThrown) { //replaces .error
                console.log("error");
                console.dir(arguments);
            })
    }


})
;
