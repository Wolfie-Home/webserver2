'use strict';

var DeviceView = React.createClass({
	displayName: 'DeviceView',


	getInitialState: function () {
		return {
			'currentDeviceId': undefined,
			'devices': {},
			'control': false
		};
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
				'currentDeviceId': deviceSelectedStore.getDeviceId()
			});
		}.bind(this);

		deviceStore.registerDeviceDetailAdded(deviceAdded);
		deviceSelectedStore.registerDeviceSelected(deviceSelected);
	},

	handleControlToggle: function (event) {
		this.setState({
			'control': event.target.checked
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
			ui = React.createElement(
				'div',
				null,
				' not yet.. '
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
					React.createElement('input', { type: 'checkbox', 'aria-label': 'control', onChange: this.handleControlToggle })
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

