'use strict';

var DeviceView = React.createClass({

	getInitialState: function() {
		return {
			'currentDeviceId': undefined,
			'devices': {},
			'control': false
		}
	},

	componentDidMount: function() {

		// FIXME listener leaks.
		var deviceAdded = (function() {
			console.log(1);
			this.setState({
				'devices': deviceStore.getDevices(),
			});
		}).bind(this);

		var deviceSelected = (function() {
			console.log(2);
			this.setState({
				'currentDeviceId': deviceSelectedStore.getDeviceId(),
			})
		}).bind(this);

		deviceStore.registerDeviceDetailAdded(deviceAdded);
		deviceSelectedStore.registerDeviceSelected(deviceSelected);
	},

	render: function() {
		var notReadyUi = (<div> </div>);
		if (!this.state['currentDeviceId']) {
			return notReadyUi;
		}

		var devices = this.state['devices'];
		var currentDeviceId = this.state['currentDeviceId'];
		if (!_.has(devices, currentDeviceId)) {
			return (<div> waiting </div>);
		}

		var device = devices[currentDeviceId];
		var control = this.state['control'];

		var ui = undefined;
		if (!control) {
			var dataUi = _.map(device['property'], function(prop) {
				var value;
				var time;
				if (prop['records'].length == 0) {
					value = 'Not Available';
					time = 'Not Available';
				} else {
					value = prop['records'][0]['value'] + '';
					time = prop['records'][0]['time'] + '';
				}

				return (
					<tr>
						<td> {prop['name']} </td>
						<td> {value} </td>
						<td> {time} </td>
					</tr>
					);
			});

			ui = (
				<div className="panel panel-primary">
	  				<div className="panel-heading">
	    				<h3 className="panel-title">{device['name']}</h3>
	  				</div>
	  				<div className="panel-body">
	    				<div className='row'> {device['description']} </div>
	    				<div className='row'>
	    					<table className='table'>
	    						<thead> <tr>
	    							<td> name </td>
	    							<td> value </td>
	    							<td> time </td>
	    						</tr> </thead>

	    						<tbody>
	    							{dataUi}
	 							</tbody>
	    					</table>
	    				</div>	
	  				</div>
				</div>);
		} else {
			throw "not yet..";
		}

		return ui;

	}


});