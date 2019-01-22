var PageHeader = ReactBootstrap.PageHeader;
var FormControl = ReactBootstrap.FormControl;
var ButtonGroup = ReactBootstrap.ButtonGroup;
var InputGroup = ReactBootstrap.InputGroup;
var FormGroup = ReactBootstrap.FormGroup;
var MenuItem= ReactBootstrap.MenuItem;
var Button = ReactBootstrap.Button;
var ButtonInput = ReactBootstrap.ButtonInput;
var SplitButton = ReactBootstrap.SplitButton;
var DropdownButton = ReactBootstrap.DropdownButton;
var Router = ReactRouter.Router;
var Route = ReactRouter.Route;
var Dispatcher = function() {};

var obf = function(the_text) {
  console.log("Original title: " + the_text);
  var new_string = "";
  for (var ii = 0, len = the_text.length; ii < len; ii++) {
    if (ii == 0) {
      new_string += the_text[ii];
    } else {
      new_string += "*";
    }
  }
  console.log("Revised title: " + new_string);
  return new_string;
}

var suggest = function(the_text) {
    console.log(the_text);
}

var Header = React.createClass({
    render: function() {
        return <PageHeader id="header"><b>risk map</b></PageHeader>;
    }
});

class LeadSelector extends React.Component {
    constructor(props) {
        super(props);
        this.setLead10 = this.setLead10.bind(this);
        this.setLead60 = this.setLead60.bind(this);
        this.setLead600 = this.setLead600.bind(this);
    }

    setLead10() {
        this.props.updateLead(10);
    }

    setLead60() {
        this.props.updateLead(60);
    }

    setLead600() {
        this.props.updateLead(600);
    }

  render() {
    return (<ButtonGroup>
      <Button onClick={this.setLead10} bsClass="leadbutton">10 Seconds</Button><br></br>
      <Button onClick={this.setLead60} bsClass="leadbutton">1 Minute</Button><br></br>
      <Button onClick={this.setLead600} bsClass="leadbutton">10 Minutes</Button><br></br>
      </ButtonGroup>
    )
  }
}

class MonthSelector extends React.Component {
    constructor(props) {
        super(props);
        this.handleSelect = this.handleSelect.bind(this);
        this.state = {month: props.month};
        this.months = {1: "2016 Jan" };

    }

  handleSelect(eventKey) {
    var newMonth = this.months[eventKey];
    this.setState({month: newMonth});
    this.props.updateMonth(newMonth);
  }

  render() {
    return (
    <DropdownButton title={this.state.month} id="month-select" onSelect={this.handleSelect}>
      <MenuItem bsClass="menuItem" eventKey="1">2016 Jan</MenuItem>
      /*<MenuItem eventKey="2">2016 Feb</MenuItem>
      <MenuItem eventKey="3">2016 Mar</MenuItem>
      <MenuItem eventKey="4">2016 Apr</MenuItem>
      <MenuItem eventKey="5">2016 May</MenuItem>
      <MenuItem eventKey="6">2016 Jun</MenuItem>
      <MenuItem eventKey="7">2016 Jul</MenuItem>
      <MenuItem eventKey="8">2016 Aug</MenuItem>
      <MenuItem eventKey="9">2016 Sep</MenuItem>
      <MenuItem eventKey="10">2016 Oct</MenuItem>
      <MenuItem eventKey="11">2016 Nov</MenuItem>

      <MenuItem eventKey="12">2016 Dec</MenuItem>*/
    </DropdownButton>)
  }
}


class TickerInfoContainer extends React.Component {
    constructor(props) {
        super(props);
        this.displayMeta = this.displayMeta.bind(this);
    }

    displayMeta() {
        if (this.props.hasOwnProperty('data')) {
            if (this.props.data != undefined) {
                return (<div className="metaDisplay">
                            <div className="display-inner">
                                <h2>{this.props.data.Name} ({this.props.data.ticker})</h2>
                                <div className="metaProperty">{this.props.data.Sector}, &nbsp; </div>
                                <div className="metaProperty">{this.props.data.Industry}, &nbsp; </div>
                                <div className="metaProperty">IPO Year: {this.props.data.IPOYear}</div>
                            </div>
                        </div>);
            } else {
                return (<div className="metaDisplay"></div>);
            }
        } else {
            return "";
        }
    }

    render() {
        return (this.displayMeta());
    }

}

class CausalityContainer extends React.Component {
    constructor(props) {
        super(props);
        this.displayTickers = this.displayTickers.bind(this);
        this.getTableElClass = this.getTableElClass.bind(this);
        if (!this.props.hasOwnProperty('data')) {
            this.state = {data: null};
        } else {
            this.state = {data: this.props.data}
        }
    }

    getTableElClass(val) {
        if (val === 1.0) {
            return "gc-yes";
        } else {
            return "gc-no";
        }
    }

    displayTickers() {
        var that = this;
        if (this.props.hasOwnProperty('data')) {
            if (this.props.data != null) {
                return (
                        <table className="CauserList">
                        <tbody>
                        <tr>
                            <th></th>
                            <th className="gc-header">Lag 1</th>
                            <th className="gc-header">Lag 2</th>
                            <th className="gc-header">Lag 3</th>
                            <th className="gc-header">Lag 4</th>
                            <th className="gc-header">Lag 5</th>
                        </tr>
                    {this.props.data.map( function(it) {
                        return (<tr key={it.causer}>
                                  <th className="causer-label">{it.causer}</th>
                                  <th className={that.getTableElClass(it.lag1)}>{it.lag1}</th>
                                  <th className={that.getTableElClass(it.lag2)}>{it.lag2}</th>
                                  <th className={that.getTableElClass(it.lag3)}>{it.lag3}</th>
                                  <th className={that.getTableElClass(it.lag4)}>{it.lag4}</th>
                                  <th className={that.getTableElClass(it.lag5)}>{it.lag5}</th>
                                </tr>);
                    })}
                    </tbody>
                    </table>);
            } else {
                return "null";
            }
        } else {
            return "null";
        }
    }


    displayData() {
        if (this.state.data === null) {
            return null;
        } else {
            return this.state.data;
        }
    }

    render() {
        if (this.props.data != null ) {
            return (<div>
                  <div className="causerDisplay">
                        <div className="display-inner">
                        <h3 className="display-title">attack vectors</h3>
                        {this.displayTickers()}
                        </div>
                        </div>
                </div>);
        } else {
            return (<div></div>);
        }
    }
}

class CauserMPContainer extends React.Component {
    constructor(props) {
        super(props);
        this.displayChart = this.displayChart.bind(this);
        this.displayMagnitudes = this.displayMagnitudes.bind(this);
        this.displayTitle = this.displayTitle.bind(this);
        if (!this.props.hasOwnProperty('data')) {
            this.state = {data: null};
        } else {
            this.state = {data: this.props.data}
        }
    }
    componentDidMount() {
        this.displayChart();
        this.displayMagnitudes();
    }

    componentWillReceiveProps() {
        //this.displayChart();
    }
    componentDidUpdate() {
        this.displayChart();
        this.displayMagnitudes();
    }
   displayMagnitudes() {
        if (this.props.hasOwnProperty('data') ) {
            if (this.props.data != null) {
                var lbls = ['lag1','lag2','lag3','lag4','lag5'];
                var b = this.props.beta;
                var srs = [b.beta1, b.beta2, b.beta3, b.beta4, b.beta5];
                // The below is a way to get more data on the color she bar should be.  It is a little hacky because it relies on the betas being unique.  Also, uses ES6
                var srs_dict = {[b.beta1]: b.lag1, [b.beta2]:b.lag2, [b.beta3]: b.lag3, [b.beta4]:b.lag4, [b.beta5]:b.lag5};
                var el_id = "#causer-"+this.displayTitle() + "-magnitude";
                var the_chart = new Chartist.Bar(el_id,{
                    labels: lbls,
                    series: [srs]});
                the_chart.on("draw", function(context) {
                    //console.log(context);
                    if (context.type === "bar") {
                        var sig = srs_dict[context.value.y];
                        //console.log(sig);
                        if (sig === 1) {
                            //console.log("Thinks it is 1");
                            context.element.attr({
                                style: 'stroke: rgba(150,0,0,1.0);'
                            });
                        } else {
                            //console.log("Thinks it is 0");
                            context.element.attr({
                                style: 'stroke: rgba(255,255,255,1.0);'
                            });
                        }
                    }
                });
            } else {
                return "";
            }
        } else {
            return "";
        }

    }

    displayChart() {
        if (this.props.hasOwnProperty('data') & this.props.data != null) {
            var not_explained = 1 - this.props.data;
            var the_class = "#causer-" + this.props.ticker;
            var the_chart = new Chartist.Pie(the_class,{
                series: [this.props.data, not_explained]
                },
                {labelInterpolationFnc: function(value) {
                    //return value;
                    return Math.round(value * 100);
                },
                donut: true,
                donutWidth: 20
            });
            the_chart.on('draw', function(ctx) {
              if (ctx.type === 'label') {
                if (ctx.index === 0) {
                  //console.log(ctx.text);
                  ctx.text = Math.round(ctx.text*100);
                  //console.log(ctx.text);
                  ctx.element.attr({
                    dx: ctx.element.root().width()/2,
                    dy: ctx.element.root().height()/2
                  });
                } else {

                  ctx.element.remove();
                }
              }
            });
        } else {
            return "";
        }

    }

    displayTitle() {
        if (this.props.hasOwnProperty('data') ) {
            if (this.props.data != null) {
              // return this.props.ticker;
                return this.props.ticker;
            } else {
                return "";
            }
        } else {
            return "";
        }
    }

    displayRank() {
        if (this.props.hasOwnProperty('data') ) {
            if (this.props.data != null) {
                return this.props.rank;
            } else {
                return "";
            }
        } else {
            return "";
        }


    }

    render() {
        return (<div className="causer-midpoint-outer">
                    <div className="display-inner">
                    <h4 className="causer-label">{this.displayTitle()}</h4>
                    <div className="causer-midpoint-chart" id={"causer-" + this.displayTitle()}></div>
                    <div className="magnitude-chart" id={"causer-" + this.displayTitle() + "-magnitude"}></div>
                    </div>
                </div>);
    }
}


class MagnitudeContainer extends React.Component {
    constructor(props) {
        super(props);
        this.displayChart= this.displayChart.bind(this);
        this.displayTitle = this.displayTitle.bind(this);
        this.causerShapeData = this.causerShapeData.bind(this);
        this.causerTicker = this.causerTicker.bind(this);
        this.causerBeta= this.causerBeta.bind(this);
        if (!this.props.hasOwnProperty('data')) {
            this.state = {data: null};
        } else {
            this.state = {data: this.props.data}
        }
    }
    componentDidMount() {
        //this.displayChart();
    }

    componentWillReceiveProps() {
        this.displayChart();
    }

    componentDidUpdate() {
        this.displayChart();
    }

    displayChart() {
        if (this.props.hasOwnProperty('data') ) {
            if (this.props.data != null) {
                var lbls = ['lag1','lag2','lag3','lag4','lag5'];
                var b = this.props.data[0];
                if (b!=null) {
                   var srs = [b.beta1, b.beta2, b.beta3, b.beta4, b.beta5];

                  new Chartist.Bar('.magnitude-chart',{
                    labels: lbls,
                    series: [srs]});
                } else {
                    console.log(this.props.data);
                    console.log("No betas")
                }
            } else {
                return "";
            }
        } else {
            return "";
        }

    }

    displayTitle() {
        if (this.props.hasOwnProperty('data') ) {
            if (this.props.data != null) {
                return "Vectors";
            } else {
                return "";
            }
        } else {
            return "";
        }
    }
    causerBeta(cc) {
        if (this.props.hasOwnProperty('data') ) {
            if (this.props.data != null) {
                return this.props.data[cc];
            } else {
                return "";
            }
        } else {
            return "";
        }
    }

    causerShapeData(cc) {
        if (this.props.hasOwnProperty('data') ) {
            if (this.props.data != null) {
                return this.props.data[cc].causer_shape;
            } else {
                return "";
            }
        } else {
            return "";
        }
    }
    causerTicker(cc) {
        if (this.props.hasOwnProperty('data') ) {
            if (this.props.data != null) {
                return this.props.data[cc].causer;
            } else {
                return "";
            }
        } else {
            return "";
        }
    }


    render() {
        this.displayChart();
        if (this.props.hasOwnProperty('data')) {
            if (this.props.data != null) {
                return (<div className="magnitude-outer">
                            <div className="display-inner">
                            <h2 id="vector-title">{this.displayTitle()}</h2>
                            <CauserMPContainer data={this.causerShapeData(0)} ticker={this.causerTicker(0)} beta={this.causerBeta(0)}/>
                            <CauserMPContainer data={this.causerShapeData(1)} ticker={this.causerTicker(1)} beta={this.causerBeta(1)}/>
                            <CauserMPContainer data={this.causerShapeData(2)} ticker={this.causerTicker(2)} beta={this.causerBeta(2)}/>
                            <CauserMPContainer data={this.causerShapeData(3)} ticker={this.causerTicker(3)} beta={this.causerBeta(3)}/>
                            <CauserMPContainer data={this.causerShapeData(4)} ticker={this.causerTicker(4)} beta={this.causerBeta(4)}/>
                            <div className="magnitude-chart"></div>
                            </div>
                        </div>);
            } else {
                return null;
            }
        } else {
            return null;
        }
    }
}

class VolatilityContainer extends React.Component {
    constructor(props) {
        super(props);
        this.displayChart = this.displayChart.bind(this);
        this.displayTitle = this.displayTitle.bind(this);
        if (!this.props.hasOwnProperty('data')) {
            this.state = {data: null};
        } else {
            this.state = {data: this.props.data}
        }
    }
    componentDidMount() {
        //this.displayChart();
    }

    componentWillReceiveProps() {
        this.displayChart();
    }

    displayChart() {
        if (this.props.hasOwnProperty('data') & this.props.data != null) {
            //console.log(this.props.data);
            var not_explained = 1 - this.props.data.r_squared;
            //console.log(not_explained);
            var the_chart = new Chartist.Pie('.volatility-chart',{
                series: [this.props.data.r_squared, not_explained],
                },
                {labelInterpolationFnc: function(value) {
                    return Math.round(value * 100);
                },
                donut: true,
                donutWidth: 30

            });
            the_chart.on('draw', function(ctx) {
              if (ctx.type === 'label') {
                if (ctx.index === 0) {
                  //console.log(ctx.text);
                  ctx.text = Math.round(ctx.text*100);
                  //console.log(ctx.text);
                  ctx.element.attr({
                    dx: ctx.element.root().width()/2,
                    dy: ctx.element.root().height()/2
                  });
                } else {

                  ctx.element.remove();
                }
              }
            });




        } else {
            return "";
        }

    }

    displayTitle() {
        if (this.props.hasOwnProperty('data') ) {
            if (this.props.data != null) {
                return "Shape and Volatility";
            } else {
                return "";
            }
        } else {
            return "";
        }
    }

    render() {
        this.displayChart();
        return (<div className="volatility-outer">
                    <div className="display-inner">
                      <div className="donut-display">
                        <h4 className="data-title">{this.displayTitle()}</h4>
                        <div className="volatility-chart"></div>
                      </div>
                    </div>
                </div>);
    }
}

class MidpointContainer extends React.Component {
    constructor(props) {
        super(props);
        this.displayChart = this.displayChart.bind(this);
        this.displayTitle = this.displayTitle.bind(this);
        if (!this.props.hasOwnProperty('data')) {
            this.state = {data: null};
        } else {
            this.state = {data: this.props.data}
        }
    }
    componentDidMount() {
        //this.displayChart();
    }

    componentWillReceiveProps() {
        this.displayChart();
    }

    displayChart() {
        if (this.props.hasOwnProperty('data') & this.props.data != null) {
            //console.log(this.props.data);

            var not_explained = 1 - this.props.data.r_squared;
            //console.log(not_explained);
            var the_chart = new Chartist.Pie('.midpoint-chart',{
                series: [this.props.data.r_squared, not_explained],
                },
                {labelInterpolationFnc: function(value) {
                    return Math.round(value * 100);
                },
                donut: true,
                donutWidth: 30
            });
            the_chart.on('draw', function(ctx) {
              if (ctx.type === 'label') {
                if (ctx.index === 0) {
                  //console.log(ctx.text);
                  ctx.text = Math.round(ctx.text*100);
                  //console.log(ctx.text);
                  ctx.element.attr({
                    dx: ctx.element.root().width()/2,
                    dy: ctx.element.root().height()/2
                  });
                } else {

                  ctx.element.remove();
                }
              }
            });

        } else {
            return "";
        }

    }

    displayTitle() {
        if (this.props.hasOwnProperty('data') ) {
            if (this.props.data != null) {
                return "Shape and Future Price";
            } else {
                return "";
            }
        } else {
            return "";
        }
    }

    displayMPD() {
        if (this.props.hasOwnProperty('data') ) {
            if (this.props.data != null) {
                return Math.round((this.props.data.num_messages/this.props.data.num_days)).toLocaleString();
            } else {
                return "";
            }
        } else {
            return "";
        }
    }

    displayMPDTitle() {
        if (this.props.hasOwnProperty('data') ) {
            if (this.props.data != null) {
                return "Messages/day";
            } else {
                return "";
            }
        } else {
            return "";
        }
    }



    render() {
        this.displayChart();
        return (<div className="display-inner">
                      <div id="midpoint-outer">
                        <h4 className="data-title">{this.displayTitle()}</h4>
                        <div className="midpoint-chart"></div>
                      </div>
                    </div>);
    }
}


class MPDDisplayContainer extends React.Component {
  constructor(props) {
      super(props);
      this.displayMPD = this.displayMPD.bind(this);
      this.displayMPDTitle = this.displayMPDTitle.bind(this);
      if (!this.props.hasOwnProperty('data')) {
          this.state = {data: null};
      } else {
          this.state = {data: this.props.data}
      }
  }

  displayMPD() {
      if (this.props.hasOwnProperty('data') ) {
          if (this.props.data != null) {
              return Math.round((this.props.data.num_messages/this.props.data.num_days)).toLocaleString();
          } else {
              return "";
          }
      } else {
          return "";
      }
  }

  displayMPDTitle() {
      if (this.props.hasOwnProperty('data') ) {
          if (this.props.data != null) {
              return "Messages/day";
          } else {
              return "";
          }
      } else {
          return "";
      }
  }

  render() {
      return (
                  <div className="display-inner">
                    <div id="mpd-display">
                      <h4 className="data-title">{this.displayMPDTitle()}</h4>
                      <div className="mpd">{this.displayMPD()}</div>
                    </div>
                  </div>);
  }

}


class SearchBox extends React.Component {
  constructor(props) {
    super(props);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.handleInputChange = this.handleInputChange.bind(this);
    this.state = {inputValue: ''}
  }
  handleInputChange(e) {
      this.setState({inputValue: e.target.value});
  }
  handleSubmit(e) {
    this.props.updateTicker(this.state.inputValue);
  }
  render() {
    return (<div>
            <FormGroup>
              <InputGroup>
                <FormControl bsClass="searchboxclass" id="searchbox" value={this.state.inputValue} onSubmit={this.handleSubmit} onChange={this.handleInputChange} type="search" onKeyPress={event => {
                  if (event.key === 'Enter') {
                    this.handleSubmit();
                  }
                }
              }

                />
                <Button type="submit" onClick={this.handleSubmit} bsClass="searchbutton">search</Button>
              </InputGroup>
            </FormGroup>
            </div>)    ;
  }
}

class RSquaredGraph extends React.Component {
    constructor(props){
        super(props);
        this.displayChart = this.displayChart.bind(this);
        this.displayTitle = this.displayTitle.bind(this);
        if (!this.props.hasOwnProperty('data')) {
                this.state = {data: null};
        console.log("data set to null");    
            } else {
                this.state = {data: this.props.data}
            }
    }
    componentDidMount(){
    //this.displayChart();
    }

    componentWillReceiveProps() {
        this.displayChart();
    }

    displayTitle() {
        if (this.props.hasOwnProperty('data') ) {
            if (this.props.data != null) {
                return "Magnitude and persistance of shape effect";
            } else {
                return "";
            }
        } else {
            return "";
        }
    }

//Function that displays the chart with the inputted two dimensional array
//labeled from 0-1 by one-tenth increments 
displayChart() {
if(this.props.hasOwnProperty('data') ){
    if(this.props.data != null){

//series is what is being plotted
var srs = this.props.data.rsq2;
var means = srs[0];
var stddev = srs[1];
var lead = this.props.data.le;
var point = this.props.data.met;
var tick;

//depending on our lead time pulls the point of the ticker from meta
if(lead == 10){
    tick = [{x: point.r2mean10, y: point.r2std10}];
}
else if(lead == 60){
    tick = [{x: point.r2mean60, y: point.r2std60}];
}
else if(lead == 600){
    tick = [{x: point.r2mean600, y: point.r2std600}];
}
var data_chart = {
  labels: [],
  series: [
        [],
        tick
    ]
};

//essentially zips the two arrays
  for (var i = 0; i < means.length; i += 1)
  {
    var in_val = {x: means[i], y: stddev[i]}
    data_chart.series[0].push(in_val);
}
  
//options for the drawing of the graph
var options = {
  axisX: {
    type: Chartist.AutoScaleAxis
  },
  showLine: false,
  width: '1000px',
  height: '200px'
};

//line where the new chart is created. First parameter is name of class corresponding to 
//output div
new Chartist.Line('.rsquared-chart', data_chart, options);
            } else {
                return "";
            }
        } else {
            return "";
        }
}

        render(){
        this.displayChart();
        return(
            <div className = "display-inner">
                <div id="mpd-display">
                     <h4 className ="data-title">{this.displayTitle()}</h4>
                <div className ="rsquared-chart"> </div>
                </div>
            </div>
            );
        }
}

class ManipApp extends React.Component {
    constructor(props) {
        super(props);
        this.updateMonth = this.updateMonth.bind(this);
        this.updateLead = this.updateLead.bind(this);
        this.updateTicker = this.updateTicker.bind(this);
        this.handleDbResponse = this.handleDbResponse.bind(this);
        this.state = {lead: 60,
                      month: "2016 Jan",
                      ticker: null,
                      data: null,};
    }
    updateMonth(new_month) {
        this.setState({month: new_month});
    }
    updateLead(new_lead) {
        this.setState({lead: new_lead});
    }
    handleDbResponse(resp) {
        var that = this;
        var stateMonth = this.state.month.substring(5).toUpperCase();
        function correctMonth(val) {
            var this_month = val.month.substring(0,3).toLowerCase();
	    //var month_names = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'};
	    //var right_month = month_names[this_month]; 
	    
            return this_month === stateMonth;
        }
        resp.json().then(function(dt) {
        console.log(dt);
            var arr = dt.data;
            var the_meta = dt.meta;
	    var out = arr.filter(correctMonth);
            var manip_rank = dt.manip_rank;
        var rsq = {rsq2: dt.rsqrd, le: that.state.lead, met: the_meta};
            that.setState({rsquare: rsq, data: arr, meta: the_meta, volatility: dt.vol, midpoint: dt.midpoint, manip_rank: dt.manip_rank});
        });
    }
    updateTicker(new_ticker) {
        var the_month = this.state.month.substring(5).toUpperCase();
        var query = new_ticker + "/" + the_month + "/" + this.state.lead;
        fetch('http://127.0.0.1:8888/ticker/' + query, {method: 'get'}).then(this.handleDbResponse);
    }
    render() {
        return (<div>
                    <Header/>
                    <SearchBox updateTicker={this.updateTicker}/>
                    <LeadSelector updateLead={this.updateLead}/>
                    <MonthSelector month={this.state.month} updateMonth={this.updateMonth}/>
                    <div className="contentWrapper">
                      <TickerInfoContainer data={this.state.meta}/>
                      <MPDDisplayContainer data={this.state.midpoint}/>
                      <MidpointContainer data={this.state.midpoint}/>
                      <VolatilityContainer data={this.state.volatility}/>
                      <RSquaredGraph data={this.state.rsquare}/>
                      <MagnitudeContainer data={this.state.data}/>
                    </div>
                </div>);
    }
}

//<CausalityContainer data={this.state.data}/>



ReactDOM.render(
        <ManipApp/>,
        document.getElementById('content')
);

