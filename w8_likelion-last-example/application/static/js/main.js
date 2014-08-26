//Enable pusher logging - don't include this in production
/*
Pusher.log = function(message) {
    if (window.concole && window.console.log) {
	window.console.log(message); // command that allows us to print out something.
    }
};
*/
$(function() {
    var pusher = new Pusher(PUSHER_KEY),
	testChannel = pusher.subscribe('test_channel'),
	broadcast = pusher.subscribe('br'),
	$window = $(window),
	$messages = $('.messages'), // new jQuery object having class 'messages'
        $inputMessage = $('.inputMessage'),
        chatPage = $('.chat.page');

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
    var initial_delay = 1500;
    setTimeout(function () {
	addChatMessage({'username': 'Duhee', 'message': 'Hello!'});
    }, initial_delay + 500)
    setTimeout(function () {
	addChatMessage({'username': 'Jinho', 'message': 'Hello!'});
    }, initial_delay + 1000)
    setTimeout(function () {
	addChatMessage({'username': 'Jinho', 'message': 'Hey Duhee, I heard that you are practicing crying selfie.'});
    }, initial_delay + 1500)
    setTimeout(function () {
	addChatMessage({'username': 'Duhee', 'message': '??????!!!!!!!!!!!!'});
    }, initial_delay + 2000)

    // window.console.log("1asdfasdf");
    
    // testChannel.bind('echo', function(data) {
    broadcast.bind('new_message', function(data) {
	data['username'] = "Dongwoo";
	addChatMessage(data);
    });

    // window.console.log("2asdfasdfasdf");
    
/*    setTimeout(function () {
	// window.console.log("asdf");
	$.post('/api/echo', {"message": "Hello World!"});
    }, initial_delay + 4000)
    setTimeout(function () {
	$.post('/api/echo', {"message": "I'd like to have a fried chicken."});
    }, initial_delay + 5000)
    setTimeout(function () {
	$.post('/api/echo', {"message": "When is it comming? Isn't it arrived yet?"});
    }, initial_delay + 6000)
    setTimeout(function () {
	$.post('/api/echo', {"message": "Hey Duhee bro! Please let me have some fried chicken!"});
    }, initial_delay + 7000)
*/
    // window.console.log("3asdfasdf"); 
    
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
	    $.post('/api/call/new_message', {"message": message});
	}
    }

    $window.keydown(function(event) {
	// When the client has ENTER on their keyboard
	if (event.which == 13) {
	    sendMessage();
	}
    });
});
