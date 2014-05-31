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


var ombrelloneIcon = L.icon({
    iconUrl: '/static/js/images/ombrellone.png',

    iconSize:     [32, 32], // size of the icon
    iconAnchor:   [22, 30], // point othe icon which will correspond to marker's location
    popupAnchor:  [-6, -27] // point from which the popup should open relative to the iconAnchor
});
