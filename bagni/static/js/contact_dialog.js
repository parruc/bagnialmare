$(function() {
    $("#contact-form-button").on("click", function(evt){
        $("#contact-form").dialog().dialog('open');
        $.ajax({
            url: $(this).data("url"),
            success: function(contact_form) {
                $("#contact-form").html(contact_form);
                $("#contact-form").dialog().dialog('open');
                $("#contact-form form button").on("click", function(evt){
                    evt.preventDefault();
                    $.ajax({
                        url: $("#contact-form form").attr("action"),
                        type: $("#contact-form form").attr("method").toUpperCase(),
                        data: $("#contact-form form" ).serialize(),
                        success: function(contact_response) {
                            if($(contact_response, "#contatti"))
                            {
                                $("#contact-form").html($(contact_response, "#contatti"));
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
                                $("#contact-form").dialog().dialog('destroy');
                            }
                        }
                    });
                });
            }
        });
    });
});
