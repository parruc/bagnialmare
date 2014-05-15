function showSpinner(selector)
{
  selector = selector || "body";
  $(selector).append("<div class='modal-wheel'></div>");
  $(selector + " > .modal-wheel").fadeIn('fast');
}

function hideSpinner(selector)
{
  selector = selector || "body";
  $(selector + " > .modal-wheel").fadeOut('fast', function(){
    $(this).remove();
  }); 
}