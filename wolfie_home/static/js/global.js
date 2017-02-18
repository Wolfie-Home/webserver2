

dispatcher = new Flux.Dispatcher();

// @create* return a action
// @extract*, return null on failure, and data on success.
Actions = {

    /*
    an action
    @action, {
        'type': '',
        'data': ''
    }
    */
    _extract: function (type, action) {
        // TODO, less trust on inputs
        if (action['type'] != type) {
            return null;
        } else {
            return action['data'];
        }
    },
    _create: function (type, data) {
        return {
            'type': type,
            'data': data
        };
    },

    // @locationId, string, location Id
    SELECT_LOCATION_ACTION: '1',
    createSelectLocationAction: function(locationId) {
        return this._create(this.SELECT_LOCATION_ACTION, locationId);
    },
    extractSelectLocationActionData: function(action) {
        return this._extract(this.SELECT_LOCATION_ACTION, action);
    },

    // @locationId, string, location Id
    GET_LOCTION_DEVICES_ACTION: '2',
    createLocationDevicesAction: function(locationId) {
        return this._create(this.GET_LOCTION_DEVICES_ACTION, locationId);
    },
    extractLocationDevicesActionData: function(action) {
        return this._extract(this.GET_LOCTION_DEVICES_ACTION, action);
    },
    
    // get device list. Acting on DeviceStore
    GET_DEVICE_LIST_ACTION: '3',
    createGetDeviceListAction: function() {
        return this._create(this.GET_DEVICE_LIST_ACTION, {})
    },
    extractGetDeviceListAction: function(action) {
        return this._extract(this.GET_DEVICE_LIST_ACTION, action);
    },

    // @device, a element from DeviceStore.getDeviceList()
    SELECT_DEVICE_ACTION: '4',
    createSelectDeviceAction: function(device) {
        return this._create(this.SELECT_DEVICE_ACTION, device);
    },
    extractSelectDeviceAction: function(action) {
        return this._extract(this.SELECT_DEVICE_ACTION, action);
    },

    // DeviceStore.js
    DEVICE_DETAIL_ACTION: '5',
    createGetDeviceDetailAction: function(deviceId) {
        return this._create(this.DEVICE_DETAIL_ACTION, deviceId)
    },
    extractGetDeviceDetailAction: function(action) {
        return this._extract(this.DEVICE_DETAIL_ACTION, action);
    },
    
};


