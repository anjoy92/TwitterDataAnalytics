var tag_cloud = {

	script_location: 'jsp/WordCloud.jsp',
	layout:null,
	
	DrawCloud:function(words)
	{
		var fill = d3.scale.category10();
		d3.select("#cloudpane").append("svg")
		.append("g")
        .attr("transform", "translate(400,400)")
		.selectAll("text")
        .data(words)
		.enter().append("text")
        .style("font-size", function(d) { return d.size + "px"; })
        .style("font-family", "Impact")
        //.style("fill", function(d, i) { return fill(i); })
        .attr("text-anchor", "middle")
        .attr("transform", function(d) {
          return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function(d) { return d.text; });
	}
  
};  
window.onload = function()
{
	var data=[{"text": "#ows", "size": 35652}, {"text": "the", "size": 25924}, {"text": "and", "size": 9125}, {"text": "#occupywallstreet", "size": 6116}, {"text": "are", "size": 5627}, {"text": "from", "size": 5306}, {"text": "you", "size": 5129}, {"text": "park", "size": 5064}, {"text": "for", "size": 4946}, {"text": "police", "size": 4299}, {"text": "#occupy", "size": 4038}, {"text": "nypd", "size": 3930}, {"text": "this", "size": 3672}, {"text": "that", "size": 3575}, {"text": "they", "size": 3366}, {"text": "protesters", "size": 3333}, {"text": "with", "size": 3329}, {"text": "have", "size": 3324}, {"text": "zuccotti", "size": 3301}, {"text": "not", "size": 3121}, {"text": "all", "size": 3017}, {"text": "now", "size": 2909}, {"text": "just", "size": 2851}, {"text": "#tcot", "size": 2588}, {"text": "occupy", "size": 2403}, {"text": "out", "size": 2376}, {"text": "what", "size": 2346}, {"text": "has", "size": 2325}, {"text": "press", "size": 2213}, {"text": "nyc", "size": 2141}, {"text": "will", "size": 2103}, {"text": "people", "size": 2067}, {"text": "#nypd", "size": 2037}, {"text": "wall", "size": 1964}, {"text": "new", "size": 1939}, {"text": "about", "size": 1937}, {"text": "but", "size": 1878}, {"text": "was", "size": 1813}, {"text": "being", "size": 1757}, {"text": "live", "size": 1727}, {"text": "eviction", "size": 1676}, {"text": "street", "size": 1648}, {"text": "its", "size": 1625}, {"text": "right", "size": 1612}, {"text": "#p2", "size": 1603}, {"text": "can", "size": 1585}, {"text": "their", "size": 1512}, {"text": "mayor", "size": 1466}, {"text": "your", "size": 1451}, {"text": "city", "size": 1419}, {"text": "like", "size": 1418}, {"text": "our", "size": 1388}, {"text": "court", "size": 1370}, {"text": "back", "size": 1353}, {"text": "were", "size": 1338}, {"text": "order", "size": 1323}, {"text": "raid", "size": 1308}, {"text": "why", "size": 1290}, {"text": "dont", "size": 1276}, {"text": "judge", "size": 1275}];
	console.log("Shobhit");
	console.log(data);
	tag_cloud.layout = d3.layout.cloud().size([350, 400])
				  .words(data)
				  .rotate(function() { return ~~(Math.random() * 2) * 1; })
				  .font("Times New Roman")
				  .fontSize(function(d) { return d.size; })
				  .padding(200)
				  .on("end", tag_cloud.DrawCloud)
				  .start();

	// $.ajax(tag_cloud.script_location,
 //            {
 //                data: {filename:'ows.json',k:60},
 //                dataType: 'json',
 //                success: function (data, statusText, jqXHR) {
				
				  
 //                }
 //            });
}
  