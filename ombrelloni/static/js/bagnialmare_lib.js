function showSpinner(selector)
{
  selector = selector || "body";
  $(selector).append("<div class='modal-wheel'></div>");
  $(".modal-wheel").fadeIn('fast');
}

function hideSpinner(selector)
{
  selector = selector || "body";
  $(".modal-wheel").fadeOut('fast', function(){
    $(".modal-wheel").remove();
  }); 
}