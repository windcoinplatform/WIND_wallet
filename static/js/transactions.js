$(document).ready(function () {

    $("#tx_load").click(function () {
            const addr = $(this).data("addr");
            $("#tx_collapse_div").toggle();
            load_tx(addr, 200);

        }
    );

    function load_tx(addr, amount) {
        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            url: '/state/transactions/' + addr + '/' + amount,

        }).done(function (data) {
            let tablecontents = "";
            tablecontents = '<table>';
            tablecontents += '<tr><th>Type</th><th>Id</th><th>Sender</th><th>Amount</th><th>Asset Id</th><th>Recipient</th><th>Height</th></tr>';
            $.each(data[0], function (index, value) {

                tablecontents += "<tr class='tr'>";
                tablecontents += "<td>" + value["type"] + "</td>";
                tablecontents += "<td>" + value["id"]  + "</td>";
                tablecontents += "<td>" + value["sender"] + "</td>";
                tablecontents += "<td>" + value["amount"]  + "</td>";
                tablecontents += "<td>" + value["assetId"] + "</td>";
                tablecontents += "<td>" + value["recipient"]  + "</td>";
                tablecontents += "<td>" + value["height"]  + "</td>";
                tablecontents += "</tr>";
            });
            tablecontents += '</table>';

            $("#tx_collapse_div").append(tablecontents);

        })
            .fail(function (jqXHR, textStatus, errorThrown) { //replaces .error
                console.log("error");
                console.dir(arguments);
            })
    }


})
;
