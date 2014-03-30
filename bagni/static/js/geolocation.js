var pos = "";
function currentPositionSuccess(position)
{
    pos = position.coords.latitude + "," + position.coords.longitude;
    $(":input[name=pos]").val(pos);
}
function currentPositionFailure(error)
{
    $(":input[name=pos]").remove();
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
        $(":input[name=l]").val($(this).data("position-label"));
        evt.preventDefault();
    });

    $("#search-form").submit(function(){
        if(pos == "")
        {
            currentPositionFailure();
        }
    });
});
