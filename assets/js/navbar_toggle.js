// $(document).ready(function() {
//     let nav_status = false;
//     if(nav_status == false) {
//         $("#full-toggle-area").hide();
//     }
//     $("#nav-toggle").click(function() {
//         if(nav_status == true) {
//             $("#full-toggle-area").fadeOut(100);
//             nav_status = false;
//         }
//         else if(nav_status == false) {
//             $("#full-toggle-area").fadeIn(100);
//             nav_status = true;
//         }
//     })
//     $("#nav-toggle-assist").click(function() {
//         $("#full-toggle-area").fadeOut(100);
//     })
// })

$(document).ready(function() {
    $("#full-toggle-area").hide();
    $(".nav-toggle").click(function() {
        $("#full-toggle-area").fadeIn(100);
    })
    $("#nav-toggle-assist").click(function() {
        $("#full-toggle-area").fadeOut(100);
    })
})