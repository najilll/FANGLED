$(document).ready(function() {
    let qty = 1;
    $(".detail-qty-input").attr("value", qty);
    $("#detail-decrement").click(function() {
        if(qty >= 2){
            qty--;
            $(".detail-qty-input").attr("value", qty);
        }
    })
    $("#detail-increment").click(function() {
        qty++;
        $(".detail-qty-input").attr("value", qty);
    })
})