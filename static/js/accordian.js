$(document).ready(function() {
    let ac1 = false;
    let ac2 = false;
    let ac3 = false;
    let ac4 = false;
    if($(window).width() < 768) {
        $("#foot-1-desc").hide();
        $("#foot-2-desc").hide();
        $("#foot-3-desc").hide();
        $("#foot-4-desc").hide();
    }
    $(window).resize(function() {
        if($(window).width() < 768) {
            $("#foot-1-desc").hide();
            $("#foot-2-desc").hide();
            $("#foot-3-desc").hide();
            $("#foot-4-desc").hide();
        }
        else {
            $("#foot-1-desc").show();
            $("#foot-2-desc").show();
            $("#foot-3-desc").show();
            $("#foot-4-desc").show();
        }
    })
    $("#foot1-b").click(function() {
        if(ac1 == false) {
            $("#foot-1-desc").slideDown(200);
            ac1 = true
        }
        else {
            $("#foot-1-desc").slideUp(200);
            ac1 = false
        }
    })
    $("#foot2-b").click(function() {
        if(ac2 == false) {
            $("#foot-2-desc").slideDown(200);
            ac2 = true
        }
        else {
            $("#foot-2-desc").slideUp(200);
            ac2 = false
        }
    })
    $("#foot3-b").click(function() {
        if(ac3 == false) {
            $("#foot-3-desc").slideDown(200);
            ac3 = true
        }
        else {
            $("#foot-3-desc").slideUp(200);
            ac3 = false
        }
    })
    $("#foot4-b").click(function() {
        if(ac4 == false) {
            $("#foot-4-desc").slideDown(200);
            ac4 = true
        }
        else {
            $("#foot-4-desc").slideUp(200);
            ac4 = false
        }
    })
})