//Enable pusher logging - don't include this in production
/*
Pusher.log = function(message) {
    if (window.concole && window.console.log) {
	window.console.log(message); // command that allows us to print out something.
    }
};
*/
$(function() {
    // var pusher = new Pusher(PUSHER_KEY),
    // 	testChannel = pusher.subscribe('test_channel'),
    // 	broadcast = pusher.subscribe('br'),
    // 	$window = $(window),
    var $window = $(window),
	$usernameInput = $('.usernameInput[name=username]'),
	$messages = $('.messages'), // new jQuery object having class 'messages'
        $inputMessage = $('.inputMessage'),
	$loginPage = $('.login.page');
        $chatPage = $('.chat.page');

    // var username;
    var username,
	connected = false,
	typing = false,
	lastTypingTime;

    var user_id = (function () {
	var text = "";
	var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

	for (var i = 0; i < 10; i++)
	    text += possible.charAt(Math.floor(Math.random() * possible.length));

	return text;
    })();

    $usernameInput.focus();
    
    /*
    //$.post는 아래의 형태와 같습니다. 
    $.ajax({
        type: "POST",
	url: url,
	data: data, 
	success: success,
	dataType: dataType
    });
    */
    
    // broadcast.bind('new_message', function(data) {
    // 	// data['username'] = "Dongwoo";
    // 	addChatMessage(data);
    // });

    function startPusher() {
	var pusher = new Pusher(PUSHER_KEY),
	    testChannel = pusher.subscribe('test_channel'),
	    broadcast = pusher.subscribe('br');

	broadcast.bind('new_message', function(data) {
	    addChatMessage(data);
	});

	broadcast.bind('user_joined', function(data) {
	    log(data.username + ' joined');
	});

	broadcast.bind('typing', function(data) {
	    if (data['user_id'] == user_id) return;
	    addChatTyping(data);
	});

	//Whenever the server emits 'stop typing', kill the typting message
	broadcast.bind('stop_typing', function(data) {
	    if (data['user_id'] == user_id) return;
	    removeChatTyping(data);
	});
    }

    // window.console.log("2asdfasdfasdf");
    
    function addChatMessage(data) {
	var $usernameDiv = $('<span class="username"></span>');
	$usernameDiv.css("color", getUsernameColor(data.username));
	$usernameDiv.text(data.username);

	var $messageBodyDiv = $('<span class="messageBody"></span>');
	$messageBodyDiv.text(data.message);

	var typingClass = data.typing ? 'typing' : '';
	var $messageDiv = $('<li class="message ' + typingClass + '"></li>');
	$messageDiv.append($usernameDiv)
	    .append($messageBodyDiv)
	    .data('username', data.username);

	if (data.typing) {
	    $messageDiv.hide().fadeIn(150);
	}
	
	addMessageElement($messageDiv);
    }

    function addMessageElement(el) {
	var $el = $(el);
	$messages.append($el);

	$messages[0].scrollTop = $messages[0].srollHeight;

    }

    function getUsernameColor(username) {
	// Compute hash code
	var hash = 7;
	for (var i = 0; i < username.length; i++) {
	    hash = username.charCodeAt(i) + (hash << 5) - hash;
	}

	// Calculate color
	var index = Math.abs(hash % 360);
	return "hsl(" + index + ", 77%, 60%)";
    }

    function sendMessage () {
	var message = $inputMessage.val().trim();

	// if ther is a non-empty message
	if (message) {
	    $inputMessage.val('');
	    // $.post('/api/echo', {"message": message});
	    $.post('/api/call/new_message', {
		"message": message,
		"username": username
	    });
	}
    }

    function setUsername() {
	var __username = $usernameInput.val().trim();

	// If the username is valid
	if (__username) {
	    // username = __username;
	    // $loginPage.fadeOut();
	    // $chatPage.show();
	    // $inputMessage.focus();
	    $.post("/api/start", {
		'username': __username,
		'user_id': user_id,
	    }, function(data) {
		if (data.status == 0) {
		    username = __username;
		    $loginPage.fadeOut();
		    $chatPage.show();
		    $inputMessage.focus();

		    startPusher();
		    connected = true;
		    // Display the welcome message
		    var message = "Welcome to Chat &mdash; ";
		    log(message);
		} else {
		    alert("error");
		}
	    }, "json"
          );
	}
    }
    
    function log(message, options) {
	var el = '<li class="log">' + message + '</li>';
	addMessageElement(el, options);
    }

    // typing methods
    function addChatTyping(data) {
	data.typing = true;
	data.message = 'is typing';
	$('.typing.message').remove();
	addChatMessage(data);
    }

    function removeChatTyping(data) {
	$('.typing.message').fadeOut(function() {
	    $(this).remove();
	});
    }

    function updateTyping() {
	var TYPING_TIMER_LENGTH = 400; // ms
	if (connected) {
	    if (!typing) {
		typing = true;
		$.post('/api/call/typing');
	    }
	    lastTypingTime = (new Date()).getTime();

	    setTimeout(function(){
		var typingTimer = (new Date()).getTime();
		var timeDiff = typingTimer - lastTypingTime;
		if (timeDiff >= TYPING_TIMER_LENGTH && typing) {
		    $.post('/api/call/stop_typing');
		    typing = false;
		}
	    }, TYPING_TIMER_LENGTH);
	}
    }
    	
    $window.keydown(function(event) {
	// When the client has ENTER on their keyboard
	if (event.which == 13) {
	    // sendMessage();
	    if (username) {
		sendMessage();
	    } else {
		setUsername();
		$usernameInput.blur();
	    }
	}
    });

    $inputMessage.on('input', function() {
	updateTyping();
    });
});
