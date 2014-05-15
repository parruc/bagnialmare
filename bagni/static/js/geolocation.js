var geo_timeout;
function currentPositionNoAnswerOrFailure()
{
    hideSpinner();
    $(":input[name=coords]").val("");
    $(":input[name=l]").val("");
    $('#geo-error-modal').modal('show');
}
function currentPositionNoAnswer()
{
  /*if position is set to current position and and there is no position set
  means that the user has dismissed or ignored the request*/
  if($(":input[name=coords]").val() == "")
  {
      currentPositionNoAnswerOrFailure();
  }
}

function currentPositionSuccess(position)
{
    clearTimeout(geo_timeout);
    hideSpinner();
    $(":input[name=coords]").val(position.coords.latitude + "," + position.coords.longitude);
    $(":input[name=l]").val($("#set-my-position").data("position-label"));
}
function currentPositionFailure(error)
{
    clearTimeout(geo_timeout);
    currentPositionNoAnswerOrFailure();
}
function setCurrentPosition()
{
    if(navigator.geolocation)
    {
        showSpinner();
        var options = {timeout:4000, maximumAge:0, enableHighAccuracy:false};
        geo_timeout = setTimeout(currentPositionNoAnswer, 6000);
        navigator.geolocation.getCurrentPosition(currentPositionSuccess, currentPositionFailure, options);
    }
    else
    {
      $('#geo-error-modal').modal('show');
    }
}

$(function() {
    $("#rootContainer").on("click", "#set-my-position", function(evt){
        setCurrentPosition();
        evt.preventDefault();
    });
});
