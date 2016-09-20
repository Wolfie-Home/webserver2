'use strict';

var ReactStore = function() {
    this._callbacks = {};
};
ReactStore.prototype._nop = function() {return ;};
// @cb, callback
// @event, string
// @return, a index
ReactStore.prototype._registerCallback = function(cb, event) {
    if (!this._callbacks[event]) {
        this._callbacks[event] = [];
    }
    this._callbacks[event].push(cb);
    return this._callbacks[event].length - 1;
};
// @index, from @return of registerCallback
// @event, string
ReactStore.prototype._unregisterCallback = function(index, event) {
    if (this._callbacks[event] != undefined && index >= 0 &&
        index < this._callbacks[event].length) {
        this._callbacks[event][index] = this._nop;
    }
};
ReactStore.prototype._notifyCallbacks = function(event) {
    if (this._callbacks[event] != undefined) {
        async.each(this._callbacks[event], function(callback) {
            callback();
        });
    }
};

var ReactStoreTest = function() {
    window.s = s;
    var s = new ReactStore();
    var dummyEvent = 'dummyEvent';
    s._registerCallback(function() {
        console.log('ReactStoreTest callback invoked.');
    }, dummyEvent);
    s._notifyCallbacks(dummyEvent);
    s._unregisterCallback(0, 'dummyEvent');
    console.log('unregisterCallback.');
    s._notifyCallbacks(dummyEvent);
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
    }).done(function(data, textStatus, jqxhr) {
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
//   state['data']. on no data, return null.
WolfieHomeLocation.LocationStore.prototype = Object.assign({},ReactStore.prototype);
WolfieHomeLocation.LocationStore.prototype.getHouse = function() {
    if (this._locations != null) {
        // finding out all houses
        var houses = _.filter(this._locations, function(location) {
            return location['house_id'] == null;
        });
        houses = _.map(houses, function(h) {
            return _.clone(h);
        });

        // finding out rooms inside each house
        _.each(houses, function(house) {
            var rooms = _.filter(this._locations, function (location) {
                var id = this;
                return id == location['house_id'];
            }, house['id']);
            rooms = _.map(rooms, function(r) {
                return _.clone(r);
            });
            house['list'] = rooms;
        }, this);
        return houses;
    } else {
        return null;
    }
};
WolfieHomeLocation.LocationStore.prototype.registerUpdateCallback = function(cb) {
    return this._registerCallback(cb, this._updateEvent);
};
WolfieHomeLocation.LocationStore.prototype.unregisterUpdateCallback = function(index) {
    this._registerCallback(index, this._updateEvent);
};

WolfieHomeLocation.locationStoreTest = function() {
    var locationStore = new WolfieHomeLocation.LocationStore();
    locationStore._locations = [
        {
            'id': '1',
            'name': 'my house 1',
            'description': 'description of the house/room',
            'house_id': null  
        },
        {
            'id': '2',
            'name': 'room1',
            'description': 'description of the house/room',
            'house_id': '1' 
        },
        {
            'id': '3',
            'name': 'name of house/room',
            'description': 'description of the house/room',
            'house_id': null  
        },
        {
            'id': '4',
            'name': 'name of house/room',
            'description': 'description of the house/room',
            'house_id': '3'  
        },
        {
            'id': '5',
            'name': 'name of house/room',
            'description': 'description of the house/room',
            'house_id': '3'  
        },
        {
            'id': '6',
            'name': 'name of house/room',
            'description': 'description of the house/room',
            'house_id': '3'  
        }    
    ];
    WolfieHomeLocation.locationStoreTestResult = locationStore.getHouse();
    console.log('check WolfieHomeLocation.locationStoreTestResult');
};


//  @prop['locationStore'], an instance of LocationStore
//  @state, json object:
//  @path, an order list for representing a path.
//  @button, string display for the button.
//  @data, according to ChaoNestedListUi data structure.
WolfieHomeLocation.LocationView = React.createClass({
    getInitialState: function() {
        var locationStore = this.props['locationStore'];
        var house = locationStore.getHouse();
        var list = house == null ? {} : house;
        // wrap it
        list = [{
            'name': "user's house",
            'list': list
        }];
        return  {
            'path': ["user's house"],
            'data': list
        };
    },

    componentDidMount: function() {
        this._listUpdateIndex = 
            this.props['locationStore'].registerUpdateCallback(this.listUpdate);
    },

    componentWillUnmount : function() {
        this.props['locationStore'].unregisterUpdateCallback(this._listUpdateIndex);
    },

    listUpdate: function() {
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

    setPath: function(newPath) {
        window.cj = newPath;
        this.setState({path: newPath});
    },

    enterListElm: function(listElm) {
        window.listElm = listElm;
        if (!listElm.list) {
            return;
        }

        var path = this.state.path.slice();
        path.push(listElm.name);
        this.setPath(path);
    },

    render: function() {
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
            if (i == path.length-1) {
                // last one
                elmUi = (
                    <li className="active">{pathElm}</li>
                );
            } else {
                elmUi = (
                <li>
                    <a href="#" onClick={this.setPath.bind(this, curPath.slice())}>{pathElm}</a>
                    <span className="divider"></span>
                </li>
                );
            }
            breadcrumbUi.push(elmUi);
        }

        breadcrumbUi = (
            <ul className="breadcrumb">
              {breadcrumbUi}
            </ul>
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
                return ;
            }
            list = listContainer.list;
        }

        // build ui
        var listUi = [];
        for (var i = 0; i < list.length; i++) {
            var elm = list[i];
            listUi.push(
              <li >
                <a href="#"
                   onClick={this.enterListElm.bind(this, elm)} >
                {elm.name}
                </a>
              </li>
            );
        }
        var listUiContainer = (
            <ul className="nav nav-tabs nav-stacked">
            {listUi}
            </ul>
        );
    
        return (
            <div className="container">
                {breadcrumbUi}
                {listUiContainer}
            </div>
        );
    }
    
});

var locationStore = new WolfieHomeLocation.LocationStore();
ReactDOM.render(
    <WolfieHomeLocation.LocationView 
     locationStore={locationStore} />,
    document.getElementById('main')
);
$("#locationLink").addClass("active");




