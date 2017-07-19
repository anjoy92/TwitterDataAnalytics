var kernel_density_object = {
  colors: ['#FFFFB2', '#FED976', '#FEB24C', '#FD8D3C', '#FC4E2A', '#E31A1C', '#B10026'],

  makeZeros: function(rows, cols) {
    var matrix = [], row = [];

    for (var i = 0; i < cols; i++){
      row[i] = 0;
    }
    for (var i = 0; i < rows; i++){
      matrix.push(row.slice());
    }
    return matrix;
  },
  
  kernelDensityEstimate: function(screenWidth, screenHeight, data, bandwidth, kernelFunction, distanceFunction){
    //If no bandwidth is provided, set a default. 
    if(!bandwidth){
      bandwidth = 400;
    }
    var GIVE_UP_AFTER = 15; //after checking a radius of this size and not finding <bandwidth> points, we just give up.

    //If the kernel is not provided by the user, default to the Epanechnikov kernel.
    if(!kernelFunction){
      //Epanechnikov kernel
      kernelFunction = function(x){
        return 3/4 * (1-x*x);
      }
      //Gaussian
      // kernelFunction = function(x){
      //   return Math.pow(Math.E, -1/2 * x * x);
      // }
      // console.log("LINEAR KERNEL");
      // kernelFunction = function(x){
      //   return 1 - x;
      // }
    }

    //If no distance function is provided, default to Euclidean distance.
    if(!distanceFunction){
      // Good old Euclidean distance.
      distanceFunction = function(x1,y1,x2,y2){
        return Math.sqrt( Math.pow(x1 - x2, 2) + Math.pow(y1 - y2, 2) );
      }
    }

    //matrices that hold the points at various stages in the computation. Each will be the size of the screen (in pixels).
    var pointMatrix = kernel_density_object.makeZeros(screenHeight, screenWidth, 0),
        bandwidthMatrix = kernel_density_object.makeZeros(screenHeight, screenWidth, 0),
        kernelDensityMatrix = kernel_density_object.makeZeros(screenHeight, screenWidth, 0),
        maxPoint = 0;

    //PointMatrix holds the raw counts of the number of tweets in each "cell" on the data grid.
    var success = 0;
    for(var i = 0; i < data.length; i++){
      try{
        pointMatrix[data[i][1]][data[i][0]] += 1;
        ++success;
      }
      catch(e){ }
    }

    // Here we visit each nonzero point and calculate how far we have to travel to find <bandwidth> points. 
    // If we do not find <bandwidth> points within a radius of <GIVE_UP_AFTER>, we set the value of the cell to Infinity.
    for(var row = 0; row < screenHeight; row++){
      for(var col = 0; col < screenWidth; col++){
        if(pointMatrix[row][col] === 0){
          continue;
        }

        maxPoint = Math.max(maxPoint, pointMatrix[row][col]);

        var sum = pointMatrix[row][col], //the tally of points at the visited radius for the radius (initial value is the count at radius 0).
            radius = 0;
        //search the radius to find the sum of the points it contains
        while(radius <= GIVE_UP_AFTER && sum < bandwidth){
          radius++;
          //Here we ensure we count only the values at new (unvisited)  cells.
          for(var i = -radius; i <= radius; i++){
            // If we're in the first or last row, take the entire row. 
            // Otherwise, just take the first and last cell in that row (since the ones in the middle have been visited).
            if(i === -radius || i === radius){
              for(var j = -radius; j <= radius; j++){
                try{
                  sum += pointMatrix[row + i][col + j];
                }catch(e){}
              }  
            }
            else{
              try{
                sum += pointMatrix[row + i][col - radius];
              }catch(e){}
              try{
                sum += pointMatrix[row + i][col + radius];
              }catch(e){}
            }
            
          }
        }
        //store the radius in bandwidthMatrix
        bandwidthMatrix[row][col] = radius > GIVE_UP_AFTER ? Infinity : radius;
      }
    }

    //kernel matrix is the result of bandwidthMatrix pushed through the kernel function
    for(var row = 0; row < screenHeight; row++){
      for(var col = 0; col < screenWidth; col++){
        //get the bandwidth value in this cell
        // var bw = Math.max(bandwidthMatrix[row][col], bandwidth),
        var bw = bandwidthMatrix[row][col],
            d = pointMatrix[row][col],
            circleNum = 0;
        if(bw === Infinity || pointMatrix[row][col] === 0){
          //ignore infinity values
          continue;
        }
        //make a circle and push out the values
        for(circleNum = 0; circleNum < bw; circleNum++){
          for(var i = -circleNum; i <= circleNum; i++){
            if(i === -circleNum || i === circleNum){
              for(var j = -circleNum; j <= circleNum; j++){
                var dist = distanceFunction(row, col, row + i, col + j);
                if(dist < bw){
                  try{
                    kernelDensityMatrix[row + i][col + j] += d * kernelFunction(dist/bw);
                  } catch(e){}
                }  
              }
            }
            else{
              var dist = distanceFunction(row, col, row + i, col + circleNum);
              if(dist < bw){
                try{
                  kernelDensityMatrix[row + i][col - circleNum] += d * kernelFunction(dist/bw);
                } catch(e){}
                try{
                  kernelDensityMatrix[row + i][col + circleNum] += d * kernelFunction(dist/bw);
                } catch(e){}
              }
            }
          }
        }
      }
    }

    //kernelDensityMatrix now holds a matrix of intensity values for each point
    return {
      'estimate': kernelDensityMatrix,
      'maxVal': maxPoint
    };
  }
}
