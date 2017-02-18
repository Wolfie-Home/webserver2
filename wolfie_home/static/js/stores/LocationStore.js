// #!include ../global.js

var LocationStore = function () {
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
    // ];
};
// @return, a data structure that is compatible with LocationSelectionView
//   state['data']. on no data, return null.
LocationStore.prototype = Object.assign({},ReactStore.prototype);
LocationStore.prototype.getHouse = function() {
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
LocationStore.prototype.registerUpdateCallback = function(cb) {
    return this._registerCallback(cb, this._updateEvent);
};
LocationStore.prototype.unregisterUpdateCallback = function(index) {
    this._unregisterCallback(index, this._updateEvent);
};

locationStoreTest = function() {
    var locationStore = new LocationStore();
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
    locationStoreTestResult = locationStore.getHouse();
    console.log('check locationStoreTestResult');
};

var locationStore = new LocationStore();
