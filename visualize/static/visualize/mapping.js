
function tooltipHtml(n, d){	/* function to create html content string in tooltip div. */
	return "<h4>"+n+"</h4><table>"+
		"<tr><td>Military Equipment $</td><td>"+(d.dollars)+"</td></tr>"+
		"<tr><td>Fatal Police Encounters</td><td>"+(d.deaths)+"</td></tr>"+
		"<tr><td>Violent Crimes</td><td>"+(d.violent)+"</td></tr>"+
		"<tr><td>Property Crimes</td><td>"+(d.property)+"</td></tr>"+
		"</table>";
}

var sampleData = {};	/* Sample random data. */
["HI", "AK", "FL", "SC", "GA", "AL", "NC", "TN", "RI", "CT", "MA",
"ME", "NH", "VT", "NY", "NJ", "PA", "DE", "MD", "WV", "KY", "OH",
"MI", "WY", "MT", "ID", "WA", "DC", "TX", "CA", "AZ", "NV", "UT",
"CO", "NM", "OR", "ND", "SD", "NE", "IA", "MS", "IN", "IL", "MN",
"WI", "MO", "AR", "OK", "KS", "LA", "VA"]
	.forEach(function(d){
		var dollars=Math.round(100*Math.random()),
			deaths=Math.round(100*Math.random()),
			violent=Math.round(100*Math.random()),
			property=;
		sampleData[d]={dollars:, deaths:, violent:, property:,  color:d3.interpolate("#ffffcc", "#800026")(dollars/100)};
	});

/* draw states on id #statesvg */
uStates.draw("#statesvg", sampleData, tooltipHtml);
