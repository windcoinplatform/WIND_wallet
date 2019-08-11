$(document).ready(function () {
    function testInput(event) {
        let value = String.fromCharCode(event.which);
        let pattern = new RegExp(/[a-z ]/i);
        return pattern.test(value);
    }

    $('#alias_create_input').bind('keypress', testInput);
    $("#alias_create_input").on('change keyup paste', function () {
        $(this).val($(this).val().toLowerCase());
    });

    $("#alias_load").click(function () {
            const addr = $(this).data("addr");
            $("#alias_collapse_div").toggle();
            alias_data(addr, "#alias_collapse_div");

        }
    );
    $("#alias_load_other").click(function () {
            const addr = $("#alias_other").val();
            $("#alias_other_collapse_div").toggle();
            alias_data(addr, "#alias_other_collapse_div");

        }
    );

    function alias_data(addr, divname) {
        $.ajax({
            type: "GET",
            contentType: "application/json; charset=utf-8",
            dataType: "json",
            url: '/state/aliases/by-address/' + addr,

        }).done(function (data) {
            let tablecontents = "";
            tablecontents = '<table>';
            tablecontents += '<tr><th>Alias</th></tr>';
            $.each(data, function (index, value) {

                tablecontents += "<tr class='tr'>";
                tablecontents += "<td>" + value + "</td>";

                tablecontents += "</tr>";
            });
            tablecontents += '</table>';

            $(divname).html(tablecontents);

        })
            .fail(function (jqXHR, textStatus, errorThrown) { //replaces .error
                console.log("error");
                console.dir(arguments);
            })
    }

})
;