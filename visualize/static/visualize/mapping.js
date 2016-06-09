function tooltipHtml(n, d){	/* function to create html content string in tooltip div. */
	if (!d) return ''
	return "<h4>"+n+"</h4><table>"+
		"<tr><td>Military Equipment $</td><td>"+(d.dollars)+"</td></tr>"+
		"<tr><td>Fatal Police Encounters</td><td>"+(d.deaths)+"</td></tr>"+
		"<tr><td>Violent Crimes</td><td>"+(d.violent)+"</td></tr>"+
		"<tr><td>Property Crimes</td><td>"+(d.property)+"</td></tr>"+
		"</table>";
}

$.getJSON("/api/state/", function(data) {
	var sampleData = {};

	data.results.forEach(function(state) {
		var dollars = state.total_military_dollars
		var population = state.total_population_twentyfifteen

		sampleData[state.state] = {
			dollars: dollars,
			deaths: state.total_deaths_twentyfifteen,
			violent: state.total_violent_crime,
			property: state.total_property_crime,
			color: d3.interpolate("#7fbeaf", "#1d4138")(dollars / population / 10)
		};
	});

	/* draw states on id #statesvg */
	uStates.draw("#statesvg", sampleData, tooltipHtml);
});
