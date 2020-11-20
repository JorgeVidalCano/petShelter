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
                        <p class="card-text"><b>${ instance[i].name }</b></p>
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