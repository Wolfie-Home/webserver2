'use strict';
// #!include ../stores/ReactStore.js
// #!include actions.js


var DeviceSelectedStore = function() {
    ReactStore.call(this);

    this._deviceId = undefined;
    this.DEVICE_SELECTED_EVENT = '1';

    dispatcher.register(this._deviceSelected.bind(this));
};
DeviceSelectedStore.prototype = Object.assign({}, ReactStore.prototype);

DeviceSelectedStore.prototype._deviceSelected = function(action) {
	if (!Actions.extractSelectDeviceAction(action)) {
		return ;
	}

	var deviceId = Actions.extractSelectDeviceAction(action);
	this._deviceId = deviceId;
	this._notifyCallbacks(this.DEVICE_SELECTED_EVENT);
};
DeviceSelectedStore.prototype.getDeviceId = function() {
	return this._deviceId;
};

DeviceSelectedStore.prototype.registerDeviceSelected = function(callback) {
    return this._registerCallback(callback, this.DEVICE_SELECTED_EVENT);
};
DeviceSelectedStore.prototype.unregisterDeviceSelected = function(index) {
	return this._unregisterCallback(index, this.DEVICE_SELECTED_EVENT);
};

var deviceSelectedStore = new DeviceSelectedStore();