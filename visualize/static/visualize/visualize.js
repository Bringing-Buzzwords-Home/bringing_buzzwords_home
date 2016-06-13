function drawStateDeaths(data){
    nv.addGraph(function() {
        var chart = nv.models.discreteBarChart()
            .x(function(d) { return d.label })
            .y(function(d) { return d.value })
            .staggerLabels(true)
            //.staggerLabels(historicalBarChart[0].values.length > 8)
            .showValues(true)
            .duration(250)
            ;

            d3.select('#top-right svg')
                .datum(data.state_deaths)
                .call(chart);

            nv.utils.windowResize(chart.update);
            return chart;
        })}

function drawPerCapitaAssaultRifles(data){
      nv.addGraph(function() {
          chart = nv.models.multiBarChart()
            .duration(300)
            .margin({bottom: 100, left: 70})
            .rotateLabels(45)
            .groupSpacing(0.1)
          ;
          chart.reduceXTicks(false).staggerLabels(true);
          chart.xAxis
            .axisLabel("Categories")
            .axisLabelDistance(35)
            .showMaxMin(false)
            .tickValues(data.per_capita_nums)
            .tickFormat(function (d){
                console.log(data.per_capita_rifles[0].values[d].label)
                return data.per_capita_rifles[0].values[d].label;
            })
          ;
          chart.yAxis
            .axisLabel("Per Capita Guns and Knives")
            .axisLabelDistance(-5)
            .tickFormat(d3.format(',.01e'))
          ;
          chart.dispatch.on('renderEnd', function(){
            nv.log('Render Complete');
          });
          d3.select('#top-right svg')
            .datum(data.per_capita_rifles)
            .call(chart);
          nv.utils.windowResize(chart.update);
          chart.dispatch.on('stateChange', function(e) {
            nv.log('New State:', JSON.stringify(e));
          });
          chart.state.dispatch.on('change', function(state){
            nv.log('state', JSON.stringify(state));
          });
   })}

function drawCategories(data){
   nv.addGraph(function (){
       chart = nv.models.multiBarChart()
         .duration(300)
         .margin({bottom: 100, left: 70})
         .rotateLabels(45)
         .groupSpacing(0.1)
       ;
       chart.reduceXTicks(false).staggerLabels(true);
       chart.xAxis
         .axisLabel("Categories")
         .axisLabelDistance(35)
         .showMaxMin(false)
         .tickValues(data.category_nums)
         .tickFormat(function (d){
             console.log(data.category_data[0].values[d].label)
             return data.category_data[0].values[d].label;
         })
       ;
       chart.yAxis
         .axisLabel("Number of Items")
         .axisLabelDistance(-5)
         .tickFormat(d3.format(',.01f'))
       ;
       chart.dispatch.on('renderEnd', function(){
         nv.log('Render Complete');
       });
       d3.select('#middle-right svg')
         .datum(data.category_data)
         .call(chart);
       nv.utils.windowResize(chart.update);
       chart.dispatch.on('stateChange', function(e) {
         nv.log('New State:', JSON.stringify(e));
       });
       chart.state.dispatch.on('change', function(state){
         nv.log('state', JSON.stringify(state));
       });
})};

function drawLineDeaths(data){
    nv.addGraph(function() {
   chart = nv.models.lineChart()
       .options({
           duration: 300,
           useInteractiveGuideline: true
       })
   ;
   // chart sub-models (ie. xAxis, yAxis, etc) when accessed directly, return themselves, not the parent chart, so need to chain separately
   chart.xAxis
       .axisLabel("Months")
       .tickFormat(function (d){
             return d3.time.format('%B %Y')(new Date(d))
       })
       .staggerLabels(true)
   ;
   chart.yAxis
       .axisLabel('Deaths')
       .tickFormat(function(d) {
           if (d == null) {
               return 'N/A';
           }
           return d3.format(',.2f')(d);
       })
   ;

   d3.select('#top-left').append('svg')
       .datum(data.deaths_over_time)
       .call(chart);
   nv.utils.windowResize(chart.update);
   return chart;
})}

function drawLineDollars(data){
     nv.addGraph(function() {
    chart = nv.models.lineChart()
        .options({
            duration: 300,
            useInteractiveGuideline: true
        })
    ;
    // chart sub-models (ie. xAxis, yAxis, etc) when accessed directly, return themselves, not the parent chart, so need to chain separately
    chart.xAxis
        .axisLabel("Years")
        .tickFormat(function (d){
            console.log(data.dollars_by_year[0].values[d].label)
            return data.dollars_by_year[0].values[d].label;
        })
        .staggerLabels(true)
    ;
    chart.yAxis
        .axisLabel('$ Value Donated')
        .tickFormat(function(d) {
            if (d == null) {
                return 'N/A';
            }
            return d3.format(',.2f')(d);
        })
    ;

    d3.select('#top-left').append('svg')
        .datum(data.dollars_by_year)
        .call(chart);
    nv.utils.windowResize(chart.update);
    return chart;
})}

function drawPerCapitaCategories(data){
    nv.addGraph(function() {
  chart = nv.models.multiBarChart()
      .duration(300)
      .margin({bottom: 100, left: 70})
      .rotateLabels(45)
      .groupSpacing(0.1)
  ;
  chart.reduceXTicks(false).staggerLabels(true);
  chart.xAxis
      .axisLabel("Categories")
      .axisLabelDistance(35)
      .showMaxMin(false)
      .tickValues(data.category_nums)
      .tickFormat(function (d){
          console.log(data.categories_per_capita[0].values[d].label)
          return data.categories_per_capita[0].values[d].label;
      })
  ;
  chart.yAxis
      .axisLabel("Per Capita Number of Items")
      .axisLabelDistance(-5)
      .tickFormat(d3.format(',.01e'))
  ;
  chart.dispatch.on('renderEnd', function(){
      nv.log('Render Complete');
  });
  d3.select('#middle-left svg')
      .datum(data.categories_per_capita)
      .call(chart);
  nv.utils.windowResize(chart.update);
  chart.dispatch.on('stateChange', function(e) {
      nv.log('New State:', JSON.stringify(e));
  });
  chart.state.dispatch.on('change', function(state){
      nv.log('state', JSON.stringify(state));
  });
  })}

function drawAvgViolentCrime(data){
    nv.addGraph(function() {
        var chart = nv.models.discreteBarChart()
            .x(function(d) { return d.label })
            .y(function(d) { return d.value })
            .staggerLabels(true)
            //.staggerLabels(historicalBarChart[0].values.length > 8)
            .showValues(true)
            .duration(250)
            ;
            chart.yAxis
                .axisLabel('Violent Crime')
            d3.select('#top-right svg')
                .datum(data.avg_violent_crime)
                .call(chart);

            nv.utils.windowResize(chart.update);
            return chart;
        })}

function drawPerCapitaViolentCrime(data){
    nv.addGraph(function() {
        var chart = nv.models.discreteBarChart()
            .x(function(d) { return d.label })
            .y(function(d) { return d.value })
            .staggerLabels(true)
            //.staggerLabels(historicalBarChart[0].values.length > 8)
            .showValues(true)
            .duration(250)
            ;
            chart.yAxis
                .axisLabel('Violent Crime')
                .tickFormat(d3.format(',.01e'))
            d3.select('#top-left svg')
                .datum(data.per_capita_violent_crime)
                .call(chart);

            nv.utils.windowResize(chart.update);
            return chart;
        })}

function drawAvgPropertyCrime(data){
    nv.addGraph(function() {
        var chart = nv.models.discreteBarChart()
            .x(function(d) { return d.label })
            .y(function(d) { return d.value })
            .staggerLabels(true)
            //.staggerLabels(historicalBarChart[0].values.length > 8)
            .showValues(true)
            .duration(250)
            ;
            chart.yAxis
                .axisLabel('Property Crime')
            d3.select('#top-right svg')
                .datum(data.avg_property_crime)
                .call(chart);

            nv.utils.windowResize(chart.update);
            return chart;
        })}

function drawPerCapitaPropertyCrime(data){
    nv.addGraph(function() {
        var chart = nv.models.discreteBarChart()
            .x(function(d) { return d.label })
            .y(function(d) { return d.value })
            .staggerLabels(true)
            //.staggerLabels(historicalBarChart[0].values.length > 8)
            .showValues(true)
            .duration(250)
            ;
            chart.yAxis
                .axisLabel('Property Crime')
                .tickFormat(d3.format(',.01e'))
            d3.select('#top-left svg')
                .datum(data.per_capita_property_crime)
                .call(chart);

            nv.utils.windowResize(chart.update);
            return chart;
        })}
// d3.json("{% url 'state_json' state %}", function(error, json) {
//   if (error) return console.warn(error);
//   data = json;
//   drawCategories(data)
//   drawLineDeaths(data)
//   drawLineDollars(data)
//   drawPerCapitaCategories(data)
//   drawCrimeCategories(data)
//   drawPerCapitaAssaultRifles(data)
//
// });
