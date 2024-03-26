$(document).ready(function() {
    $(".addc").hide();
    $(".product-cover").mouseover(function() {
      $(this).find(".addc").stop().fadeIn(function() {
        // Optional code to run after fade-in completes
      });
    });
    $(".product-cover").mouseout(function() {
      $(this).find(".addc").stop().fadeOut(function() {
        // Optional code to run after fade-out completes
      });
    });
  });
  