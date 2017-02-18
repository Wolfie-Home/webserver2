$(document).ready(function() {
    console.log('ready');

    var login_btn = $('#login_btn');
    if (login_btn) {
        login_btn.click(function(event) {
            console.log('button is clicked');
            var username = $('#username').val();
            var password = $('#password').val();
            $.ajax({
                type: "POST",
                url: "/api/login",
                data: JSON.stringify({"username": username, "password": password}),
                contentType: "application/json",
                dataType: "json",
                success: function(jqXHR, textstatus) {
                    $('#msg').text(jqXHR["msg"]);
                    // how it is time go to the house page
                    window.location.replace('/index');
                },
                error: function(jqXHR, textstatus) {
                    $('#errmsg').text(jqXHR.responseJSON["errmsg"]);
                }
            });
        });
    }

    var logout_btn = $('#logout_btn');
    if (logout_btn) {
        logout_btn.click(function(event) {
            $.ajax({
                type: "POST",
                url: "/api/logout",
                data: '',   // No data
                contentType: "application/json",
                dataType: "json",
                success: function(jqXHR, textstatus) {
                    $('#msg').text(jqXHR["msg"]);
                    // how it is time go to the house page
                    window.location.replace('/');
                }
            });
        });
    }
});