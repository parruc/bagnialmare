/*$('body').on('click', 'a' function(evt) {
    alert('CLICK');
    var href = $(evt.target).attr('href');
    var internal = new RegExp('^(/|bagnialmare.com|http://bagnialmare.com).*');
    if(!internal.test(href)){
        window.open(href, '_system');
        evt.preventDefault();
    }
});*/

$(function(){
   var internal = new RegExp('^(/|bagnialmare.com|http://bagnialmare.com).*');
   $('a').each(function(){
       var href = $(this).attr('href');
       if(!internal.test(href)){
           $(this).hide();
       }
   });
});
