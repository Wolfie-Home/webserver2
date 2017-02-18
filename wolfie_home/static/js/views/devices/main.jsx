'use strict';

// #!include DeviceListView.js
// #!include DeviceView.js


// initialization
$("#devicesLink").addClass("active");

var ui = (
    <div className='row'>
        <div className='col-md-4'>
            <DeviceListView />,
        </div>
        <div className='col-md-8'>
            <DeviceView /> 
        </div>
    </div>
);
    
ReactDOM.render(
    ui,
    document.getElementById('main')
);