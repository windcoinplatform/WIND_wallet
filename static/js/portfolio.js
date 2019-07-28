$(document).ready(function () {

    $(".details_btn").click(function () {
            let asset = $(this).attr('data-asset');
            alert(JSON.stringify(asset))


        }
    );
})
;