function tooltipHtml(n, d){	/* function to create html content string in tooltip div. */
	if (!d) return ''
	return "<h4>"+n+"</h4><table>"+
		"<tr><td>Military Equipment</td><td>"+(d.dollars)+"</td></tr>"+
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
		var violent = state.total_violent_crime
		var deaths = state.total_deaths_twentyfifteen

		sampleData[state.state] = {
			dollars: '$' + dollars.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","),
			deaths: deaths,
			violent: violent.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","),
			property: state.total_property_crime.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","),
			color: d3.interpolate("#b0b5b9", "#930006")((dollars / population) / 10)
		};
	});

	/* draw states on id #statesvg */
	uStates.draw("#statesvg", sampleData, tooltipHtml);
});
