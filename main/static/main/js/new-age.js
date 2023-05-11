(function($) {
    "use strict"; // Start of use strict
  
    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function() {
      if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
        var target = $(this.hash);
        target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
        if (target.length) {
          $('html, body').animate({
            scrollTop: (target.offset().top - 48)
          }, 1000, "easeInOutExpo");
          return false;
        }
      }
    });
  
    // Closes responsive menu when a scroll trigger link is clicked
    $('.js-scroll-trigger').click(function() {
      $('.navbar-collapse').collapse('hide');
    });
  
    // Activate scrollspy to add active class to navbar items on scroll
    $('body').scrollspy({
      target: '#mainNav',
      offset: 54
    });
  
    // Collapse Navbar
    var navbarCollapse = function() {
      if ($("#mainNav").offset().top > 100) {
        $("#mainNav").addClass("navbar-shrink");
      } else {
        $("#mainNav").removeClass("navbar-shrink");
      }
    };
    // Collapse now if page is not at top
    navbarCollapse();
    // Collapse the navbar when page is scrolled
    $(window).scroll(navbarCollapse);
  
  })(jQuery); // End of use strict
  
  
  $(window).scroll(function() {
    if ($(window).scrollTop() > 10) {
        $('#mainNav').addClass('floatingNav');
    } else {
        $('#mainNav').removeClass('floatingNav');
    }
  });

function animateRows(){
  $("#img_row1").animate({left: "-50px"});
  console.log("I'm Moving");
}

$(window).scroll(function() {
  var scrollTop = $(window).scrollTop();
  console.log("scrollTop>>>" + scrollTop);
  var scroll_to_mentor_showoff = $('#mentor-showoff').offset().top;
  var scroll_to_what_is = $('#what-is').offset().top;
  console.log("hello "+scroll_to_mentor_showoff);
  if (scrollTop < scroll_to_mentor_showoff) {
   $("#img_col1").css({"margin-top": "40px"});    
   $("#img_col2").css({"margin-top": "0px"});    
   $("#img_col3").css({"margin-top": "40px"});    
   $("#img_col4").css({"margin-top": "0px"});    
   $("#img_col5").css({"margin-top": "40px"});    
   $("#img_col6").css({"margin-top": "0px"});    
  } else if(scrollTop < scroll_to_what_is) {
   $("#img_col1").css({"margin-top":  40+(scroll_to_mentor_showoff-($(window).scrollTop()))/5 + "px"});    
   $("#img_col2").css({"margin-top":  (scroll_to_mentor_showoff-($(window).scrollTop()))/30 + "px"});    
   $("#img_col3").css({"margin-top":  40+(scroll_to_mentor_showoff-($(window).scrollTop()))/5 + "px"});    
   $("#img_col4").css({"margin-top":  (scroll_to_mentor_showoff-($(window).scrollTop()))/30 + "px"});    
   $("#img_col5").css({"margin-top":  40+(scroll_to_mentor_showoff-($(window).scrollTop()))/5 + "px"});    
   $("#img_col6").css({"margin-top":  (scroll_to_mentor_showoff-($(window).scrollTop()))/30 + "px"});    
  }
});