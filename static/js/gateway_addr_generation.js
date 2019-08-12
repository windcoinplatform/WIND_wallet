$(document).ready(function () {
    $('#gateway_select_id').on('change', function () {
        $('.hide').hide();
        $('#' + this.value + '_container').show();
    });

    $(".gw_load_dep").click(function () {
        const gwname = $(this).data("gwname");
        $("#" + gwname + "_collapse_wd_div").hide();
        $("#" + gwname + "_collapse_dep_div").toggle();
        if (gwname !== "tn") {
            $.ajax({
                type: "GET",
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                url: '/gateway/' + gwname,

            }).done(function (data) { //same as .success (depricated as of 1.8)
                $("#" + gwname + "_personal_p").text('Send amount bigger then ' + data['fee'] + ' $' + data['name'] + '\n' +
                    '                        to ' + data['personal_addr'])
            })
                .fail(function (jqXHR, textStatus, errorThrown) { //replaces .error
                    console.log("error");
                    console.dir(arguments);
                })
        }
    });

    $(".gw_load_wd").click(function () {
        const gwname = $(this).data("gwname");
        $("#" + gwname + "_collapse_dep_div").hide();
        $("#" + gwname + "_collapse_wd_div").toggle();

    });

    $(".gw_send").click(function () {
            const gwname = $(this).data("gwname");
            const fee = $(this).data("fee");

            var amount = $("#" + gwname + "_amount").val();
            var addr = $("#" + gwname + "_addr").val();
            var tx_fee = $("#" + gwname + "_fee").val();

            const data = {amount: parseFloat(amount) + parseFloat(fee), addr: addr, fee: tx_fee};
            gw_tx(gwname, data)

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
            $("#Modal-body").html(JSON.stringify(data).replace("null", "Something went wrong.\n"));
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
