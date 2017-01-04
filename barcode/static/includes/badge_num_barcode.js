function barcodeScanned(barcode) {
    $.post("../registration/qrcode_reader", {csrf_token: csrf_token, qrcode: barcode})
        .success(function (json) {
            toastr.clear();
            var message = json.message;
            if (json.success) {
                if ($("#search_bar")) { $("#search_bar").val(json.data).parents('form').submit() }
            } else {
                $.post("../barcode/get_badge_num_from_barcode", {csrf_token: csrf_token, barcode: barcode})
                    .done(function (data) {
                        if ($("#checkin-badge")) { $("#checkin-badge").val(data['badge_num']) }
                        else if ($("#badge_num")) { $("#badge_num").val(data['badge_num']) }
                        else if ($("#search_bar")) { $("#search_bar").val(data['badge_num']) }
                    })
                    .fail(function(message) {
                        toastr.error(message);
                    });
            }
        })
        .fail(function () {
            toastr.error('Unable to connect to server, please try again.');
        })
}