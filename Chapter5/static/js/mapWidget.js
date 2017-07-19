$.widget('ui.tsmap', {
  options: {
    //this can be modified to change the style of the map
    "cloudmade_tile_base": "http://{s}.tile.osm.org/{z}/{x}/{y}.png",
    //the colors of the heatmap
    "colors": ['#FFFFB2', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#B10026']
  },

  //this variable will hold instance data about the object.
  _odata: {},

  _create: function(){
    var that = this,
      map = L.map($(this.element).attr('id')).setView([25.0, 0], 2),
      APIstr = this.options.cloudmade_tile_base;

    // map.fitWorld();
    L.tileLayer(APIstr).addTo(map);
    this._odata.map = map;

    // get the data and draw the map
    $.ajax({
      "url": "/getData",
      "dataType": "json",
      "success": function(data, jqXHR){
        that._odata.geoData = data;
        that.updateMap(that);
      },
      "error": function(data, jqXHR){
      }
    });

    //reset the map on zoom or pan
    map.on({
      'zoomend': function(){that.updateMap(that);},
      'drag': function(){that.updateMap(that);}
    });

  },

  _getTileTopLeftCell: function(map, elem){
    var top, left, width, height, offset = elem.style.transform;

    if(offset){
      offset = offset.substring(offset.indexOf("(") + 1, offset.indexOf(")"));
      var parts = offset.replace("px","").split(", ");

      left = parseInt(parts[0], 10);
      top = parseInt(parts[1], 10);
    }
    else{
      top = elem.style.top;
      top = Number(top.substring(0, top.length - 2));
      left = elem.style.left;
      left = Number(left.substring(0, left.length - 2));
    }

    
    // top = elem.offsetHeight;
    // left = elem.offsetWidth;
    width = elem.width;
    height = elem.height;

    return {
      'top': top,
      'left': left,
      'width': width,
      'height': height
    };
  },

  updateMap: function(widgetContext){
    var data = widgetContext._odata.geoData;
    if(data){
      var screenHeight = widgetContext.element.height(),
          screenWidth = widgetContext.element.width(),
          coordData = [],
          estimateObj,
          estimate,
          top_k = new Array(widgetContext.options.top_k),
          max = 0.0,
          colors = widgetContext.options.colors;
      //translate each lat/lng to a layer point
      for(var i = 0; i < data.length; i++){
        try{
          var lat = parseFloat(data[i]['lat']),
            lng = parseFloat(data[i]['lng']),
            point = new L.LatLng(lat, lng),
            tmp = widgetContext._odata.map.latLngToLayerPoint(point);
          coordData.push([tmp.x, tmp.y]);
        }
        catch(e){}
      }

      //get the KDE 
      estimateObj = kernel_density_object.kernelDensityEstimate(screenWidth, screenHeight, coordData);
      estimate = estimateObj['estimate'];

      //get the maximum
      for(var row = 0; row < estimate.length; row++){
        for(var col = 0; col < estimate[row].length; col++){
          max = Math.max(max, estimate[row][col]);
        }
      }

      // remove the old heatmap layer
      if(widgetContext._odata.heatmaplayer){
        widgetContext._odata.map.removeLayer(widgetContext._odata.heatmaplayer);
      }

      widgetContext._odata.heatmaplayer = L.tileLayer.canvas();
      widgetContext._odata.heatmaplayer.drawTile = function(canvas, tilepoint, zoom){
        var ctx = canvas.getContext('2d'),
          topLeft = widgetContext._getTileTopLeftCell(widgetContext._odata.map, canvas);

        for(var row = topLeft.top; row < topLeft.top + topLeft.height; row++){
          for(var col = topLeft.left; col < topLeft.left + topLeft.width; col++){
            if(row >= 0 && col >= 0 && row < estimate.length && col < estimate[0].length){
              if(estimate[row][col] > 0){
                ctx.fillStyle = colors[Math.floor(estimate[row][col] / max * colors.length)];
                ctx.fillRect(col - topLeft.left, row - topLeft.top, 1, 1);
              }
            }
          }
        }
      }

      widgetContext._odata.map.addLayer(widgetContext._odata.heatmaplayer);

      //remove all other maps
      $(".map-legend", widgetContext.element).remove();
      //now draw the legend
      var $legend = $(document.createElement('div')).addClass('map-legend');
      for(var i = colors.length - 1; i >= 0; i--){
          var $toAppend = $(document.createElement('div'))
            .addClass('map-legend-item')
            .css('background-color', colors[i])
            .css('height', 100/colors.length + '%')
            .append(
              1 + Math.round(10 * estimateObj['maxVal'] * i/(colors.length-1)) / 10
            );
          if(i === colors.length - 1){
            $toAppend.css('border-top-left-radius', '15px');
            $toAppend.css('border-top-right-radius', '15px');
          }
          else if(i === 0){
            $toAppend.css('border-bottom-left-radius', '15px');
            $toAppend.css('border-bottom-right-radius', '15px');
          }
          $legend.append($toAppend);
      }
      widgetContext.element.append($legend);
    }
  }
});