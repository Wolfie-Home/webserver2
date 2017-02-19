'use strict';

var DeviceView = React.createClass({
	displayName: 'DeviceView',


	getInitialState: function () {
		return {
			'currentDeviceId': undefined,
			'devices': {},
			'control': false,
			'controlForm': {} };
	},

	componentDidMount: function () {

		// FIXME listener leaks.
		var deviceAdded = function () {
			console.log(1);
			this.setState({
				'devices': deviceStore.getDevices()
			});
		}.bind(this);

		var deviceSelected = function () {
			console.log(2);
			this.setState({
				'currentDeviceId': deviceSelectedStore.getDeviceId(),
				'control': false,
				'controlForm': {}
			});
		}.bind(this);

		var deviceUpdated = function () {
			// pass... deviceAdded will be called eventually.
		}.bind(this);

		deviceStore.registerDeviceDetailAdded(deviceAdded);
		deviceStore.registerDeviceDetailUpdated(deviceUpdated);
		deviceSelectedStore.registerDeviceSelected(deviceSelected);
	},

	handleControlToggle: function (event) {
		var control = this.state['control'];
		var checked = event.target.checked;
		if (!control && checked) {
			var deviceId = this.state['currentDeviceId'];
			var device = this.state['devices'][deviceId];
			var controlForm = {};
			for (var i = 0; i < device['property'].length; i++) {
				var prop = device['property'][i];
				if (prop.records.length > 0) {
					controlForm[prop['name']] = prop.records[0]['value'];
				} else {
					controlForm[prop['name']] = undefined;
				}
			}

			this.setState({
				'control': event.target.checked,
				'controlForm': controlForm
			});
		} else if (control && !checked) {
			this.setState({
				'control': event.target.checked,
				'controlForm': {}
			});
		}
	},

	setBoolean: function (name, event) {
		var controlForm = this.state['controlForm'];
		controlForm[name] = event.target.checked;
		this.setState({
			'controlForm': controlForm
		});
	},

	updateInteger: function (name, event) {
		var controlForm = this.state['controlForm'];
		// TODO checking.
		controlForm[name] = event.target.value;
		this.setState({
			'controlForm': controlForm
		});
	},

	updateNumber: function (name, event) {
		var controlForm = this.state['controlForm'];
		// TODO checking.
		controlForm[name] = event.target.value;
		this.setState({
			'controlForm': controlForm
		});
	},

	updateString: function (name, event) {
		var controlForm = this.state['controlForm'];
		// TODO checking.
		controlForm[name] = event.target.value;
		this.setState({
			'controlForm': controlForm
		});
	},

	applyChange: function () {
		// prepare data
		var controlForm = this.state['controlForm'];
		var device = this.state['devices'][this.state['currentDeviceId']];

		var data = {
			'device': device,
			'update': controlForm
		};

		var action = Actions.createUpdateDeviceDetailAction(data);
		dispatcher.dispatch(action);

		showMsg('update request has been sent');
		this.setState({
			'control': false,
			'controlForm': {}
		});
	},

	render: function () {
		var notReadyUi = React.createElement(
			'div',
			null,
			' '
		);
		if (!this.state['currentDeviceId']) {
			return notReadyUi;
		}

		var devices = this.state['devices'];
		var currentDeviceId = this.state['currentDeviceId'];
		if (!_.has(devices, currentDeviceId)) {
			return React.createElement(
				'div',
				null,
				' waiting '
			);
		}

		var device = devices[currentDeviceId];
		var control = this.state['control'];

		var ui = undefined;
		if (!control) {
			var dataUi = _.map(device['property'], function (prop) {
				var value;
				var time;
				if (prop['records'].length == 0) {
					value = 'Not Available';
					time = 'Not Available';
				} else {
					value = prop['records'][0]['value'] + '';
					time = prop['records'][0]['time'] + '';
				}

				return React.createElement(
					'tr',
					null,
					React.createElement(
						'td',
						null,
						' ',
						prop['name'],
						' '
					),
					React.createElement(
						'td',
						null,
						' ',
						value,
						' '
					),
					React.createElement(
						'td',
						null,
						' ',
						time,
						' '
					)
				);
			});

			ui = React.createElement(
				'div',
				{ className: 'panel panel-primary' },
				React.createElement(
					'div',
					{ className: 'panel-heading' },
					React.createElement(
						'h3',
						{ className: 'panel-title' },
						device['name']
					)
				),
				React.createElement(
					'div',
					{ className: 'panel-body' },
					React.createElement(
						'div',
						{ className: 'row' },
						' ',
						device['description'],
						' '
					),
					React.createElement(
						'div',
						{ className: 'row' },
						React.createElement(
							'table',
							{ className: 'table' },
							React.createElement(
								'thead',
								null,
								' ',
								React.createElement(
									'tr',
									null,
									React.createElement(
										'td',
										null,
										' name '
									),
									React.createElement(
										'td',
										null,
										' value '
									),
									React.createElement(
										'td',
										null,
										' time '
									)
								),
								' '
							),
							React.createElement(
								'tbody',
								null,
								dataUi
							)
						)
					)
				)
			);
		} else {

			var formUi = _.map(device['property'], function (prop) {
				var name = prop['name'];
				var controlForm = this.state['controlForm'];

				var value = controlForm[name] !== undefined ? controlForm[name] : '';

				// 0 means not controllable
				if (prop['controllable'] == 0) {
					return React.createElement(
						'tr',
						null,
						React.createElement(
							'td',
							null,
							' ',
							prop['name'],
							' '
						),
						React.createElement(
							'td',
							null,
							' ',
							value + '',
							' '
						)
					);
				} else {
					var tdInput = React.createElement(
						'td',
						null,
						'????'
					);

					if (prop['type'] == 'boolean') {
						tdInput = React.createElement(
							'td',
							null,
							'True',
							React.createElement(
								'div',
								{ className: 'input-group' },
								React.createElement(
									'span',
									{ className: 'input-group-addon' },
									'True:',
									React.createElement('input', { type: 'checkbox', 'aria-label': 'control',
										onChange: this.setBoolean.bind(this, name) })
								)
							)
						);
					} else if (prop['type'] == 'integer') {
						tdInput = React.createElement(
							'td',
							null,
							React.createElement('input', { type: 'number', 'class': 'form-control',
								value: value,
								onChange: this.updateInteger.bind(this, name) })
						);
					} else if (prop['type'] == 'number') {
						tdInput = React.createElement(
							'td',
							null,
							React.createElement('input', { type: 'number', 'class': 'form-control',
								value: value,
								onChange: this.updateNumber.bind(this, name) })
						);
					} else if (prop['type'] == 'string') {
						tdInput = React.createElement(
							'td',
							null,
							React.createElement('input', { type: 'text', 'class': 'form-control',
								value: value,
								onChange: this.updateString.bind(this, name) })
						);
					} else {
						showMsg('data corrupted?');
					}

					return React.createElement(
						'tr',
						null,
						React.createElement(
							'td',
							null,
							' ',
							prop['name'],
							' '
						),
						tdInput
					);
				}
			}, this);

			ui = React.createElement(
				'div',
				null,
				React.createElement(
					'div',
					{ className: 'panel panel-primary' },
					React.createElement(
						'div',
						{ className: 'panel-heading' },
						React.createElement(
							'h3',
							{ className: 'panel-title' },
							device['name']
						)
					),
					React.createElement(
						'div',
						{ className: 'panel-body' },
						React.createElement(
							'div',
							{ className: 'row' },
							' ',
							device['description'],
							' '
						),
						React.createElement(
							'div',
							{ className: 'row' },
							React.createElement(
								'table',
								{ className: 'table' },
								React.createElement(
									'thead',
									null,
									' ',
									React.createElement(
										'tr',
										null,
										React.createElement(
											'td',
											null,
											' name '
										),
										React.createElement(
											'td',
											null,
											' value '
										)
									),
									' '
								),
								React.createElement(
									'tbody',
									null,
									formUi
								)
							)
						)
					)
				),
				React.createElement(
					'div',
					null,
					React.createElement(
						'span',
						{ className: 'btn btn-primary', onClick: this.applyChange },
						'Apply'
					)
				)
			);
		}

		var controlBtn = React.createElement(
			'div',
			{ className: 'row' },
			React.createElement(
				'div',
				{ className: 'input-group' },
				React.createElement(
					'span',
					{ className: 'input-group-addon' },
					'Control:',
					React.createElement('input', { type: 'checkbox', 'aria-label': 'control', checked: control,
						onChange: this.handleControlToggle })
				)
			)
		);

		return React.createElement(
			'div',
			null,
			React.createElement(
				'div',
				{ className: 'row' },
				' ',
				controlBtn,
				' '
			),
			React.createElement(
				'div',
				{ className: 'row' },
				' ',
				ui,
				' '
			)
		);
	}

});

