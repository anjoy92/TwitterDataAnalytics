var sparkline = {


GenerateSparkLines:function(data)
{
	//loop through the data and load sparkline for each word
	for(key in data)
	{	
		$("#vizpanel").append(this.CreateTextElement(key)).append(this.CreateSpanElement(key));	
		$("span[data='"+key+"']").sparkline(data[key]);
	}		
},

CreateTextElement:function(key)
{
	return $("</br><text class='spark-label'>"+key+"</text>");
},

CreateSpanElement:function(word)
{
	return $("<span class='sparkline' data="+key+"></span>");
}
};
window.onload = function(){

		$.ajax('/getData',
		{
			data: {filename:'ows.json',words:"#ows,#nypd,zuccotti,protest"},
			dataType: 'json',
			success: function (data, statusText, jqXHR)
			{
				sparkline.GenerateSparkLines(data);
			}
		});
};