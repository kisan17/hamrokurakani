var socket = io.connect('http://' + document.domain + ':' + location.port + '/chatwith');
// get current user profileimage
var currentUserImg = $('img#profile-img').attr('src');

$(document).ready(function () {

  socket.on('connect', function () { socket.emit('joined', {}); });

  //? scroll to the last message and focus on the message input
  $(".messages").scrollTop($(".messages")[0].scrollHeight);
  $('#message').val('').focus();


  //? If i press send button the message is also sent
  $('#sendmessage').on('click', function () {
    var text = $('#message').val();
    var type = 'sent';
    if (text !== "") {
      $('#message').val('').focus();
      var type = messageSender(text);
      socket.emit('text', { msg: text, type: type });
    }
  });

  //? If i press enter the message is also sent
  $('#message').keypress(function (e) {
    var code = e.keyCode || e.which;
    if (code == 13) {
      var text = $('#message').val();
      if (text !== "") {
        $('#message').val('').focus()
        var type = messageSender(text);
        socket.emit('text', { msg: text, type: type });
      }
    }
  });

  socket.on('message', function (data) {
    if (data.msg !== "") {
      var replies = `<li class='sent'><img src=${currentUserImg}><p>`;
      $(replies + data.msg + '</p></li>').appendTo($('.messages ul'));
      $('.contact.active .preview').html('<span>' + data.msg + '</span>');
      $(".messages").animate({ scrollTop: $(".messages")[0].scrollHeight }, "fast");
    }
  });
});

function messageSender(text) {
  var replies = `<li class='replies'><img src=${currentUserImg}><p>`;
  var type = $(replies + text + '</p></li>').appendTo($('.messages ul'));
  $('.contact.active .preview').html('<span>You: </span>' + text);
  $(".messages").animate({ scrollTop: $(".messages")[0].scrollHeight }, "fast");
  return type;
}

function leave_room() {
  socket.emit('left', {}, function () {
    socket.disconnect();
  });
}

function set_message_count(n) {
  $('#message_count').text(n);
  $('#message_count').css('visibility', n ? 'visible' : 'hidden');
}


$(document).ready(function () {
  $("#exit").click(function () {
    leave_room();
  });
});
