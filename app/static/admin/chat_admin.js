window.onload = function() {
  $("#messages").scrollTop($('#messages')[0].scrollHeight);
  var socket = io.connect('//' + document.domain + ':' + location.port, {transports: ['websocket']});

  socket.on('connect', function(){socket.emit('admin/joined', {chat_id: chat_id})});
  socket.on('message', function(data){render_message(data);});

  $('#text').keypress(function(e) {
    var code = e.keyCode || e.which;
    if (code == 13) {
      submit_message($('#text').val());
    }
  });

  $("#send").click(function() {
    submit_message($('#text').val());
  });

  function submit_message(text) {
    $('#text').val('');
    socket.emit('admin/text', {body: text, chat_id: chat_id});
  }
};

function render_message(data) {
  document.getElementById("messages").insertAdjacentHTML('beforeend', getMessageString(data));
  $("#messages").scrollTop($('#messages')[0].scrollHeight);
}

function getMessageString(data){
  let photo, name, text, time
  if(data.role == 'USER'){
    photo = '<div class="sup-message-user-photo"> <img src="' + data.avatar + '" width="50px" height="50px"> </div>';
    name = '<div class="sup-message-name"> ' + data.nickname + ' </div>';
    text = '<div class="sup-message-block">' + data.message + '</div>';
    time = '<div class="sup-message-time">' + data.created + '</div>';
    return '<div class="sup-message">' + photo + '<div class="sup-message-body">' + name + text + time + '</div></div>';
  }else{
    photo = '<div class="my-message-user-photo"> <img src="' + data.avatar + '" width="50px" height="50px"> </div>';
    name = '<div class="my-message-name"> ' + data.nickname + ' </div>';
    text = '<div class="my-message-block">' + data.message + '</div>';
    time = '<div class="my-message-time">' + data.created + '</div>';
    return '<div class="my-message">' + photo + '<div class="my-message-body">' + name + text + time + '</div></div>';
  }
}