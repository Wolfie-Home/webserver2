
// !include ../stores/DeviceStore.js

var DeviceListView = React.createClass({
    displayName: 'DeviceListView',

    deviceListUpdateCallbackId: null,

    getInitialState: function () {
        return {
            'deviceList': [],
            'activeIndex': null
        };
    },

    componentDidMount: function () {
        this.deviceListUpdateCallbackId = deviceStore.registerDeviceListChange(this.handleDeviceListUpdate.bind(this));
        dispatcher.dispatch(Actions.createGetDeviceListAction());
    },

    componentWillUnmount: function () {
        deviceStore.unregisterDeviceListChange(this.deviceListUpdateCallbackId);
    },

    handleDeviceListUpdate: function () {

        var deviceList = deviceStore.getDeviceList();
        this.setState({
            'deviceList': deviceList,
            'activeIndex': null
        });
    },

    handleDeviceClicked: function (device, index) {
        // @device is a element in this.state['deviceList']
        // TODO
        var action = Actions.createSelectDeviceAction(_.clone(device));
        dispatcher.dispatch(action);
        this.setState({
            'activeIndex': index
        });
    },

    render: function () {
        var deviceList = this.state['deviceList'];

        var ListElmsUi = _.map(deviceList, function (device, index) {
            var activeIndex = this.state['activeIndex'];
            if (activeIndex == index) {
                return React.createElement(
                    'li',
                    { className: 'active' },
                    React.createElement(
                        'a',
                        { href: 'javascript:void(0)' },
                        device['name']
                    )
                );
            } else {
                return React.createElement(
                    'li',
                    null,
                    React.createElement(
                        'a',
                        { href: 'javascript:void(0)',
                            onClick: this.handleDeviceClicked.bind(this, device, index) },
                        device['name']
                    )
                );
            }
        }, this);

        var ListUi = React.createElement(
            'ul',
            { className: 'nav nav-pills nav-stacked' },
            ListElmsUi
        );

        return React.createElement(
            'div',
            { className: 'col-md-12' },
            React.createElement(
                'h2',
                null,
                ' Device List '
            ),
            React.createElement(
                'div',
                { className: 'col-md-12' },
                ListUi
            )
        );
    }

});

var testDeviceListView = function (deviceStore, htmlContainerId) {
    var ui = React.createElement(DeviceListView, null);
    ReactDOM.render(ui, document.getElementById(htmlContainerId));
};

var ui = React.createElement(DeviceListView, null);
ReactDOM.render(ui, document.getElementById('main'));

