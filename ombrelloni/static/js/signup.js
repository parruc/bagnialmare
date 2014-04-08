$(function() {
    $("#tos-content").hide();
    $("#privacy-content").hide();
    $("#id_privacy").next(".helptext").on("click", function(){
        $("#privacy-content").dialog().dialog("open");
    });
    $("#id_tos").next(".helptext").on("click", function(){
        $("#tos-content").dialog().dialog("open");
    });
});
