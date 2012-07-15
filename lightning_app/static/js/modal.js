$(document).ready(function() {    

     //select all the a tag with name equal to modal
     $('a[name=modal]').click(function(e) {
          e.preventDefault();
         
          //Get the A tag
          var id = $(this).attr('href');
    
          //Get the screen height and width
          var maskHeight = $(document).height();
          var maskWidth = $(window).width();
    
          //Set heigth and width to mask to fill up the whole screen
          $('#mask').css({'width':maskWidth,'height':maskHeight});
         
          //transition effect         
          $('#mask').fadeIn(1000);    
          $('#mask').fadeTo("slow",0.8);    
    
          //Get the window height and width
          var winH = $(window).height();
          var winW = $(window).width();
             
          //Set the popup window to center
          $(id).css('top',  winH/2-$(id).height()/2);
          $(id).css('left', winW/2-$(id).width()/2);
    
          //transition effect
          $(id).fadeIn(2000);
    
     });
    
     //if mask is clicked (outside of modal window)
     $('#mask').click(function () {
          $(this).hide();
          $('.window').hide();
     });              

     $(window).resize(function () {
     
        var box = $('#boxes .window');
        var maskHeight = $(document).height();
        var maskWidth = $(window).width();
     
        $('#mask').css({'width':maskWidth,'height':maskHeight});
        var winH = $(window).height();
        var winW = $(window).width();

        //Set the popup window to center
        box.css('top',  winH/2 - box.height()/2);
        box.css('left', winW/2 - box.width()/2);
     });
});
