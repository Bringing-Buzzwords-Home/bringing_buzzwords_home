function drawAvgPropCrime(prop_crime){
      nv.addGraph(function() {
          var chart = nv.models.multiBarChart()
              .barColor(d3.scale.category20().range())
              .duration(300)
              .margin({bottom: 50, left: 70})
              .groupSpacing(0.1)
              ;
          chart.reduceXTicks(false);
          chart.xAxis
              .axisLabel("Crime Categories")
              .axisLabelDistance(35)
              .showMaxMin(false)
              .tickFormat(function (d){
                  console.log(prop_crime[0].values[d].label)
                  return prop_crime[0].values[d].label;
              })
          ;
          chart.yAxis
              .axisLabel("# of Crimes")
              .axisLabelDistance(-5)
              .tickFormat(d3.format(',f'))
          ;
          chart.dispatch.on('renderEnd', function(){
              nv.log('Render Complete');
          });
          d3.select('#top-left svg')
              .datum(prop_crime)
              .call(chart);
          nv.utils.windowResize(chart.update);
          chart.dispatch.on('stateChange', function(e) {
              nv.log('New State:', JSON.stringify(e));
          });
          chart.state.dispatch.on('change', function(state){
              nv.log('state', JSON.stringify(state));
  });
})};


function drawAvgPropCrimePerCap(prop_crime_per_cap){
      nv.addGraph(function() {
          var chart = nv.models.multiBarChart()
              .barColor(d3.scale.category20().range())
              .duration(300)
              .margin({bottom: 50, left: 70})
              .groupSpacing(0.1)
              ;
          chart.reduceXTicks(false);
          chart.xAxis
              .axisLabel("Crime Categories")
              .axisLabelDistance(35)
              .showMaxMin(false)
              .tickFormat(function (d){
                  console.log(prop_crime_per_cap[0].values[d].label)
                  return prop_crime_per_cap[0].values[d].label;
              })
          ;
          chart.yAxis
              .axisLabel("# of Crimes Per Capita")
              .axisLabelDistance(-5)
              .tickFormat(d3.format(',.01e'))
          ;
          chart.dispatch.on('renderEnd', function(){
              nv.log('Render Complete');
          });
          d3.select('#top-right svg')
              .datum(prop_crime_per_cap)
              .call(chart);
          nv.utils.windowResize(chart.update);
          chart.dispatch.on('stateChange', function(e) {
              nv.log('New State:', JSON.stringify(e));
          });
          chart.state.dispatch.on('change', function(state){
              nv.log('state', JSON.stringify(state));
  });
})};




function drawAvgViolCrime(viol_crime){
      nv.addGraph(function() {
          var chart = nv.models.multiBarChart()
              .barColor(d3.scale.category20().range())
              .duration(300)
              .margin({bottom: 50, left: 70})
              .groupSpacing(0.1)
              ;
          chart.reduceXTicks(false);
          chart.xAxis
              .axisLabel("Crime Categories")
              .axisLabelDistance(35)
              .showMaxMin(false)
              .tickFormat(function (d){
                  console.log(viol_crime[0].values[d].label)
                  return viol_crime[0].values[d].label;
              })
          ;
          chart.yAxis
              .axisLabel("# of Crimes")
              .axisLabelDistance(-5)
              .tickFormat(d3.format(',f'))
          ;
          chart.dispatch.on('renderEnd', function(){
              nv.log('Render Complete');
          });
          d3.select('#top-left svg')
              .datum(viol_crime)
              .call(chart);
          nv.utils.windowResize(chart.update);
          chart.dispatch.on('stateChange', function(e) {
              nv.log('New State:', JSON.stringify(e));
          });
          chart.state.dispatch.on('change', function(state){
              nv.log('state', JSON.stringify(state));
  });
})};


function drawAvgViolCrimePerCap(viol_crime_per_cap){
      nv.addGraph(function() {
          var chart = nv.models.multiBarChart()
              .barColor(d3.scale.category20().range())
              .duration(300)
              .margin({bottom: 50, left: 70})
              .groupSpacing(0.1)
              ;
          chart.reduceXTicks(false);
          chart.xAxis
              .axisLabel("Crime Categories")
              .axisLabelDistance(35)
              .showMaxMin(false)
              .tickFormat(function (d){
                  console.log(viol_crime_per_cap[0].values[d].label)
                  return viol_crime_per_cap[0].values[d].label;
              })
          ;
          chart.yAxis
              .axisLabel("# of Crimes Per Capita")
              .axisLabelDistance(-5)
              .tickFormat(d3.format(',.01e'))
          ;
          chart.dispatch.on('renderEnd', function(){
              nv.log('Render Complete');
          });
          d3.select('#top-right svg')
              .datum(viol_crime_per_cap)
              .call(chart);
          nv.utils.windowResize(chart.update);
          chart.dispatch.on('stateChange', function(e) {
              nv.log('New State:', JSON.stringify(e));
          });
          chart.state.dispatch.on('change', function(state){
              nv.log('state', JSON.stringify(state));
  });
})};



function drawFatalEncounters(average_fatal_encounters){
      nv.addGraph(function() {
        chart = nv.models.multiBarChart()
            .barColor(d3.scale.category20().range())
            .duration(300)
            .margin({bottom: 50, left: 70})
            .groupSpacing(0.1)
        ;
        chart.reduceXTicks(false).staggerLabels(true);
        chart.xAxis
            .axisLabel("Crime Categories")
            .axisLabelDistance(35)
            .showMaxMin(false)
            .tickFormat(function (d){
                console.log(average_fatal_encounters[0].values[d].label)
                return average_fatal_encounters[0].values[d].label;
            })
        ;
        chart.yAxis
            .axisLabel("# of Fatal Encounters")
            .axisLabelDistance(-5)
            .tickFormat(d3.format(',.01e'))
        ;
        chart.dispatch.on('renderEnd', function(){
            nv.log('Render Complete');
        });
        d3.select('#top-left svg')
            .datum(average_fatal_encounters)
            .call(chart);
        nv.utils.windowResize(chart.update);
        chart.dispatch.on('stateChange', function(e) {
            nv.log('New State:', JSON.stringify(e));
        });
        chart.state.dispatch.on('change', function(state){
            nv.log('state', JSON.stringify(state));
    });
  })};



function drawFatalEncountersPerCapita(average_fatal_encounters_per_cap){
      nv.addGraph(function() {
        chart = nv.models.multiBarChart()
            .barColor(d3.scale.category20().range())
            .duration(300)
            .margin({bottom: 50, left: 70})
            .groupSpacing(0.1)
        ;
        chart.reduceXTicks(false).staggerLabels(true);
        chart.xAxis
            .axisLabelDistance(35)
            .showMaxMin(false)
            .tickFormat(function (d){
                console.log(average_fatal_encounters_per_cap[0].values[d].label)
                return average_fatal_encounters_per_cap[0].values[d].label;
            })
        ;
        chart.yAxis
            .axisLabel("# of Fatal Encounters")
            .axisLabelDistance(-5)
            .tickFormat(d3.format(',.01e'))
        ;
        chart.dispatch.on('renderEnd', function(){
            nv.log('Render Complete');
        });
        d3.select('#top-right svg')
            .datum(average_fatal_encounters_per_cap)
            .call(chart);
        nv.utils.windowResize(chart.update);
        chart.dispatch.on('stateChange', function(e) {
            nv.log('New State:', JSON.stringify(e));
        });
        chart.state.dispatch.on('change', function(state){
            nv.log('state', JSON.stringify(state));
          });
  })};

function drawMilitaryValue(military_value){
      nv.addGraph(function() {
        chart = nv.models.multiBarChart()
            .barColor(d3.scale.category20().range())
            .duration(300)
            .margin({bottom: 50, left: 70})
            .groupSpacing(0.1)
        ;
        chart.reduceXTicks(false).staggerLabels(true);
        chart.xAxis
            .showMaxMin(false)
            .tickFormat(function (d){
                console.log(military_value[0].values[d].label)
                return military_value[0].values[d].label;
            })
        ;
        chart.yAxis
            .axisLabel("Dollars")
            .axisLabelDistance(-5)
            .tickFormat(d3.format(',f'))
        ;
        chart.dispatch.on('renderEnd', function(){
            nv.log('Render Complete');
        });
        d3.select('#top-left svg')
            .datum(military_value)
            .call(chart);
        nv.utils.windowResize(chart.update);
        chart.dispatch.on('stateChange', function(e) {
            nv.log('New State:', JSON.stringify(e));
    });
    chart.state.dispatch.on('change', function(state){
        nv.log('state', JSON.stringify(state));
    });
  })};



function drawMilitaryValuePerCap(military_value_per_cap){
      nv.addGraph(function() {
        chart = nv.models.multiBarChart()
            .barColor(d3.scale.category20().range())
            .duration(300)
            .margin({bottom: 50, left: 70})
            .groupSpacing(0.1)
        ;
        chart.reduceXTicks(false).staggerLabels(true);
        chart.xAxis
            .showMaxMin(false)
            .tickFormat(function (d){
                console.log(military_value_per_cap[0].values[d].label)
                return military_value_per_cap[0].values[d].label;
            })
        ;
        chart.yAxis
            .axisLabel("Dollars Per Capita")
            .axisLabelDistance(-5)
            .tickFormat(d3.format(',.01f'))
        ;
        chart.dispatch.on('renderEnd', function(){
            nv.log('Render Complete');
        });
        d3.select('#top-right svg')
            .datum(military_value_per_cap)
            .call(chart);
        nv.utils.windowResize(chart.update);
        chart.dispatch.on('stateChange', function(e) {
            nv.log('New State:', JSON.stringify(e));
        });
        chart.state.dispatch.on('change', function(state){
            nv.log('state', JSON.stringify(state));
        });
      })};
