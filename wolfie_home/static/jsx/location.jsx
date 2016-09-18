window.WolfieHomeLocation = window.WolfieHomeLocation || {};


//  @state, json object:
//  @path, an order list for representing a path.
//  @button, string display for the button.
//  @data, according to ChaoNestedListUi data structure.
WolfieHomeLocation.LocationView = React.createClass({
    getInitialState: function() {
       return  {
            'path': ['sushi paradise'],
            'button': 'Create',
            'data': {
                'name': 'sushi paradise',
                'list': [
                {
                    'name': 'sushi',
                    'list': [
                    {
                        'name': 'cali roll',          
                        'list': null
                    },
                    {
                        'name': 'boston roll',
                        'list': null
                    }
                    ]
                },
                {
                    'name': 'spicy food',
                    'list': [
                    {
                        'name': 'thai',
                        'list': null
                    },
                    {
                        'name': 'szuan',
                        'list': null
                    }
                    ],
                }
                ],
            }
        };
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

    clickOnButton: function() {
        // TODO
    },

    render: function() {
        var path = this.state.path;
        var data = this.state.data;
        var buttonName = this.state.button;
    
        // building breadcrumb
        curPath = [];
        breadcrumbUi = [];
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
        var list = [data];
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

        // button 
        var buttonUi = (
            <button className="btn btn-primary" style={{'margin-top':'10px'}}>
            {buttonName}
            </button>
        );
    
        return (
            <div className="container">
                {breadcrumbUi}
                {listUiContainer}
                {buttonUi}
            </div>
        );
    }
    
});


ReactDOM.render(
    <WolfieHomeLocation.LocationView />,
    document.getElementById('main')
);
