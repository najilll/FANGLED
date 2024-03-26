$(document).ready(function () {
    $(".cart-add-btn").click(function () {
            var product_Id = $(this).data("product_id");
            var url = "/cart/add/?product_id="+product_Id; 
            var qty_value = $("#quantity-" + product_Id);
            var total_amt = $("#total-" + product_Id);
            console.log(product_Id)
            $.ajax({
                type: "GET",
                url: url,
                
                success: function (data) {
                  qty_value.val(data.quantity);
                  total_amt.text("₹"+data.total_price);
                  
                  $('#cart_total').html("₹"+data.cart_total);
                },
                error: function (data) {
                    // Display error message
                    console.log("error")
                }
            });
        });
        $(".cart-minus-btn").click(function () {
            var product_Id = $(this).data("product_id");
            var url = "/cart/minus/?item_id=" + product_Id;
            var qty_value = $("#quantity-" + product_Id);
            var total_amt = $("#total-" + product_Id);
            var total_mob = $("#total-mobile-" + product_Id);
    
            $.ajax({
                type: "GET",
                url: url,
                success: function (data) {
                //   if (data.quantity == '1') {window.location.reload()}
                  qty_value.val(data.quantity);
                  total_amt.text("₹"+data.total_price);
                  $('#cart_total').html("₹"+data.cart_total);
                  sub_total = parseFloat(data.cart_total);
                  $("#sub_total").text("₹"+sub_total.toFixed(2));
                  total_mob.text("₹"+data.total_price);
                  console.log("success")
    
                  
                    
                },
                error: function (data) {
                    // Display error message
                    console.log("error")
                }
            });
        });
})