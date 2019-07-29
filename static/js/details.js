$(document).ready(function () {

    $("#send").click(function () {
            var amount = $("#amount").val();
            var addr = $("#waddr").val();

            const data = {amount: parseFloat(amount), addr: addr};
            alert("in future it will send with params "+JSON.stringify(data))

        }
    );
    $("#burn").click(function () {
            var amount = $("#amount").val();

            const data = {amount: parseFloat(amount)};
             alert("in future it will burn with params "+JSON.stringify(data))

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
            alert("Data: " + JSON.stringify(data))
        })
            .fail(function (jqXHR, textStatus, errorThrown) { //replaces .error
                console.log("error");
                console.dir(arguments);
            })
    }


})
;
