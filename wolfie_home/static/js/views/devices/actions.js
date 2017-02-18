// #!include ../global.js


// WARNING, assuming not name duplications....
Actions.DEVICE_SELECT_DEVICE_ACTION = 'Device1';
Actions.createSelectDeviceAction = function(deviceId) {
    return this._create(this.SELECT_LOCATION_ACTION, deviceId);
};
Actions.extractSelectDeviceAction = function(action) {
	return this._extract(this.SELECT_LOCATION_ACTION, action);
};