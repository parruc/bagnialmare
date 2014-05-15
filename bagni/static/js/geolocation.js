function currentPositionSuccess(position)
{
    $("body").removeClass("loading");
    $(":input[name=coords]").val(position.coords.latitude + "," + position.coords.longitude);
    $(":input[name=l]").val($("#set-my-position").data("position-label"));
}
function currentPositionFailure(error)
{
    $("body").removeClass("loading");
    $(":input[name=coords]").val("");
    $(":input[name=l]").val("");
    /*Todo modal popup che prende contenuti tradotti dal template*/
    alert("Condivisione della posizione disattivata");
}
function setCurrentPosition()
{
    if(navigator.geolocation)
    {
        $("body").addClass("loading");
        navigator.geolocation.getCurrentPosition(currentPositionSuccess, currentPositionFailure, {timeout: 4000});
    }
}

$(function() {
    $("#set-my-position").click(function(evt){
        setCurrentPosition();
        evt.preventDefault();
    });

    $("#search-form").submit(function(){
    /*if position is set to current position and and there is no position set*/
        if($(":input[name=l]").val() == $("#set-my-position").data("position-label") && $(":input[name=coords]").val() == "")
        {
            currentPositionFailure();
        }
    });
});
