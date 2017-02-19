'use strict';

var DeviceView = React.createClass({

	getInitialState: function() {
		return {
			'currentDeviceId': undefined,
			'devices': {},
			'control': false,
			'controlForm': {}, // name => value. holds values when control == true
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
				'control': false,
				'controlForm': {}
			})
		}).bind(this);

		var deviceUpdated = (function() {
			// pass... deviceAdded will be called eventually.
		}).bind(this);

		deviceStore.registerDeviceDetailAdded(deviceAdded);
		deviceStore.registerDeviceDetailUpdated(deviceUpdated);
		deviceSelectedStore.registerDeviceSelected(deviceSelected);
	},

	handleControlToggle: function(event) {
		var control = this.state['control'];
		var checked = event.target.checked;
		if (!control && checked) {
			var deviceId = this.state['currentDeviceId'];
			var device = this.state['devices'][deviceId];
			var controlForm = {};
			for (var i = 0; i < device['property'].length; i++) {
				var prop = device['property'][i];
				if (prop.records.length > 0) {
					controlForm[prop['name']] = prop.records[0]['value']
				} else {
					controlForm[prop['name']] = undefined;
				}
			}

			this.setState({
				'control': event.target.checked,
				'controlForm': controlForm,
			});
		} else if (control && !checked) {
			this.setState({
				'control': event.target.checked,
				'controlForm': {},
			});
		}
	},

	setBoolean: function(name, event) {
		var controlForm = this.state['controlForm'];
		controlForm[name] = event.target.checked;
		this.setState({
			'controlForm': controlForm,
		});
	},

	updateInteger: function(name, event) {
		var controlForm = this.state['controlForm'];
		// TODO checking.
		controlForm[name] = event.target.value;
		this.setState({
			'controlForm': controlForm,
		});
	},

	updateNumber: function(name, event) {
		var controlForm = this.state['controlForm'];
		// TODO checking.
		controlForm[name] = event.target.value;
		this.setState({
			'controlForm': controlForm,
		});
	},

	updateString: function(name, event) {
		var controlForm = this.state['controlForm'];
		// TODO checking.
		controlForm[name] = event.target.value;
		this.setState({
			'controlForm': controlForm,
		})
	},

	applyChange: function() {
		// prepare data
		var controlForm = this.state['controlForm'];
		var device = this.state['devices'][this.state['currentDeviceId']];

		var data = {
			'device': device,
			'update': controlForm
		}

		var action = Actions.createUpdateDeviceDetailAction(data);
		dispatcher.dispatch(action);

		showMsg('update request has been sent');
		this.setState({
			'control': false,
			'controlForm': {}
		})
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

			var formUi = _.map(device['property'], function(prop) {
				var name = prop['name'];
				var controlForm = this.state['controlForm'];

				var value = controlForm[name] !== undefined ? controlForm[name] : '';

				// 0 means not controllable
				if (prop['controllable'] == 0) {
					return (<tr>
						<td> {prop['name']} </td>
						<td> {value+''} </td>
					</tr>);
				} else {
					var tdInput = (<td>????</td>);

					if (prop['type'] == 'boolean') {
						tdInput = (
							<td> 	
	        					True 
	        					<div className="input-group">
				      				<span className="input-group-addon">
				        				True:<input type="checkbox" aria-label="control"
				        						 onChange={this.setBoolean.bind(this, name)}/>
				     				</span>
				    			</div>						
	    					</td>
							);
					} else if (prop['type'] == 'integer') {
						tdInput = (
							<td>
								<input type="number" class="form-control" 
									value={value}
									onChange={this.updateInteger.bind(this, name)}/>
							</td>
							);
					} else if (prop['type'] == 'number') {
						tdInput = (
							<td>
								<input type="number" class="form-control" 
									value={value}
									onChange={this.updateNumber.bind(this, name)}/>
							</td>
							);
					} else if (prop['type'] == 'string') {
						tdInput = (
							<td>
								<input type="text" class="form-control" 
									value={value}
									onChange={this.updateString.bind(this, name)}/>
							</td>

							);
					} else {
						showMsg('data corrupted?');
					}

					return (<tr>
								<td> {prop['name']} </td>
								{tdInput}
							</tr>);
				}

			}, this);

			ui = (
				<div>
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
		    						</tr> </thead>

		    						<tbody>
		    							{formUi}
		 							</tbody>
		    					</table>
		    				</div>	
		  				</div>
					</div>

					<div>
						<span className='btn btn-primary' onClick={this.applyChange}>
							Apply
						</span>
					</div>
				</div>);
		}

		var controlBtn = (
				<div className='row'>
				    <div className="input-group">
				      <span className="input-group-addon">
				        Control:<input type="checkbox" aria-label="control" checked={control}
				        			onChange={this.handleControlToggle}/>
				      </span>
				    </div>
			    </div>
			);

		return (
			<div>
				<div className='row'> {controlBtn} </div>
				<div className='row'> {ui} </div>
			</div>
			);

	}


});