$(function(){
  $(".collapse").on("shown.bs.collapse", function () {
       $("#span"+this.id.toString()).removeClass('glyphicon-chevron-right').addClass("glyphicon-chevron-down");
  });
  $(".collapse").on('hidden.bs.collapse', function () {
       $("#span"+this.id.toString()).removeClass('glyphicon-chevron-down').addClass("glyphicon-chevron-right");
  });
  $("#facilities-list-trigger").on("click", function(){
    $('#facilities_modal').modal();
  });
});

function populateWhatField(aTag){
    $('#facilities_modal').modal('hide');
    $('#search_q').focus();
    $('#search_q').attr("value", aTag.innerHTML);
}
