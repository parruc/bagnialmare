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
   // Remove social links (external)
   $(".social-links").hide();

   // Unwrap external links a tag
   $('a.external').each(function(){
       $(this).contents().unwrap();
   });

   // Make tel link work
   $('a[href^="tel:"]').click(function(evt){
       evt.preventDefault();
   });
});
