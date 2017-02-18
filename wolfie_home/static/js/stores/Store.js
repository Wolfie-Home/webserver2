// provide a barebone template for implementing a store in Flux
// it can register/unregister callbacks with a "event" identifer, 
// and notify these callbacks.

// var async = require('async');

var ReactStore = function() {
    this._callbacks = {};
};
ReactStore.prototype._nop = function() {return ;};

// register a callback
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

// unregister a callback
// @index, from @return of registerCallback
// @event, string
ReactStore.prototype._unregisterCallback = function(index, event) {
    if (this._callbacks[event] != undefined && index >= 0 &&
        index < this._callbacks[event].length) {
        this._callbacks[event][index] = this._nop;
    }
};

// notify all callbacks with registered by @event
ReactStore.prototype._notifyCallbacks = function(event) {
    if (this._callbacks[event] != undefined) {
        async.each(this._callbacks[event], function(callback) {
            callback();
        });
    }
};

var reactStoreTest = function() {
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


