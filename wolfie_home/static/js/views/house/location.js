'use strict';

// #!include ../global.js
// #!include ../stores/Store.js
// #!include ../stores/LocationStore.js
// #!include ../stores/LocationDeviceStore.js


/****/
//  @state, json object:
//  @path, an order list for representing a path.
//  @button, string display for the button.
//  @data, according to ChaoNestedListUi data structure.

var LocationSelectionView = React.createClass({
    displayName: 'LocationSelectionView',

    getInitialState: function () {
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

    componentDidMount: function () {
        this._listUpdateIndex = locationStore.registerUpdateCallback(this.listUpdate);
    },

    componentWillUnmount: function () {
        locationStore.unregisterUpdateCallback(this._listUpdateIndex);
    },

    listUpdate: function () {
        var list = locationStore.getHouse();
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

    setPath: function (newPath) {
        this.setState({ path: newPath });
    },

    enterListElm: function (listElm) {
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

    render: function () {
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

/****/
// store of info about LocationSelectionView
var LocationSelectionViewStore = function (locationId) {
    // NOT tested
    ReactStore.call(this);

    this._locationSelected = null;
    this._LOCATION_CHANGE = '1';

    dispatcher.register(this._selectLocation.bind(this));
};
LocationSelectionViewStore.prototype = Object.assign({}, ReactStore.prototype);
LocationSelectionViewStore.prototype._selectLocation = function (action) {
    var locationId = Actions.extractSelectLocationActionData(action);
    if (locationId == null) {
        return;
    }

    this._locationSelected = locationId;
    this._notifyCallbacks(this._LOCATION_CHANGE);
};
LocationSelectionViewStore.prototype.registerLocationSelectedChange = function (cb) {
    return this._registerCallback(cb, this._LOCATION_CHANGE);
};
LocationSelectionViewStore.prototype.unregisterLocationSelectedChange = function (index) {
    this._unregisterCallback(index, this._LOCATION_CHANGE);
};
// @return, string, selected location id. null if have not been selected.
LocationSelectionViewStore.prototype.getLocationSelected = function () {
    return this._locationSelected;
};
var locationSelectionViewStore = new LocationSelectionViewStore();

var locationSelectionViewStoreTest = function () {
    window.locationSelectionViewStore = new LocationSelectionViewStore();
    window.locationSelectionViewStoreTestData = 0;
    var cb = function () {
        window.locationSelectionViewStoreTestData = 1;
        console.log('check window.locationSelectionViewStoreTestData');
    };

    locationSelectionViewStore.registerLocationSelectedChange(cb);
    dispatcher.dispatch(Actions.createSelectLocationAction('1'));
};

/*** view all devices in a location ***/

var LocationDevicesView = React.createClass({
    displayName: 'LocationDevicesView',

    // NOT TESTED
    devicesChangeCbId: null,
    locationSelectionCbId: null,

    getInitialState: function () {
        return {
            'locationSelected': null,
            'devices': null
        };
    },

    componentDidMount: function () {

        this.devicesChangeCbId = locationDevicesStore.registerDevicesChangeCallback(this.devicesChange.bind(this));
        this.locationSelectionCbId = locationSelectionViewStore.registerLocationSelectedChange(this.locationChange.bind(this));
    },

    componentWillUnmount: function () {
        locationDevicesStore.unregisterDevicesChangeCallback(this.devicesChangeId);
        locationSelectionViewStore.unregisterLocationSelectedChange(this.locationSelectionCbId);
    },

    devicesChange: function () {
        var locationSelectedId = this.state['locationSelected'];
        if (locationSelectedId == null) {
            return;
        }

        this.setState({
            'devices': locationDevicesStore.getDevicesByLocationId(locationSelectedId)
        });
    },

    locationChange: function () {

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

    render: function () {
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
var locationDevicesViewTest = function (container) {
    if (container == undefined) {
        throw 'please specify the input argument';
    }

    var locationSelectionViewStore = new LocationSelectionViewStore();
    var locationDevicesStore = new LocationDevicesStore();
    var ui = React.createElement(LocationDevicesView, null);

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

// initialization
$("#locationLink").addClass("active");

var ui = React.createElement(
    'div',
    { className: 'row' },
    React.createElement(
        'div',
        { className: 'col-md-4' },
        React.createElement(LocationSelectionView, null),
        ','
    ),
    React.createElement(
        'div',
        { className: 'col-md-8' },
        React.createElement(LocationDevicesView, null)
    )
);

ReactDOM.render(ui, document.getElementById('main'));

