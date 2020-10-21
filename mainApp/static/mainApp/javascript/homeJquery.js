$(document).ready(function () {
  var c = 1;
  let end = false
  let call = true;
  
  $(window).on("scroll", function(){
      console.log($(this).scrollTop())
      console.log($(document).height()*0.65)
      if(call == true){
          if( $(this).scrollTop() > ($(document).height()*0.65).toFixed(0) & end == false) {
              call = false;
              c ++
              alert(window.location.origin + "/lazyReload/" + c + window.location.href.slice(window.location.origin.length, -1))      
    //   var $formData = $(this).serialize();
    //   var $endpoint = window.location.origin + "/lazyReload/" + c + window.location.href.slice(window.location.origin.length, -1)
    //   $.ajax({
        // method: "GET",
        // url: $endpoint,
        // data: $formData,
        // success: handleFormSuccess,
        // error: handleFormError,
    //   })

      function handleFormSuccess(data, textStatus, jqXHR){

    //   var instance = JSON.parse(data["instance"]);
      
    //   end = JSON.parse(data["end"]);
      
    //   for ( var i = 0; i < instance.length; i++){      
    //     var tags ='';
    //     $.each(instance[i].tags, function(index, v){
    //       tags += `<span class="badge badge-warning">${v}</span>`
    //     });
        
    //     var results = $(`
    //                     <div class="card mb-4">
    //                       <img class="border card-img-top" src="${ instance[i].image }" alt="Card image cap">
    //                       <div class="card-body">
    //                           <h2 class="card-title">${ instance[i].title }</h2>
    //                           ${tags}
    //                           <hr>
    //                           <p class="card-text">${ instance[i].content.split(/\s+/).slice(0,35).join(" ") }</p>
    //                           <a href="/post/${ instance[i].slug }" class="btn btn-primary">Read More &rarr;</a>
    //                       </div>
    //                       <div class="card-footer text-muted">
    //                       Posted on ${ instance[i].datePosted } by <span class="text-primary">@${ instance[i].author }</span>
    //                       </div>
    //                     </div>
    //       `);
    //   $(".col-md-8").append( $(results));
    //   }
    //   call=true
      
      }
      function handleFormError(data, textStatus, errorThrown){
        console.log(data)
        console.log(textStatus)
        console.log(errorThrown)
      }
    }}
  }
  )
})