$(function() {
    var booking_modal;
    $("#book-button").on("click", function(evt){
        evt.preventDefault();
        $.ajax({
            url: $(this).data("url"),
            success: function(booking_form) {
                $("#booking-form").html(booking_form);
                booking_modal = $("#booking-modal").modal("show");
            }
        });
    });
    $("#booking-form").on("click", "form button", function(evt){
        evt.preventDefault();
        showSpinner("#booking-modal");
        $.ajax({
            url: $("#booking-form form").attr("action"),
            type: $("#booking-form form").attr("method").toUpperCase(),
            data: $("#booking-form form" ).serialize(),
            success: function(contact_response) {
                hideSpinner("#booking-modal");
                var modal = $(contact_response).filter("#booking-modal");
                if(modal.length > 0)
                {
                    $("#booking-modal .modal-dialog").replaceWith(modal.html());
                }
                else
                {
                    if($("#messages").length > 0)
                    {
                        $("#messages").append($(contact_response).find("#messages div").html());
                    }
                    else{
                        $("#rootContainer").prepend($(contact_response).find("#messages").html());
                    }
                    $('.modal-backdrop').remove();
                    $('body').removeClass('modal-open');

                    booking_modal.hide();
                }
            }
        });
    });
});