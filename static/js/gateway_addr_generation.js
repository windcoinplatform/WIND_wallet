$(document).ready(function () {

    $("#waves_gw_send").click(function () {
            var amount = $("#waves_amount").val();
            var addr = $("#waves_addr").val();
            var fee = 0.01;

            const data = {amount: parseFloat(amount) + parseFloat(fee), addr: addr};
            gw_tx('waves', data)

        }
    );
    $("#tn_gw_send").click(function () {
            var amount = $("#tn_amount").val();
            var addr = $("#tn_addr").val();
            var fee = 0.09;

            const data = {amount: parseFloat(amount) + parseFloat(fee), addr: addr};
            gw_tx('tn', data)

        }
    );

    function gw_tx(gw, sendData) {
        $.ajax({
            type: "POST",
            data: JSON.stringify(sendData),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            url: '/gw/send/' + gw,

        }).done(function (data) { //same as .success (depricated as of 1.8)
            alert("Data: " + data)
        })
            .fail(function (jqXHR, textStatus, errorThrown) { //replaces .error
                console.log("error");
                console.dir(arguments);
            })
    }


})
;
