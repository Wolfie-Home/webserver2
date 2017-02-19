'use strict';
// #!include ReactStore.js

var DeviceStore = function() {
    ReactStore.call(this);

    this.DEVICE_LIST_CHANGE_EVENT = '1';
    this.DEVICE_DETAIL_ADDED_EVENT = '2';
    this.DEVICE_DETAIL_UPDATED_EVENT = '3';
    this._deviceList = [];
    this._deviceDetail = {}; // id => detail object
    this._getDeviceDetailLocked = false;
    dispatcher.register(this._getDeviceList.bind(this));
    dispatcher.register(this._getDeviceDetail.bind(this));
    dispatcher.register(this._updateDeviceDetail.bind(this));

    // refresh added devices
    var refreshPeriod = 1500;
    setInterval((function() {
        // refresh all. very bad performance
        if (deviceSelectedStore != undefined) {
            var deviceId = deviceSelectedStore.getDeviceId();
            var action = Actions.createGetDeviceDetailAction(deviceId);
            dispatcher.dispatch(action);
        }
    }).bind(this), refreshPeriod);
};
DeviceStore.prototype = Object.assign({}, ReactStore.prototype);

DeviceStore.prototype._getDeviceList = function(action) {
    if (!Actions.extractGetDeviceListAction(action)) {
        return ;
    }

    var url = '/api/device';
    $.ajax(url, {
        'context': this,
        'dataType': 'json',
        'method': 'GET'
    }).done(function(data, textStatus, jqxhr) {
        if (jqxhr.status == 200) {
            _.each(data['devices'], function(device) {
                device['children'] = undefined; // we dont need this data.
            });
            this._deviceList = data['devices'];
            this._notifyCallbacks(this.DEVICE_LIST_CHANGE_EVENT);
        }
    });
};

DeviceStore.prototype._getDeviceDetail = function(action) {
    if (!Actions.extractGetDeviceDetailAction(action)) {
        return ;
    }

    if (this._getDeviceDetailLocked) {
        return ;
    }

    var deviceId = Actions.extractGetDeviceDetailAction(action);
    
    this._getDeviceDetailLocked = true;

    var url = '/api/device/' + deviceId;

    this._getDeviceDetail.deviceId = deviceId;
    this._getDeviceDetail.callbackNum = 0;
    this._getDeviceDetail.callbackSuccesses = 0;
    this._getDeviceDetail.callback = (function() {
        if (this._getDeviceDetail.callbackNum == 2 && this._getDeviceDetail.callbackSuccesses == 2) {
            // notification ready
            var data = this._getDeviceDetail.data;
            data['property'] = this._getDeviceDetail.property['parameters'];
            this._deviceDetail[this._getDeviceDetail.deviceId] = data;
            this._notifyCallbacks(this.DEVICE_DETAIL_ADDED_EVENT);
        } else if (this._getDeviceDetail.callbackNum == 2) {
            // TODO get request failed....
            console.log('faild3');
        }

        if (this._getDeviceDetail.callbackNum == 2) {
            this._getDeviceDetailLocked = false;
        }
    }).bind(this);
    // this._getDeviceDetail.callback.bind(this);

    $.ajax(url, {
        'context': this,
        'dataType': 'json',
        'method': 'GET'
    }).done(function(data, textStatus, jqxhr) {
        if (jqxhr.status == 200) {
            this._getDeviceDetail.callbackSuccesses += 1;
            this._getDeviceDetail.data = data;
        } else {
            console.log('failed to get device')
        }

        this._getDeviceDetail.callbackNum += 1;
        this._getDeviceDetail.callback();
    }).fail(function() {
        this._getDeviceDetail.callbackNum += 1;
        this._getDeviceDetail.callback();
    })

    var propertyUrl = '/api/device/' + deviceId + '/property';
    $.ajax(propertyUrl, {
        'context': this,
        'dataType': 'json',
        'method': 'GET'
    }).done(function(data, textStatus, jqxhr) {
        if (jqxhr.status == 200) {
            this._getDeviceDetail.callbackSuccesses += 1;
            this._getDeviceDetail.property = data;
        } else {
            console.log('failed property url');
        }

        this._getDeviceDetail.callbackNum += 1;
        this._getDeviceDetail.callback();
    }).fail(function() {
        this._getDeviceDetail.callbackNum += 1;
        this._getDeviceDetail.callback();
    });

};

DeviceStore.prototype._updateDeviceDetail = function(action) {
    if (Actions.extractUpdateDeviceDetailAction(action) == null) {
        return ;
    }

    var updateData = Actions.extractUpdateDeviceDetailAction(action);
    var device = updateData['device'];
    var update = updateData['update'];

    // var url = 'dev_api/'+device['location']+'/'device['name'];
    var url = 'dev_api/defaultUser/'+'HackCEWIT'+'/'+device['name']; // hardcode it for now.
    var data = {
        'type': 'info',
        'content': update,
        'password': 'no needed',
    };

    this._updateDeviceDetail.deviceId = device['id'];
    $.ajax(url, {
        'context': this,
        'dataType': 'json',
        'contentType': 'application/json',
        'data': JSON.stringify(data),
        'method': 'POST'
    }).done(function(data, textStatus, jqxhr) {
        if (jqxhr.status == 200) {
            // re-getting device
            var action = Actions.createGetDeviceDetailAction(this._updateDeviceDetail.deviceId);
            dispatcher.dispatch(action);
            this._notifyCallbacks(this.DEVICE_DETAIL_UPDATED_EVENT);
        } else {
            if (showMsg) {
                showMsg('failed to update');
            }
        }
    }).fail(function(){
        if (showMsg) {
            showMsg('server error.');
        }
    });


// @updateData : {
    //     'device': {} // type of detail device from DeviceStore 
    //     'update': {} // name => value object..   
    // }

    // notify.
}

DeviceStore.prototype.getDevices = function() {
    // WARNING, shodow copy.
    return this._deviceDetail;
};

// get device list. a device format is like
// [{
//    "user_id":1,
//    "location":null,
//    "class_id":null,
//    "id":1,
//    "location_id":null,
//    "mother_id":null,
//    "name":"defaultDevice1",
//    "description":"This is default device in nowhere",
// }]
DeviceStore.prototype.getDeviceList = function() {
    var ret = _.map(this._deviceList, function(elm) {
                    return _.clone(elm);
                });
    return ret;
};

// listen to device list and see if there is any changes.
// @callback,
// @return, index used for unregistering.
DeviceStore.prototype.registerDeviceListChange = function(callback) {
    return this._registerCallback(callback, this.DEVICE_LIST_CHANGE_EVENT);
};
DeviceStore.prototype.unregisterDeviceListChange = function(index) {
    return this._unregisterCallback(index, this.DEVICE_LIST_CHANGE_EVENT);
};

// override previous one is also means added.
DeviceStore.prototype.registerDeviceDetailAdded = function(callback) {
    return this._registerCallback(callback, this.DEVICE_DETAIL_ADDED_EVENT);
};
DeviceStore.prototype.unregisterDeviceDetailAdded = function(index) {
    return this._unregisterCallback(index, this.DEVICE_DETAIL_ADDED_EVENT);
};

DeviceStore.prototype.registerDeviceDetailUpdated = function(callback) {
    return this._registerCallback(callback, this.DEVICE_DETAIL_UPDATED_EVENT);
};
DeviceStore.prototype.registerDeviceDetailUpdated = function(index) {
    return this._registerCallback(index, this.DEVICE_DETAIL_UPDATED_EVENT);
};

// deviceStore.getDeviceList() should return list, 
//   and deviceStore.tested  is true 
var testDeviceStore = function() {
    var callback = function() {
        console.log('testGetDeviceList callback');
        deviceStore.tested = true;
    };
    deviceStore.registerDeviceListChange(callback);
    dispatcher.dispatch(Actions.createGetDeviceListAction());

    var callback2 = function() {
        console.log('testGetDeviceList callback 2');
        deviceStore.tested2 = true;
    };
    deviceStore.registerDeviceDetailAdded(callback2);
    dispatcher.dispatch(Actions.createGetDeviceDetailAction(2));
};

var deviceStore = new DeviceStore();
