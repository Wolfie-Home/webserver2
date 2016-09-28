'use strict';

var ReactStore = function ReactStore() {
    this._callbacks = {};
};
ReactStore.prototype._nop = function () {
    return;
};
// @cb, callback
// @event, string
// @return, a index
ReactStore.prototype._registerCallback = function (cb, event) {
    if (!this._callbacks[event]) {
        this._callbacks[event] = [];
    }
    this._callbacks[event].push(cb);
    return this._callbacks[event].length - 1;
};
// @index, from @return of registerCallback
// @event, string
ReactStore.prototype._unregisterCallback = function (index, event) {
    if (this._callbacks[event] != undefined && index >= 0 && index < this._callbacks[event].length) {
        this._callbacks[event][index] = this._nop;
    }
};
ReactStore.prototype._notifyCallbacks = function (event) {
    if (this._callbacks[event] != undefined) {
        async.each(this._callbacks[event], function (callback) {
            callback();
        });
    }
};

var ReactStoreTest = function ReactStoreTest() {
    window.s = s;
    var s = new ReactStore();
    var dummyEvent = 'dummyEvent';
    s._registerCallback(function () {
        console.log('ReactStoreTest callback invoked.');
    }, dummyEvent);
    s._notifyCallbacks(dummyEvent);
    s._unregisterCallback(0, 'dummyEvent');
    console.log('unregisterCallback.');
    s._notifyCallbacks(dummyEvent);
};

/** global variable **/
var dispatcher = new Flux.Dispatcher();

// @create* return a action
// @extract*, return null on failure, and data on success.
var Actions = {

    /*
    an action
    @action, {
        'type': '',
        'data': ''
    }
    */
    _extract: function _extract(type, action) {
        // TODO, less trust on inputs
        if (action['type'] != type) {
            return null;
        } else {
            return action['data'];
        }
    },
    _create: function _create(type, data) {
        return {
            'type': type,
            'data': data
        };
    },

    // @locationId, string, location Id
    SELECT_LOCATION_ACTION: '1',
    createSelectLocationAction: function createSelectLocationAction(locationId) {
        return this._create(this.SELECT_LOCATION_ACTION, locationId);
    },
    extractSelectLocationActionData: function extractSelectLocationActionData(action) {
        return this._extract(this.SELECT_LOCATION_ACTION, action);
    },

    // @locationId, string, location Id
    GET_LOCTION_DEVICES_ACTION: '2',
    createLocationDevicesAction: function createLocationDevicesAction(locationId) {
        return this._create(this.GET_LOCTION_DEVICES_ACTION, locationId);
    },
    extractLocationDevicesActionData: function extractLocationDevicesActionData(action) {
        return this._extract(this.GET_LOCTION_DEVICES_ACTION, action);
    }

};

/************/

window.WolfieHomeLocation = window.WolfieHomeLocation || {};

WolfieHomeLocation.LocationStore = function () {
    ReactStore.call(this);

    this._updateEvent = '1';
    this._locations = null;
    this._changeCallbacks = [];
    this._url = '/api/location';
    $.ajax(this._url, {
        'context': this,
        'contentType': 'application/json',
        'dataType': 'json'
    }).done(function (data, textStatus, jqxhr) {
        if (jqxhr.status == 200) {
            this._locations = data['locations'];
            this._notifyCallbacks(this._updateEvent);
            console.log('LocationStore get data successfully');
        } else {
            console.log('LocationStore fail to get data');
        }
    });

    // //DUMMY DATA
    // this._locations = [
    //     {
    //         'id': '1',
    //         'name': 'my house 1',
    //         'description': 'description of the house/room',
    //         'house_id': null  
    //     }, 
    // ];
};
// @return, a data structure that is compatible with LocationSelectionView
//   state['data']. on no data, return null.
WolfieHomeLocation.LocationStore.prototype = Object.assign({}, ReactStore.prototype);
WolfieHomeLocation.LocationStore.prototype.getHouse = function () {
    if (this._locations != null) {
        // finding out all houses
        var houses = _.filter(this._locations, function (location) {
            return location['house_id'] == null;
        });
        houses = _.map(houses, function (h) {
            return _.clone(h);
        });

        // finding out rooms inside each house
        _.each(houses, function (house) {
            var rooms = _.filter(this._locations, function (location) {
                var id = this;
                return id == location['house_id'];
            }, house['id']);
            rooms = _.map(rooms, function (r) {
                return _.clone(r);
            });
            house['list'] = rooms;
        }, this);
        return houses;
    } else {
        return null;
    }
};
WolfieHomeLocation.LocationStore.prototype.registerUpdateCallback = function (cb) {
    return this._registerCallback(cb, this._updateEvent);
};
WolfieHomeLocation.LocationStore.prototype.unregisterUpdateCallback = function (index) {
    this._registerCallback(index, this._updateEvent);
};

WolfieHomeLocation.locationStoreTest = function () {
    var locationStore = new WolfieHomeLocation.LocationStore();
    locationStore._locations = [{
        'id': '1',
        'name': 'my house 1',
        'description': 'description of the house/room',
        'house_id': null
    }, {
        'id': '2',
        'name': 'room1',
        'description': 'description of the house/room',
        'house_id': '1'
    }, {
        'id': '3',
        'name': 'name of house/room',
        'description': 'description of the house/room',
        'house_id': null
    }, {
        'id': '4',
        'name': 'name of house/room',
        'description': 'description of the house/room',
        'house_id': '3'
    }, {
        'id': '5',
        'name': 'name of house/room',
        'description': 'description of the house/room',
        'house_id': '3'
    }, {
        'id': '6',
        'name': 'name of house/room',
        'description': 'description of the house/room',
        'house_id': '3'
    }];
    WolfieHomeLocation.locationStoreTestResult = locationStore.getHouse();
    console.log('check WolfieHomeLocation.locationStoreTestResult');
};

/********* Devices in a location Store ****/
WolfieHomeLocation.LocationDevicesStore = function () {
    // NOT tested

    ReactStore.call(this);
    // @_devices = {'locationId': [<device>] }
    this._devices = {};
    this._DEVICES_CHANGE = '1';

    dispatcher.register(this._pullDevices.bind(this));
};
WolfieHomeLocation.LocationDevicesStore.prototype = Object.assign({}, ReactStore.prototype);
WolfieHomeLocation.LocationDevicesStore.prototype._generateRequestUrl = function (locationId) {
    var url = '/api/location/' + locationId + '/device';
    return url;
};
WolfieHomeLocation.LocationDevicesStore.prototype._pullDevices = function (action) {
    var locationId = Actions.extractLocationDevicesActionData(action);
    if (locationId == null) {
        return;
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
    }).done(function (data, textStatus, jqxhr) {
        var locationDevicesStore = this['locationDevicesStore'];
        var devices = locationDevicesStore._devices;
        var locationId = this['locationId'];
        if (jqxhr.status == 200) {
            devices[locationId] = data['devices'];
            locationDevicesStore._notifyCallbacks(locationDevicesStore._DEVICES_CHANGE);
            console.log('LocationDevicesStore get data successfully');
        } else {
            console.log('LocationDevicesStore fail to get data');
        }
    });
};
WolfieHomeLocation.LocationDevicesStore.prototype.registerDevicesChangeCallback = function (cb) {
    return this._registerCallback(cb, this._DEVICES_CHANGE);
};
WolfieHomeLocation.LocationDevicesStore.prototype.unregisterDevicesChangeCallback = function (index) {
    return this._unregisterCallback(index, this._DEVICES_CHANGE);
};
WolfieHomeLocation.LocationDevicesStore.prototype.getDevicesByLocationId = function (id) {
    var allDevices = this._devices[id];
    if (!allDevices) {
        return [];
    }

    var devices = _.map(allDevices, function (dev) {
        return _.clone(dev);
    });
    return devices;
};

// return instance of LocationDevicesStore. cb funciton should be called.
// and devices in side location with @locationId should be available.
// @locationId, id of a location.
WolfieHomeLocation.locationDevicesStoreTest = function (locationId) {
    var l = new WolfieHomeLocation.LocationDevicesStore();
    WolfieHomeLocation.locationDevicesStoreTest.data = 0;
    var cb = function cb() {
        WolfieHomeLocation.locationDevicesStoreTest.data += 1;
    };
    l.registerDevicesChangeCallback(cb);
    var action = Actions.createLocationDevicesAction(locationId);
    dispatcher.dispatch(action);
    return l;
};

/****/
// store of info about LocationSelectionView
WolfieHomeLocation.LocationSelectionViewStore = function (locationId) {
    // NOT tested
    ReactStore.call(this);

    this._locationSelected = null;
    this._LOCATION_CHANGE = '1';

    dispatcher.register(this._selectLocation.bind(this));
};
WolfieHomeLocation.LocationSelectionViewStore.prototype = Object.assign({}, ReactStore.prototype);
WolfieHomeLocation.LocationSelectionViewStore.prototype._selectLocation = function (action) {
    var locationId = Actions.extractSelectLocationActionData(action);
    if (locationId == null) {
        return;
    }

    this._locationSelected = locationId;
    this._notifyCallbacks(this._LOCATION_CHANGE);
};
WolfieHomeLocation.LocationSelectionViewStore.prototype.registerLocationSelectedChange = function (cb) {
    return this._registerCallback(cb, this._LOCATION_CHANGE);
};
WolfieHomeLocation.LocationSelectionViewStore.prototype.unregisterLocationSelectedChange = function (index) {
    this._unregisterCallback(index, this._LOCATION_CHANGE);
};
// @return, string, selected location id. null if have not been selected.
WolfieHomeLocation.LocationSelectionViewStore.prototype.getLocationSelected = function () {
    return this._locationSelected;
};

WolfieHomeLocation.locationSelectionViewStoreTest = function () {
    window.locationSelectionViewStore = new WolfieHomeLocation.LocationSelectionViewStore();
    window.locationSelectionViewStoreTestData = 0;
    var cb = function cb() {
        window.locationSelectionViewStoreTestData = 1;
        console.log('check window.locationSelectionViewStoreTestData');
    };

    locationSelectionViewStore.registerLocationSelectedChange(cb);
    dispatcher.dispatch(Actions.createSelectLocationAction('1'));
};

//TODO
/****/
//  @prop['locationStore'], an instance of LocationStore
//  @state, json object:
//  @path, an order list for representing a path.
//  @button, string display for the button.
//  @data, according to ChaoNestedListUi data structure.
WolfieHomeLocation.LocationSelectionView = React.createClass({
    displayName: 'LocationSelectionView',

    getInitialState: function getInitialState() {
        var locationStore = this.props['locationStore'];
        var house = locationStore.getHouse();
        var list = house == null ? {} : house;
        // wrap it
        list = [{
            'name': "user's house",
            'list': list
        }];
        return {
            'path': ["user's house"],
            'data': list
        };
    },

    componentDidMount: function componentDidMount() {
        this._listUpdateIndex = this.props['locationStore'].registerUpdateCallback(this.listUpdate);
    },

    componentWillUnmount: function componentWillUnmount() {
        this.props['locationStore'].unregisterUpdateCallback(this._listUpdateIndex);
    },

    listUpdate: function listUpdate() {
        var list = this.props['locationStore'].getHouse();
        // wrap it
        list = [{
            'name': "user's house",
            'list': list
        }];
        this.setState({
            'path': ["user's house"],
            'data': list
        });
    },

    setPath: function setPath(newPath) {
        this.setState({ path: newPath });
    },

    enterListElm: function enterListElm(listElm) {
        window.listElm = listElm;
        if (!!listElm.list) {
            var path = this.state.path.slice();
            path.push(listElm.name);
            this.setState({ path: path });
        } else {}

        // TODO be cautions here...
        var action = Actions.createLocationDevicesAction(listElm['id']);
        dispatcher.dispatch(action);
        action = Actions.createSelectLocationAction(listElm['id']);
        dispatcher.dispatch(action);
    },

    render: function render() {
        var path = this.state.path;
        var data = this.state.data;
        var buttonName = this.state.button;

        // building breadcrumb
        var curPath = [];
        var breadcrumbUi = [];
        for (var i = 0; i < path.length; i++) {
            var pathElm = path[i];
            var elmUi = null;
            curPath.push(pathElm);
            if (i == path.length - 1) {
                // last one
                elmUi = React.createElement(
                    'li',
                    { className: 'active' },
                    pathElm
                );
            } else {
                elmUi = React.createElement(
                    'li',
                    null,
                    React.createElement(
                        'a',
                        { href: 'javascript:void(0)', onClick: this.setPath.bind(this, curPath.slice()) },
                        pathElm
                    ),
                    React.createElement('span', { className: 'divider' })
                );
            }
            breadcrumbUi.push(elmUi);
        }

        breadcrumbUi = React.createElement(
            'ul',
            { className: 'breadcrumb' },
            breadcrumbUi
        );

        // find the corresponding list according to path
        var listContainer = null;
        var list = data;
        for (var i = 0; i < path.length; i++) {
            var found = false;
            for (var j = 0; j < list.length; j++) {
                console.log(list[j].name);
                console.log(path[i]);
                if (list[j].name == path[i]) {
                    listContainer = list[j];
                    found = true;
                    break;
                }
            }
            if (!found) {
                window.cjPath = path;
                window.data = data;
                console.log('error, invalid path!');
                return;
            }
            list = listContainer.list;
        }

        // build ui
        var listUi = [];
        for (var i = 0; i < list.length; i++) {
            var elm = list[i];
            listUi.push(React.createElement(
                'li',
                null,
                React.createElement(
                    'a',
                    { href: 'javascript:void(0)',
                        onClick: this.enterListElm.bind(this, elm) },
                    elm.name
                )
            ));
        }
        var listUiContainer = React.createElement(
            'ul',
            { className: 'nav nav-pills nav-stacked' },
            listUi
        );

        return React.createElement(
            'div',
            null,
            breadcrumbUi,
            listUiContainer
        );
    }

});

/*** view all devices in a location ***/
// @props['locationDevicesStore']
// @props['locationSelectionViewStore']
WolfieHomeLocation.LocationDevicesView = React.createClass({
    displayName: 'LocationDevicesView',

    // NOT TESTED
    devicesChangeCbId: null,
    locationSelectionCbId: null,

    getInitialState: function getInitialState() {
        return {
            'locationSelected': null,
            'devices': null
        };
    },

    componentDidMount: function componentDidMount() {
        var locationDevicesStore = this.props['locationDevicesStore'];
        var locationSelectionViewStore = this.props['locationSelectionViewStore'];
        if (!locationDevicesStore || !locationSelectionViewStore) {
            throw 'no stores?';
        }

        this.devicesChangeCbId = locationDevicesStore.registerDevicesChangeCallback(this.devicesChange.bind(this));
        this.locationSelectionCbId = locationSelectionViewStore.registerLocationSelectedChange(this.locationChange.bind(this));
    },

    componentWillUnmount: function componentWillUnmount() {
        var locationDevicesStore = this.props['locationDevicesStore'];
        locationDevicesStore.unregisterDevicesChangeCallback(this.devicesChangeId);
        locationSelectionViewStore.unregisterLocationSelectedChange(this.locationSelectionCbId);
    },

    devicesChange: function devicesChange() {
        var locationDevicesStore = this.props['locationDevicesStore'];
        if (locationDevicesStore == null || locationDevicesStore == undefined) {
            throw "locationDevicesStore props are undefined or null?";
        }

        var locationSelectedId = this.state['locationSelected'];
        if (locationSelectedId == null) {
            return;
        }

        this.setState({
            'devices': locationDevicesStore.getDevicesByLocationId(locationSelectedId)
        });
    },

    locationChange: function locationChange() {
        var locationSelectionViewStore = this.props['locationSelectionViewStore'];
        var locationDevicesStore = this.props['locationDevicesStore'];

        if (!locationSelectionViewStore) {
            throw "locationSelectionViewStore props is nothing?";
        }
        if (!locationDevicesStore) {
            throw "locationDevicesStore props is nothing??";
        }

        var locationSelectedId = locationSelectionViewStore.getLocationSelected();
        if (!locationSelectedId) {
            return;
        }

        var devices = locationDevicesStore.getDevicesByLocationId(locationSelectedId);
        this.setState({
            'locationSelected': locationSelectedId,
            'devices': devices
        });
    },

    render: function render() {
        var devices = this.state['devices'];
        var locationSelected = this.state['locationSelected'];

        var devicesUi;
        if (!devices || !locationSelected) {
            devicesUi = React.createElement(
                'tr',
                { 'class': 'info' },
                React.createElement(
                    'td',
                    { colSpan: '3' },
                    ' No Devices '
                )
            );
        } else {
            devicesUi = _.map(devices, function (dev) {
                return React.createElement(
                    'tr',
                    { className: 'info' },
                    React.createElement(
                        'td',
                        null,
                        ' ',
                        dev['id'],
                        ' '
                    ),
                    React.createElement(
                        'td',
                        null,
                        ' ',
                        dev['name'],
                        ' '
                    ),
                    React.createElement(
                        'td',
                        null,
                        ' ',
                        dev['description'],
                        ' '
                    )
                );
            });
        }

        var locationSelected = this.state['locationSelected'];
        var locationSelectedUi;
        if (!locationSelected) {
            locationSelectedUi = React.createElement(
                'div',
                null,
                ' No location selected. '
            );
        } else {
            locationSelectedUi = React.createElement(
                'div',
                null,
                'Location id: ',
                locationSelected
            );
        }

        return React.createElement(
            'div',
            { className: 'bs-component' },
            React.createElement(
                'div',
                { className: 'col-md-12' },
                locationSelectedUi
            ),
            React.createElement(
                'div',
                { className: 'col-md-12' },
                React.createElement(
                    'table',
                    { className: 'table table-striped table-hover' },
                    React.createElement(
                        'thead',
                        null,
                        React.createElement(
                            'tr',
                            null,
                            React.createElement(
                                'th',
                                null,
                                'id'
                            ),
                            React.createElement(
                                'th',
                                null,
                                'name'
                            ),
                            React.createElement(
                                'th',
                                null,
                                'description'
                            )
                        )
                    ),
                    React.createElement(
                        'tbody',
                        null,
                        devicesUi
                    )
                )
            )
        );
    }
});

// test LocationDevicesView, append to @container. use @return with 
//   actions to change views. 
// After invoking, you should see location id '1' data.
// @container, string of a div.
// @return. {
//            'locationSelectionViewStore': locationSelectionViewStore,
//            'locationDevicesStore': locationDevicesStore
//          };
// NOTE it has been past
WolfieHomeLocation.locationDevicesViewTest = function (container) {
    if (container == undefined) {
        throw 'please specify the input argument';
    }

    var locationSelectionViewStore = new WolfieHomeLocation.LocationSelectionViewStore();
    var locationDevicesStore = new WolfieHomeLocation.LocationDevicesStore();
    var ui = React.createElement(WolfieHomeLocation.LocationDevicesView, {
        locationSelectionViewStore: locationSelectionViewStore,
        locationDevicesStore: locationDevicesStore });

    ReactDOM.render(ui, document.getElementById(container));

    var action = Actions.createLocationDevicesAction('1');
    dispatcher.dispatch(action);
    action = Actions.createSelectLocationAction('1');
    dispatcher.dispatch(action);

    return {
        'locationSelectionViewStore': locationSelectionViewStore,
        'locationDevicesStore': locationDevicesStore
    };
};

// // initialization
// var locationStore = new WolfieHomeLocation.LocationStore();
// ReactDOM.render(
//     <WolfieHomeLocation.LocationSelectionView 
//      locationStore={locationStore} />,
//     document.getElementById('main')
// );
// $("#locationLink").addClass("active");


function initReactViews() {
    $("#locationLink").addClass("active");

    var locationStore = new WolfieHomeLocation.LocationStore();
    var locationSelectionViewStore = new WolfieHomeLocation.LocationSelectionViewStore();
    var locationDevicesStore = new WolfieHomeLocation.LocationDevicesStore();

    var ui = React.createElement(
        'div',
        { className: 'row' },
        React.createElement(
            'div',
            { className: 'col-md-4' },
            React.createElement(WolfieHomeLocation.LocationSelectionView, {
                locationStore: locationStore }),
            ','
        ),
        React.createElement(
            'div',
            { className: 'col-md-8' },
            React.createElement(WolfieHomeLocation.LocationDevicesView, {
                locationDevicesStore: locationDevicesStore,
                locationSelectionViewStore: locationSelectionViewStore })
        )
    );

    ReactDOM.render(ui, document.getElementById('main'));
}

initReactViews();

