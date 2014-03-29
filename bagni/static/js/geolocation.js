$(function() {
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
    if(navigator.geolocation)
    {
        navigator.geolocation.getCurrentPosition(currentPositionSuccess, currentPositionFailure);
    }
    $("#search-form").submit(function(){
        if(pos == "")
        {
            currentPositionFailure();
        }
    });
});
