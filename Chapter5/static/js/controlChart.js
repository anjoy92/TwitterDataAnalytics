var trendcomp = {
	margin: {top: 20, right: 80, bottom: 30, left: 50},
    width:null,
    height:null,
	parseDate: d3.time.format("%d %b %Y %H:%M").parse,
	x:null,
	y:null,
	color: d3.scale.category10(),
	xAxis:null,
	yAxis:null,
	line:null,
	svg:null,

Initialize: function(){
	this.width = 1360 - this.margin.left - this.margin.right,
    this.height = 540 - this.margin.top - this.margin.bottom;
	this.x = d3.time.scale()
    .range([0, this.width]);
	this.y = d3.scale.linear()
    .range([this.height, 0]);
	this.xAxis = d3.svg.axis()
		.scale(this.x)
		.orient("bottom");
	this.yAxis = d3.svg.axis()
		.scale(this.y)
		.orient("left");
	this.line = d3.svg.line()
		.interpolate("basis")
		.x(function(d) { return this.x(d.date); })
		.y(function(d) { return this.y(d.count); });
	this.svg = d3.select("#vizpanel").append("svg")
		.attr("width", this.width + this.margin.left + this.margin.right)
		.attr("height", this.height + this.margin.top + this.margin.bottom)
		.append("g")
		.attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");	
},

GenerateGraph:function(data)
{
	  this.color.domain(d3.keys(data[0]).filter(function(key) { return key !== "date"; }));
	  data.forEach(function(d) {
		d.date = trendcomp.parseDate(d.date);
	  });

	  var words = this.color.domain().map(function(word) {
		return {
		  word: word,
		  values: data.map(function(d) {
			return {date: d.date, count: +d[word]};
		  })
		};
	  });

	  this.x.domain(d3.extent(data, function(d) { return d.date; }));

	  this.y.domain([
		d3.min(words, function(c) { return d3.min(c.values, function(v) { return v.count; }); }),
		d3.max(words, function(c) { return d3.max(c.values, function(v) { return v.count; }); })
	  ]);

	  this.svg.append("g")
		  .attr("class", "x axis")
		  .attr("transform", "translate(0," + this.height + ")")
		  .call(this.xAxis);

	  this.svg.append("g")
		  .attr("class", "y axis")
		  .call(this.yAxis)
		  .append("text")
		  .attr("class", "ylabel")
		  .attr("text-anchor", "end")
		  .attr("y", -40)
		  .attr("dy", ".75em")
		  .attr("transform", "rotate(-90)")
		  .text("Number of Tweets");		  

	  var word = this.svg.selectAll(".word")
		  .data(words)
		  .enter().append("g")
		  .attr("class", "word");

	  word.append("path")
		  .attr("class", "line")
		  .attr("d", function(d) { return trendcomp.line(d.values); })
		  .style("stroke", function(d) { return trendcomp.color(d.word); });

	  word.append("text")
		  .datum(function(d) { return {word: d.word, value: d.values[d.values.length - 1]}; })
		  .attr("transform", function(d) { return "translate(" + trendcomp.x(d.value.date) + "," + trendcomp.y(d.value.count) + ")"; })
		  .attr("x", 3)
		  .attr("dy", ".35em")		  
		  .text(function(d) { return d.word; });	//comment this to remove the legend beside the trendline
		  
	  var legend = this.svg.selectAll(".legend")
		  .data(this.color.domain().slice().reverse())
		  .enter().append("g")
		  .attr("class", "legend")
		  .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

	  legend.append("rect")
		  .attr("x", this.width - 18)
		  .attr("width", 18)
		  .attr("height", 18)
		  .style("fill", this.color);

	  legend.append("text")
		  .attr("x", this.width - 24)
		  .attr("y", 9)
		  .attr("dy", ".35em")
		  .style("text-anchor", "end")
		  .text(function(d) { return d; });
			

}
};
window.onload = function() {
	trendcomp.Initialize();
	$.ajax('/getData',
	{
		dataType: 'json',
		success: function (data, statusText, jqXHR)
		{
			trendcomp.GenerateGraph(data);
		}
	});

};