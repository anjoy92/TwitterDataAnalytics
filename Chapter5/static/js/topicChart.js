var cat_chart = {

	CreateTopicChart:function(json)
	{
		var r = Raphael("vizpanel");                    
         r.dotchart(10, 10, 1000, 500, json.xcoordinates, json.ycoordinates, json.data, {symbol: "o", max: 20, heat: true, axis: "0 0 1 1", axisxstep: json.axisxstep, axisystep: json.axisystep, axisxlabels: json.axisxlabels, axisxtype: "  ", axisytype: "|", axisylabels: json.axisylabels}).hover(function () {
                    this.marker = this.marker || r.tag(this.x, this.y, this.value, 0, this.r + 2).insertBefore(this);
                    this.marker.show();
                }, function () {
                    this.marker && this.marker.hide();
                });           
	}
};

//call this on load
window.onload = function()
{
        
       //call the initializer for infovis graph panel

        $.ajax('/getData',
            {
                data: {filename:'ows.json'},
                dataType: 'json',
                success: function (data, statusText, jqXHR) {
                    console.log(data);
                cat_chart.CreateTopicChart(data);
                }
            });
			
	
};