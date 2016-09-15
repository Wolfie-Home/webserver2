$(document).ready(function() {
    console.log('ready');

    var login_btn = $('#login_btn');
    if (login_btn) {
        login_btn.click(function(event) {
            console.log('button is clicked');
            var username = $('#username').val();
            var password = $('#password').val();
            var req = {'username': username, 'password': password };
            $.post('/api/login', req).always(function(jqxhr, status) {
                if (status == "success") {
                    // how it is time go to the house page
                    window.location.replace('/index');
                }
            });
        });
    }

    var logout_btn = $('#logout_btn');
    if (logout_btn) {
        logout_btn.click(function(event) {
            $.post('/api/logout').always(function(jqxhr, status) {
                if (status == "success") {
                    // how it is time go to the house page
                    window.location.replace('/');
                }
            });
        });
    }
});