function cj_redirect(message, message_type) {
    var get_req = 'message?message=' + message + 
	'&message_type=' + message_type;
    window.location.replace(get_req);
}


$(document).ready(function() {
    console.log('ready');

    // so many hacks just to achieve one thing: make a shared object
    // visible to some callback functions.... javascript...
    window.myglb = {}

    var get_house_info_cb = function(data,status) {
	// let's say it failed
	console.log(data);
	window.myglb['house_info'] = JSON.parse(data)
	console.log(window.myglb['house_info']);
	create_tables();
    };


    var get_house_info_fail_cb = function(jqxhr) {
	// let's say it failed
	console.log('failed to get_house_info');
	console.log(jqxhr);
	jjjjjjjjjjjjjjjjjjj();	// abort
    };

    var module_success_cb = function(data) {
	// building table
	console.log(data);
	$('body').append(data+'<br>');
    };

    var module_failed_cb = function(data) {
	console.log(data);
	jjjjjjjjjjjjjjjjjjj();	// abort
    };

    var module_failed_unknown_cb = function(jqxhr) {
	console.log(jqxhr);
	jjjjjjjjjjjjjjjjjjjj();
    };

    var create_table = function(mod_type, uid) {
	req = {
	    'command': 'get_module_recent',
	    'module_uids': uid+'',
	    'modules': mod_type+''
	};
	console.log(req);
	var ajax_module = {
	    'url': 'api/module',
	    'data': req,
	    'statusCode': {
		200: module_success_cb,
		400: module_failed_cb
	    },
	    'error': module_failed_unknown_cb,
	    'method': 'POST'
	};
	$.ajax(ajax_module);
    };

    var create_tables = function() {
	console.log(window.myglb['house_info']);
	var house_info = window.myglb['house_info'];
	for (var i = 0; i < house_info['mod_list'].length; ++i) {
	    var mod = house_info['mod_list'][i];
	    create_table(mod['module'], mod['uid']);
	}
    };

    // main
    var ajax_house = {
	'url': 'api/house',
	'statusCode': {
	    200: get_house_info_cb
	},
	'error': get_house_info_fail_cb,
	'method': 'POST'
    };
    $.ajax(ajax_house)

});
