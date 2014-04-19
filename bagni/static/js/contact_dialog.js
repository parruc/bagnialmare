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
        $.ajax({
            url: $("#contact-form form").attr("action"),
            type: $("#contact-form form").attr("method").toUpperCase(),
            data: $("#contact-form form" ).serialize(),
            success: function(contact_response) {
                if($(contact_response, "#contacts-modal"))
                {
                    contacts_modal.hide();
                    $("#contacts-modal .modal-dialog").replaceWith($(contact_response, ".modal-dialog").html());
                    contacts_modal.show();
                }
                else
                {
                    if($("#wrap #messages").length > 0)
                    {
                        $("#wrap #messages").append($(contact_response, "#messages div"));
                    }
                    else{
                        $("#wrap .navbar").after($(contact_response, " #messages"));
                    }
                    contacts_modal.hide();
                }
            }
        });
    });
});
