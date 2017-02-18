
// !include ../stores/DeviceStore.js

var DeviceListView = React.createClass({
    deviceListUpdateCallbackId: null,

    getInitialState: function() {
        return {
            'deviceList': [],
            'activeIndex': null
        };
    },

    componentDidMount: function() {
        this.deviceListUpdateCallbackId = deviceStore.registerDeviceListChange(
            this.handleDeviceListUpdate.bind(this));
        dispatcher.dispatch(Actions.createGetDeviceListAction());
    },

    componentWillUnmount: function() {
        deviceStore.unregisterDeviceListChange(this.deviceListUpdateCallbackId);
    },

    handleDeviceListUpdate: function() {

        var deviceList = deviceStore.getDeviceList();
        this.setState({
            'deviceList': deviceList,
            'activeIndex': null
        });      
    },

    handleDeviceClicked: function(device, index) {
        // @device is a element in this.state['deviceList']
        // TODO
        var action = Actions.createSelectDeviceAction(_.clone(device));
        dispatcher.dispatch(action);
        this.setState({
            'activeIndex': index
        });
    },

    render: function() {
        var deviceList = this.state['deviceList'];

        var ListElmsUi = _.map(deviceList, function(device, index) {
            var activeIndex = this.state['activeIndex'];
            if (activeIndex == index) {
                return (
                    <li className='active'>
                        <a href='javascript:void(0)'>
                        {device['name']}
                        </a>
                    </li>
                    );
            } else {
                return (
                    <li>
                        <a href='javascript:void(0)'
                            onClick={this.handleDeviceClicked.bind(this, device, index)}>
                        {device['name']}
                        </a>
                    </li>
                    );
            }
        }, this);

        var ListUi = (
            <ul className='nav nav-pills nav-stacked'>
                {ListElmsUi}
            </ul>
            );

        return (
            <div className='col-md-12'>

                <h2> Device List </h2>
                <div className='col-md-12'>
                    {ListUi}
                </div>
            </div>
            );
    }

});

var testDeviceListView = function(deviceStore, htmlContainerId) {
    var ui = (<DeviceListView />);
    ReactDOM.render(
        ui,
        document.getElementById(htmlContainerId)
    );
}

var ui = (<DeviceListView />);
ReactDOM.render(
    ui,
    document.getElementById('main')
);