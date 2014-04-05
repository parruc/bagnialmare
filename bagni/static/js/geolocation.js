function currentPositionSuccess(position)
{
    $(":input[name=pos]").val(position.coords.latitude + "," + position.coords.longitude);
    $(":input[name=l]").val($("#set-my-position").data("position-label"));
}
function currentPositionFailure(error)
{
    $(":input[name=pos]").val("");
    $(":input[name=l]").val("");
}
function setCurrentPosition()
{
    if(navigator.geolocation)
    {
        navigator.geolocation.getCurrentPosition(currentPositionSuccess, currentPositionFailure);
    }
}

$(function() {
    $("#set-my-position").click(function(evt){
        setCurrentPosition();
        evt.preventDefault();
    });

    $("#search-form").submit(function(){
    /*if position is set to current position and and there is no position set*/
        if($(":input[name=l]").val() == $("#set-my-position").data("position-label") && $(":input[name=pos]").val() == "")
        {
            currentPositionFailure();
        }
    });
});
