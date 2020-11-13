// Adds comments 
$(document).ready(function () {
    
    var $myForm = $("#commentPet")
    $myForm.submit(function(event){
      event.preventDefault();
      var $formData = $(this).serialize();
      var $endpoint = window.location.origin + $myForm.attr("data-url") || window.location.href
        
      $.ajax({
        method: "POST",
        url: $endpoint,
        data: $formData,
        success: handleFormSuccess,
        error: handleFormError,
      })
      function handleFormSuccess(data, textStatus, jqXHR){
        console.log(data)
        console.log(textStatus)
        console.log(jqXHR)
        $myForm[0].reset();
              
        var instance = JSON.parse(data["instance"]);
        var fields = instance[0]["fields"];

      }
      function handleFormError(data, textStatus, errorThrown){
        console.log(data)
        console.log(textStatus)
        console.log(errorThrown)
      }
    })
    }
  )
  
  