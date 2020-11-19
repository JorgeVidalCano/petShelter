// Adds a comment in the petDetail page
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
      
      var successMessage = $(`<div class="alert alert-success fade show" role="alert">
                                Message sent
                              <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                                <span aria-hidden="true">&times;</span>
                              </button>
                              </div>`)
      $("#commentPet").remove();
      $(".special-width").prepend($(successMessage));
    }
    function handleFormError(data, textStatus, errorThrown){
      console.log(data)
      console.log(textStatus)
      console.log(errorThrown)
    }
  })
 }
)
  
// Selects a chatroom in the board and show the messages
$(document).ready(function () {
  var $chatRoom = $(".chatRoom")
  $chatRoom.click(function(event){
    event.preventDefault();
    var $formData = $(this).serialize();
    var $endpoint = window.location.origin + $(this).attr("href") || window.location.href
    $(".activeChatRoom").removeClass("activeChatRoom");
    $(this).addClass("activeChatRoom");
    $.ajax({
      method: "GET",
      url: $endpoint,
      data: $formData,
      success: handleFormSuccess,
      error: handleFormError,
    })
    function handleFormSuccess(data, textStatus, jqXHR){
      console.log(textStatus)
      console.log(jqXHR)
      
      $(".comment").remove(); // deletes the last conversation
      $(".commentForm").remove(); // deletes the form
      
      var message = JSON.parse(data["messages"]);
      // Months go from 0 to 11, so it needs a +1
      for (var i = 0; i < message.length; i++){
        var d = new Date(message[i]['fields'].date_created)
        if(data["user_id"] == message[i]['fields'].sender){
          var result = $(`<div class="comment media w-50 ml-auto mb-3">
                            <div class="media-body">
                              <p class="small font-weight-bold">You</p>
                                <div class="bg-primary rounded py-2 px-3 mb-2">
                                  <p class="text-small mb-0 text-white">${message[i]['fields'].message}</p>
                                </div>
                              <p class="small text-muted">${ d.getHours()}:${d.getMinutes()} ${d.getDate()}/${d.getMonth()+1}/${d.getFullYear()}</p>
                              </div>
                            </div>
                        `);
        }else{
          var result = $(`<div class="comment media w-50 mb-3">
                            <div class="media-body ml-3">
                              <p class="small text-muted font-weight-bold">${ data["user_sender"] } </p>
                              <div class="bg-light rounded py-2 px-3 mb-2">
                                <p class="text-small mb-0 text-muted">${message[i]['fields'].message}</p>
                              </div>
                              <p class="small text-muted">${ d.getHours()}:${d.getMinutes()} ${d.getDate()}/${d.getMonth()+1}/${d.getFullYear()}</p>
                            </div>
                          </div>
                          `);
        }
        $("#message").prepend($(result))
      }
      var form = $(`<div class="commentForm input-group">
                      <textarea name="message" cols=30 rows=3 placeholder="Type a message" aria-describedby="button-addon2" class="form-control rounded-0 border-0 py-4 bg-light"></textarea>
                      <div class="input-group-append">
                        <button id="button-addon2" type="submit" class="btn btn-link"> <i class="fa fa-paw"></i></button>
                      </div>
                    </div>`)
      $("#answerForm").append($(form)) 
      
      $("#answerForm").attr("data-url", data["newMessageUrl"])
      $("#message").scrollTop($("#message").height());
    }
    function handleFormError(data, textStatus, errorThrown){
      console.log(data)
      console.log(textStatus)
      console.log(errorThrown)
    }
  })
 }
)

// Creates a new comment in the board page
$(document).ready(function () {
  var $form = $("#answerForm")
  $form.submit(function(event){
    
    console.log($form)
    event.preventDefault();
    var $formData = $(this).serialize();
    var $endpoint = window.location.origin + $form.attr("data-url") || window.location.href
    
    $.ajax({
      method: "POST",
      url: $endpoint,
      data: $formData,
      success: handleFormSuccess,
      error: handleFormError,
    })

    function handleFormSuccess(data, textStatus, jqXHR){
      console.log(textStatus)
      console.log(jqXHR)
      $form[0].reset();

      console.log(data['message']);
      if (data['message'] != null){
      var result = $(`<div class="comment media w-50 ml-auto mb-3">
                        <div class="media-body">
                          <p class="small font-weight-bold">You</p>
                            <div class="bg-primary rounded py-2 px-3 mb-2">
                              <p class="text-small mb-0 text-white">${data['message']}</p>
                            </div>
                          <p class="small text-muted">Now</p>
                          </div>
                        </div>
                    `).hide();
      $("#message").append($(result));
      $(result).fadeIn(800);
      $("#message").scrollTop($("#message").height());
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