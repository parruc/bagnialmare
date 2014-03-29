$(function() {

    var lang = $("html").attr("lang");
    $("#search_l").autocomplete({
        source: function (request, response) {
            jQuery.get("/"+ lang +"/json/autocomplete/places", {
            query: request.term
            }, function (data) {
                response(data["success"]);
            });
        },
        minLength: 1
    }).attr('autocomplete', 'off');

    $("#search_q").autocomplete({
        source: function (request, response) {
            jQuery.get("/"+ lang +"/json/autocomplete/searchterms", {
            query: request.term
            }, function (data) {
                response(data["success"]);
            });
        },
        minLength: 1
    }).attr('autocomplete', 'off');
});
