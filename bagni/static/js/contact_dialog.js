$(function() {
    var contacts_modal;
    $("#contact-form-button").on("click", function(evt){
        evt.preventDefault();
        $.ajax({
            url: $(this).data("url"),
            success: function(contact_form) {
                $("#contact-form").html(contact_form);
                contacts_modal = $("#contacts-modal").modal("show");
            }
        });
    });
    $("#contact-form").on("click", "form button", function(evt){
        evt.preventDefault();
        showSpinner("#contacts-modal");
        $.ajax({
            url: $("#contact-form form").attr("action"),
            type: $("#contact-form form").attr("method").toUpperCase(),
            data: $("#contact-form form" ).serialize(),
            success: function(contact_response) {
                hideSpinner("#contacts-modal");
                var modal = $(contact_response).filter("#contacts-modal");
                if(modal.length > 0)
                { 
                    $("#contacts-modal .modal-dialog").replaceWith(modal.html());
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
                    
                    contacts_modal.hide();
                }
            }
        });
    });
});
