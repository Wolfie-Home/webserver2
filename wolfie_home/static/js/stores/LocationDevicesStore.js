
// #!include Store.js

/********* Devices in a location Store ****/
var LocationDevicesStore = function () {
    // NOT tested

    ReactStore.call(this);
    // @_devices = {'locationId': [<device>] }
    this._devices = {};
    this._DEVICES_CHANGE = '1';

    dispatcher.register(this._pullDevices.bind(this));
};
LocationDevicesStore.prototype = Object.assign({},ReactStore.prototype);
LocationDevicesStore.prototype._generateRequestUrl = function(locationId) {
    var url = '/api/location/'+locationId+'/device';
    return url;
};
LocationDevicesStore.prototype._pullDevices = function(action) {
    var locationId = Actions.extractLocationDevicesActionData(action);
    if (locationId == null) {
        return ;
    }

    var url = this._generateRequestUrl(locationId);
    var context = {
        'locationDevicesStore': this,
        'locationId': locationId
    };

    $.ajax(url, {
        'context': context,
        'contentType': 'application/json',
        'dataType': 'json',
        'method': 'GET'
    }).done(function(data, textStatus, jqxhr) {
        var locationDevicesStore = this['locationDevicesStore'];
        var devices = locationDevicesStore._devices;
        var locationId = this['locationId'];
        if (jqxhr.status == 200) {
            devices[locationId] = data['devices'];
            locationDevicesStore._notifyCallbacks(locationDevicesStore._DEVICES_CHANGE);// FIX ME
            console.log('LocationDevicesStore get data successfully');
        } else {
            console.log('LocationDevicesStore fail to get data');
        }
    });
};
LocationDevicesStore.prototype.registerDevicesChangeCallback = function(cb) {
    return this._registerCallback(cb, this._DEVICES_CHANGE);
};
LocationDevicesStore.prototype.unregisterDevicesChangeCallback = function(index) {
    return this._unregisterCallback(index, this._DEVICES_CHANGE);
};
LocationDevicesStore.prototype.getDevicesByLocationId = function(id) {
    var allDevices = this._devices[id];
    if (!allDevices) {
        return [];
    }

    var devices = _.map(allDevices, function(dev) {
        return _.clone(dev);
    });
    return devices;
};

var locationDevicesStore = new LocationDevicesStore();