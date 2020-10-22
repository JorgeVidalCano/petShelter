$(document).ready(function () {
  var c = 1;
  let end = false
  let call = true;
  
  $(window).on("scroll", function(){
      if(call == true){
          if( $(this).scrollTop() > ($(document).height()*0.65).toFixed(0) & end == false) {
              call = false;
              c ++
              var $endpoint = window.location.origin + "/lazyReload/" + c + window.location.href.slice(window.location.origin.length, -1)
              var $formData = $(this).serialize();

              $.ajax({
                method: "GET",
                url: $endpoint,
                data: $formData,
                success: handleFormSuccess,
                error: handleFormError,
              })
              
              function handleFormSuccess(data, textStatus, jqXHR){
                
                var instance = JSON.parse(data["instance"]);

                }
                call=true
              }
      function handleFormError(data, textStatus, errorThrown){
        console.log(data)
        console.log(textStatus)
        console.log(errorThrown)
      }
    }}
  )
})