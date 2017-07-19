var trendline = {
	script_location: 'jsp/TrendLine.jsp',
	margin: {top: 10, right: 10, bottom: 100, left: 40},
    margin2: {top: 430, right: 10, bottom: 20, left: 40},
    width: null,
    height: null,
    height2: null,
	
	parseDate: d3.time.format("%d %b %Y %H:%M").parse,
	
	x: null,
    x2: null,
    y: null,
    y2: null,
	
	xAxis: null,
    xAxis2: null,
    yAxis: null,
	
	brush: null,
	
	area: null,
	
	area2: null,
	
	svg: null,
	
	focus: null,
	context: null,

	
	initialize:function(){
		this.width = 1260 - this.margin.left - this.margin.right;
		this.height = 500 - this.margin.top - this.margin.bottom;
		this.height2 = 500 - this.margin2.top - this.margin2.bottom;
		this.x = d3.time.scale().range([0, this.width]);
		this.x2 = d3.time.scale().range([0, this.width]);
		this.y = d3.scale.linear().range([this.height, 0]);
		this.y2 = d3.scale.linear().range([this.height2, 0]);
		this.xAxis = d3.svg.axis().scale(this.x).orient("bottom");
		this.xAxis2 = d3.svg.axis().scale(this.x2).orient("bottom");
		this.yAxis = d3.svg.axis().scale(this.y).orient("left");
		this.brush = d3.svg.brush()
			.x(this.x2)
			.on("brush", brushed);
			
		this.area = d3.svg.area()
			.interpolate("monotone")
			.x(function(d) { return trendline.x(d.date); })
			.y0(this.height)
			.y1(function(d) { return trendline.y(d.count); });
			
			
		this.area2 = d3.svg.area()
			.interpolate("monotone")
			.x(function(d) { return trendline.x2(d.date); })
			.y0(this.height2)
			.y1(function(d) { return trendline.y2(d.count); });
			
		this.svg = d3.select("#vizpanel").append("svg")
			.attr("width", this.width + this.margin.left + this.margin.right)
			.attr("height", this.height + this.margin.top + this.margin.bottom);
		this.svg.append("defs").append("clipPath")
			.attr("id", "clip")
			.append("rect")
			.attr("width", this.width)
			.attr("height", this.height);
		this.focus = this.svg.append("g")
			.attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");
		this.context = this.svg.append("g")
			.attr("transform", "translate(" + this.margin2.left + "," + this.margin2.top + ")");	
			
	}
};

function brushed() {
		trendline.x.domain(trendline.brush.empty() ? trendline.x2.domain() : trendline.brush.extent());
		trendline.focus.select("path").attr("d", trendline.area);
		trendline.focus.select(".x.axis").call(trendline.xAxis);
	};

window.onload = function()
{
	// Step 1: Initialize the chart
	trendline.initialize();
	// Step 2: Fetch data using AJAX
	$.ajax('/getData',
	{
		data: {filename:'ows.json'},
		dataType: 'json',
		success: function (data, statusText, jqXHR) {
			  data.forEach(function(d) {
				d.date = trendline.parseDate(d.date);
				d.count = +d.count;
			  });

			  trendline.x.domain(d3.extent(data.map(function(d) { return d.date; })));
			  trendline.y.domain([0, d3.max(data.map(function(d) { return d.count; }))]);
			  trendline.x2.domain(trendline.x.domain());
			  trendline.y2.domain(trendline.y.domain());
			  //Step 3: Initialize the focus handlers
			  trendline.focus.append("path")
				  .datum(data)
				  .attr("clip-path", "url(#clip)")
				  .attr("d", trendline.area);

			  trendline.focus.append("g")
				  .attr("class", "x axis")
				  .attr("transform", "translate(0," + trendline.height + ")")
				  .call(trendline.xAxis);

			  trendline.focus.append("g")
				  .attr("class", "y axis")
				  .call(trendline.yAxis)
				  .append("text")
				  .attr("class", "ylabel")
				  .attr("text-anchor", "end")
				  .attr("y", -40)
				  .attr("dy", ".75em")
				  .attr("transform", "rotate(-90)")
				  .text("Number of Tweets");
				 //Step 4: Context is initialized to series 2
			  trendline.context.append("path")
				  .datum(data)
				  .attr("d", trendline.area2);

			  trendline.context.append("g")
				  .attr("class", "x axis")
				  .attr("transform", "translate(0," + trendline.height2 + ")")
				  .call(trendline.xAxis2);
				// Step 5: Select the brushed region and focus on it
			  trendline.context.append("g")
				  .attr("class", "x brush")
				  .call(trendline.brush)
				.selectAll("rect")
				  .attr("y", -6)
				  .attr("height", trendline.height2 + 7);

		}
	});
};
