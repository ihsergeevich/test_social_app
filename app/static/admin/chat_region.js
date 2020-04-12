window.onload = function() {
  $("#messages").scrollTop($('#messages')[0].scrollHeight);
  var socket = io.connect('//' + document.domain + ':' + location.port, {transports: ['websocket']});

  socket.on('connect', function(){socket.emit('region/joined', {region_id: region_id})});
  socket.on('message', function(data){render_message(data)});
  socket.on('delete', function(data){delete_message(data)});

  $('#text').keypress(function(e) {
    var code = e.keyCode || e.which;
    if (code == 13) {
      submit_message($('#text').val());
    }
  });

  $("#send").click(function() {
    submit_message($('#text').val());
  });

  $(".message-delete").click(function() {
    message_id = $(this).parent().parent().attr('message_id');
    socket.emit('region/delete', {message_id: message_id, region_id: region_id})
  });

  function submit_message(text) {
    $('#text').val('');
    socket.emit('region/text', {body: text, region_id: region_id});
  }
};

function render_message(data) {
  document.getElementById("messages").insertAdjacentHTML('beforeend', getMessageString(data));
  $("#messages").scrollTop($('#messages')[0].scrollHeight);
}

function delete_message(data) {
  $("div[message_id='" + data.message_id + "']").remove();
}

function getMessageString(data){
  let photo, name, text, time;
  let message_id = data.id;
  let message_delete = '<div class="message-delete" style="color:red; cursor:pointer;">Удалить</div>';
  if(data.user_id == user_id){
    photo = '<div class="my-message-user-photo"> <img src="' + data.avatar + '" width="50px" height="50px"> </div>';
    name = '<div class="my-message-name"> ' + data.nickname + ' </div>';
    text = '<div class="my-message-block">' + data.message + '</div>';
    time = '<div class="my-message-time">' + data.created + '</div>';
    return '<div class="my-message"' + message_id + '>' + photo + '<div class="my-message-body">' + name + text + message_delete + time + '</div></div>';
  }else{
    photo = '<div class="sup-message-user-photo"> <img src="' + data.avatar + '" width="50px" height="50px"> </div>';
    name = '<div class="sup-message-name"> ' + data.nickname + ' </div>';
    text = '<div class="sup-message-block">' + data.message + '</div>';
    time = '<div class="sup-message-time">' + data.created + '</div>';
    return '<div class="sup-message"' + message_id + '>' + photo + '<div class="sup-message-body">' + name + text + message_delete + time + '</div></div>';
  }
}