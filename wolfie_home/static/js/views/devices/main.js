'use strict';

// #!include DeviceListView.js
// #!include DeviceView.js


// initialization

$("#devicesLink").addClass("active");

var ui = React.createElement(
    "div",
    { className: "row" },
    React.createElement(
        "div",
        { className: "col-md-4" },
        React.createElement(DeviceListView, null),
        ","
    ),
    React.createElement(
        "div",
        { className: "col-md-8" },
        React.createElement(DeviceView, null)
    )
);

ReactDOM.render(ui, document.getElementById('main'));

