'use strict';

window.WolfieHomeLocation = window.WolfieHomeLocation || {};

WolfieHomeLocation.LocationStore = function () {
    this._locations = null;
    this._ready = false;
    this._url = '/api/location';
    $.ajax(this._url, {
        'context': this,
        'contentType': 'application/json',
        'dataType': 'json'
    }).done(function (data, textStatus, jqxhr) {
        if (jqxhr.status == 200) {
            this._locations = data['locations'];
            this._ready = true;
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
    //     {
    //         'id': '2',
    //         'name': 'room1',
    //         'description': 'description of the house/room',
    //         'house_id': '1' 
    //     },
    //     {
    //         'id': '3',
    //         'name': 'name of house/room',
    //         'description': 'description of the house/room',
    //         'house_id': null  
    //     },
    //     {
    //         'id': '4',
    //         'name': 'name of house/room',
    //         'description': 'description of the house/room',
    //         'house_id': '3'  
    //     },
    //     {
    //         'id': '5',
    //         'name': 'name of house/room',
    //         'description': 'description of the house/room',
    //         'house_id': '3'  
    //     },
    //     {
    //         'id': '6',
    //         'name': 'name of house/room',
    //         'description': 'description of the house/room',
    //         'house_id': '3'  
    //     }    
    // ];
};
// @return, a data structure that is compatible with LocationView
//   state['data'].
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
    }
};
WolfieHomeLocation.LocationStore.prototype.isReady = function () {
    return this._ready;
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

//  @prop['locationStore'], an instance of LocationStore
//  @state, json object:
//  @path, an order list for representing a path.
//  @button, string display for the button.
//  @data, according to ChaoNestedListUi data structure.
WolfieHomeLocation.LocationView = React.createClass({
    displayName: 'LocationView',

    getInitialState: function () {
        return {
            'path': ['sushi paradise'],
            'button': 'Create',
            'data': [{
                'name': 'sushi paradise',
                'list': [{
                    'name': 'sushi',
                    'list': [{
                        'name': 'cali roll',
                        'list': null
                    }, {
                        'name': 'boston roll',
                        'list': null
                    }]
                }, {
                    'name': 'spicy food',
                    'list': [{
                        'name': 'thai',
                        'list': null
                    }, {
                        'name': 'szuan',
                        'list': null
                    }]
                }]
            }]
        };
    },

    setPath: function (newPath) {
        window.cj = newPath;
        this.setState({ path: newPath });
    },

    enterListElm: function (listElm) {
        window.listElm = listElm;
        if (!listElm.list) {
            return;
        }

        var path = this.state.path.slice();
        path.push(listElm.name);
        this.setPath(path);
    },

    clickOnButton: function () {
        // TODO
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
                        { href: '#', onClick: this.setPath.bind(this, curPath.slice()) },
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
                    { href: '#',
                        onClick: this.enterListElm.bind(this, elm) },
                    elm.name
                )
            ));
        }
        var listUiContainer = React.createElement(
            'ul',
            { className: 'nav nav-tabs nav-stacked' },
            listUi
        );

        // button 
        var buttonUi = React.createElement(
            'button',
            { className: 'btn btn-primary', style: { 'margin-top': '10px' } },
            buttonName
        );

        return React.createElement(
            'div',
            { className: 'container' },
            breadcrumbUi,
            listUiContainer,
            buttonUi
        );
    }

});

ReactDOM.render(React.createElement(WolfieHomeLocation.LocationView, null), document.getElementById('main'));

