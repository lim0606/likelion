//Enable pusher logging - don't include this in production
/*
Pusher.log = function(message) {
    if (window.concole && window.console.log) {
	window.console.log(message); // command that allows us to print out something.
    }
};
*/

function toggleGlobalLoadingIndicator() {
    var spinner_el = $(".spinner");
    
    if (spinner_el.length == 0) {
	var opts = {
	    lines: 13, // The number of lines to draw
	    length: 20, // The length of each line
	    width: 10, // The line thickness
	    radius: 30, // The radius of the inner circle
	    corners: 1, // Corner roundness (0..1)
	    rotate: 0, // The rotation offset
	    direction: 1, // 1: clockwise, -1: counterclockwise
	    color: '#000', // #rgb or #rrggbb or array of colors
	    speed: 1, // Rounds per second
	    trail: 60, // Afterglow percentage
	    shadow: false, // Whether to render a shadow
	    hwaccel: false, // Whether to use hardware accel
	    className: 'spinner', // The CSS class to assign to the spinner
	    zIndex: 2e9, // The z-index (default to 2000000000)
	    top: '50%', // Top position relative to parent
	    left: '50%' // Left position relative to parent
	};
	// window.console.log("opts success!");
	
	$("body").prepend("<div id='spinner-container' style='position: fixed; top: 0; right: 0; bottom: 0; z-index:9999; overflow: hidden; outline: 0; color: #333; background-color: gray; opacity: 0.8;'></div>");
	// window.console.log("prepend success!");
	
	var spinner = new Spinner(opts).spin($("#spinner-container")[0]);
	// window.console.log("spinner object!");
    } else {
	$("#spinner-container").toggleClass("display-none");
    }
}

$(function() {
    // var pusher = new Pusher(PUSHER_KEY),
    // 	testChannel = pusher.subscribe('test_channel'),
    // 	broadcast = pusher.subscribe('br'),
    // 	$window = $(window),
    var $window = $(window),
	$usernameInput = $('.usernameInput[name=username]'),
        $passwordInput = $('.usernameInput[name=password]'),
	$messages = $('.messages'), // new jQuery object having class 'messages'
        $inputMessage = $('.inputMessage'),
	$loginPage = $('.login.page'),
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
	window.console.log(text);
	return text;
    })();

    $usernameInput.focus();
    
    // //$.post는 아래의 형태와 같습니다. 
    // $.ajax({
    //     type: "POST",
    // 	url: url,
    // 	data: data, 
    // 	success: success,
    // 	dataType: dataType
    // });
    
    // broadcast.bind('new_message', function(data) {
    // 	// data['username'] = "Dongwoo";
    // 	addChatMessage(data);
    // });

    function startPusher() {
	window.console.log("pusherkey!!!")
	window.console.log(PUSHER_KEY);
	
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

    function sendMessage() {
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
	var __password = $passwordInput.val().trim();
	window.console.log("asdfasdf!!asdf");
	// If the username is valid
	if (__username && __password) {
	    toggleGlobalLoadingIndicator();
	    window.console.log("whatthe!!");
	    var setuser_post = $.post("/api/trylogin", {
		'username': __username, 
		'password': __password,
		'user_id': user_id,
	    }, function(data) {
		if (data.status == 0) {
		    username = __username;
		    window.console.log(__username); 
		    $loginPage.fadeOut();
		    $chatPage.show();
		    $inputMessage.focus();

		    startPusher();
		    connected = true;
		    // Display the welcome message
		    var message = "Welcome to Chat &mdash; ";
		    log(message);
		} else {
		    alert("fail to login");
		}
	    }, "json"
		  );//.always(funtion() {
	      // toggleGlobalLoadingIndicator();
	      //});
	    setuser_post.always(function() {
		toggleGlobalLoadingIndicator();
	    });
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

