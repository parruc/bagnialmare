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
    //iconUrl: '/static/js/images/ombrellone.png',
    iconUrl: '/static/js/images/marker-icon-2x.png',
    iconSize: [25,41],
    iconAnchor: [12, 41],
    popupAnchor: [-3, -76],
    shadowUrl: '/static/js/images/marker-shadow.png',
    shadowSize: [41, 41],
    shadowAnchor: [9, 40]
});

$(function(){
  $("a[href^='http']:not([href^='http://bagnialmare.com'])").addClass("external");
  $("a:not([href^='http']), a[href^='http://bagnialmare.com']").addClass("internal");
});

