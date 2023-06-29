
  $(document).ready(function () {

    $('.payWithRazorpay').click(function (e) {
      e.preventDefault();

      var fname = $("[name='first_name']").val()
      var phone = $("[name='phone']").val()
      var email = $("[name='email']").val()
      var token = $("[name='csrfmiddlewaretoken']").val()
      var selectedAddress = $("input[name='delivery_address']:checked").val();
      if(!selectedAddress)
      {
        swal("Alert!", "Address field is mandatory!", "error");
        console.log('All fields are empty');
        return false;

      }
      else
      {
        $.ajax({
           method:"GET",
           url:"{% url 'proceedtopay' %}",
           success: function(response) {
            var options = {
              console.log(response),
              "key": "rzp_test_x2O5Zk54HJvUOv", // Enter the Key ID generated from the Dashboard
              "amount": response.total_price*100,//response.total_price * 100, // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
              "currency": "INR",
              "name": "E-BUDS",
              "description": "Thank you for buying with us",
              "image": "https://example.com/your_logo",
              //"order_id": "order_IluGWxBm9U8zJ8", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
              "handler": function (responseb){
                alert(responseb.razorpay_payment_id);
                  data = {
                    
                    "payment_method" : "Razorpay",
                    "payment_id" : responseb.razorpay_payment_id,
                    "address": selectedAddress,
                    csrfmiddlewaretoken: token
                    
                  }
                    $.ajax({
                      method:"POST",
                      url:"/checkout/placeorder/",
                      data: data,
                      success: function (responsec) {
                        console.log(responsec)
                        swal("Congratulations!", responsec.status,"success").then((value) => {
                            window.location.href = '/orders/'
                        });
                      }

                  });
              },
              "prefill": {
                  "name": fname,
                  "email" : email,
                  'contact' : phone,
              },
              
              "theme": {
                  "color": "#3399cc"
              }
          };
          var rzp1 = new Razorpay(options);
          rzp1.on('payment.failed', function (response){
                  alert(response.error.code);
                  alert(response.error.description);
                  alert(response.error.source);
                  alert(response.error.step);
                  alert(response.error.reason);
                  alert(response.error.metadata.order_id);
                  alert(response.error.metadata.payment_id);
          });
          rzp1.open();
            console.log(responsec);

           }
        });
        
 
      }





      
    });

  });

 

 