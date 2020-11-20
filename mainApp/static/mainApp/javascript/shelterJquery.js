$(document).ready(function () {
    var c = 1;
    let end = false
    let call = true;
    
    $(window).on("scroll", function(){
        if(call == true){
            if( $(this).scrollTop() > ($(document).height()*0.20).toFixed(0) & end == false) {
                call = false;
                c ++
                var $endpoint = window.location.origin + "/lazyReload/shelters/" + c 
                console.log(document.getElementsByClassName("removeHoverLink").attr("href"))
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
                  end = JSON.parse(data["end"]);
                  for ( var i = 0; i < instance.length; i++){
                    
                    var results = $(` <a class="removeHoverLink" href="${instance[i].slug}">
                                        <div class="row my-4 p-2 border box-shadow">
                                            <div class="col-md-7">
                                                <img id="pet-image-card" class="img-fluid rounded mb-3 mb-md-0" src="${instance[i].image}" alt="${instance[i].name}">
                                            </div>
                                            <div class="col-md-5">
                                                <h3 class="h3 text-primary">${instance[i].name}</h3>
                                                <p>${instance[i].about}</p>
                                                <p>Location: ${instance[i].location}</p>
                                                <p>It holds ${instance[i].petAdoption} animals.</p>
                                            </div>
                                        </div>
                                    </a>`);
                  $(".removeHoverLink").last().append($(results));
                  }
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