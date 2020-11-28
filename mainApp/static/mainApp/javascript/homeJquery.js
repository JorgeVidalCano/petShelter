/* Lazy load pets in home */ 
$(document).ready(function () {
  var c = 1;
  let end = false
  let call = true;
  
  $(window).on("scroll", function(){
      if(call == true){
          if( $(this).scrollTop() > ($(document).height()*0.20).toFixed(0) & end == false) {
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
                end = JSON.parse(data["end"]);
                for ( var i = 0; i < instance.length; i++){
                  console.log(instance[i].slug )
                  var results = $(`
                    <div class="col-lg-3 col-md-4 col-sm-6 col-xs-12 pet-card">
                    <a href="/${ instance[i].slug }" >
                    <div class="card mb-4 box-shadow">
                      <img id="pet-image-card" class="card-img-top" alt="${ instance[i].name }" src="${ instance[i].images}">
                      <div class="card-img-overlay">
                        <h3><span class="badge badge-primary ${ instance[i].status }">${ instance[i].status }</span></h3>
                      </div>
                      <div class="card-body">
                        <p class="card-text text-primary"><b>${ instance[i].name }</b></p>
                        <p class="card-text">Place ${ instance[i].shelter }</p>
                        <p class="card-text">Sex ${ instance[i].sex }</p>
                        <div class="d-flex justify-content-between align-items-center">
                          <small class="text-muted">${ instance[i].date_created }</small>
                        </div>
                      </div>
                    </div>
                  </div> 
                `);
                $(".general-row").last().append($(results));
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

// Search Bar
$(document).ready(function () {    
  var $myForm = $("#searchFormId")
  
  $myForm.on('change keyup',function(e){
      
      var $formData = $(this).serialize();
      var $endpoint = window.location.origin + "/search/ajaxSearch"
      
    $.ajax({
      method: "GET",
      url: $endpoint,
      data: $formData,
      success: handleFormSuccess,
      error: handleFormError,
    })

    function handleFormSuccess(data, textStatus, jqXHR){

    var instance = JSON.parse(data["instance"]);
    $(".searchResult").remove();
    for ( var i = 0; i < instance.length; i++){      
      var results = $(`
                      <div class="container border p-1 searchResult col-4">
                        <a href="/pet/${instance[i].slug}" class="removeHoverLink" /">
                          <div class="row top-buffer align-items-center flex-row-reverse">
                            <div class="col-lg-7 col-md-7 col-sm-12">
                                <h3 class="h4 text-primary">${instance[i].name}</h3>
                                <h6>Location: ${instance[i].location}</h6>
                            </div>
                            <div class="col-lg-5 col-md-5 align-items-center flex-row-reverse">
                                <img class="searchImg float-left " src="${instance[i].image}">
                            </div>
                          </div>
                        </a>
                      </div>
        `);
        $("#inputFormId").append(results);
      }
    }
    function handleFormError(data, textStatus, errorThrown){
      console.log(data)
      console.log(textStatus)
      console.log(errorThrown)
    }
  })
  }
)

$(document).ready(function () {    
  var $myForm = $("#searchFormId")
  
  $myForm.on('submit',function(e){
    e.preventDefault();

  })
  }
)

// $(document).ready(function () {
//   $("#inputFormId").focusout(function() {
//     // deletes the search if focus is lost
//     setTimeout(function() { 
//       $(".searchResult").remove();
//     }, 200); 
//   });
// })