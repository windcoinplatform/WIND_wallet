function get(url) {
    $.ajax({
        type: "GET",
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


$(document).ready(function () {
    $("#send_tn").click(function () {
            const amount = $("#send_amount_tn").val();
            const addr = $("#send_addr_tn").val();
            const fee = $("#send_fee_tn").val();
            const data = {amount: parseFloat(amount), addr: addr, attachment: '', fee: parseFloat(fee)};
            send_tn(data);

        }
    );
    $("#lease_tn").click(function () {
            const amount = $("#lease_amount_tn").val();
            const addr = $("#lease_addr_tn").val();
            const fee = $("#lease_fee_tn").val();
            const data = {amount: parseFloat(amount), addr: addr, fee: parseFloat(fee)};
            lease_tn(data);

        }
    );
    $("#send").click(function () {
            const amount = $("#send_amount").val();
            const addr = $("#send_addr").val();
            const fee = $("#send_fee").val();
            const asset = $(this).data("asset");

            const data = {amount: parseFloat(amount), addr: addr, fee: parseFloat(fee)};
            send_tx(data, asset);

        }
    );
    $("#burn").click(function () {
            const amount = $("#burn_amount").val();
            const asset = $(this).data("asset");
            const fee = $("#burn_fee").val();
            const data = {amount: parseFloat(amount), fee: parseFloat(fee)};


            send_burn(data, asset);

        }
    );
    $("#create_alias_button").click(function () {
            const fee = $("#alias_fee").val();
            const alias = $("#alias_create_input").val();
            const data = {alias: alias, fee: parseFloat(fee)};


            create_alias(data);

        }
    );
    $(".cancel_lease").click(function () {
        const id = $(this).data("id");
        get('/state/leases/cancel/' + id)

    });

    function lease_tn(sendData) {
        tx(sendData, '/state/leases/start')
    }

    function send_tn(sendData) {
        tx(sendData, '/tn/send/')
    }

    function send_tx(sendData, asset) {
        tx(sendData, '/assets/send/' + asset)
    }

    function send_burn(sendData, asset) {
        tx(sendData, '/assets/burn/' + asset)
    }

    function create_alias(sendData) {
        tx(sendData, '/create/alias/')
    }

    function tx(sendData, url) {
        $.ajax({
            type: "POST",
            data: JSON.stringify(sendData),
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            url: url,

        }).done(function (data) { //same as .success (depricated as of 1.8)
                $("#Modal-body").html(JSON.stringify(data));
                $("#Modal-vert-center-demo-label").text("User feedback");
                $("#Modal-vert-center-demo").modal('show');
        })
            .fail(function (jqXHR, textStatus, errorThrown) { //replaces .error
                console.log("error");
                console.dir(arguments);
            })
    }


})
;
$(document).on("click", "button.cancel_lease", function () {
    const id = $(this).data("id");
    get('/state/leases/cancel/' + id)

});
