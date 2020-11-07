//show the delete button
$(document).ready(function(){
    var $deleteButton = $(".deleteImg")
    $deleteButton.hover(function(event){
      $(this).find(".deleteImg").show();
    })
    $deleteButton.mouseleave(function(event){
      $(this).find(".deleteImg").hide();
    })
  }
  )