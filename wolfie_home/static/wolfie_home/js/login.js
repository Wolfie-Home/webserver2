$(document).ready(function() {
    console.log('ready');

    var login_btn = $('#login_btn');
    login_btn.click(function(event) {
	console.log('button is clicked');
	var username = $('#username').val();
	var password = $('#password').val();
	var req = {
	    'username': username,
	    'password': password
	};

	console.log(req);	// for debug
	$.post('/api/login', req).always(function(jqxhr, status) {
	    if (jqxhr.status == 301) {
		console.log('login success');
		// how it is time go to the house page
		window.location.replace('house');
	    }
	});
    });
    
});
