/*global console, window */

var BEZIER = BEZIER || {};
BEZIER.errors = BEZIER.errors || {};
BEZIER.core = BEZIER.core || {};

/////////////////////////
//EXCEPTIONS
/////////////////////////
BEZIER.errors.error = function (name, message) {
	var e = new Error(message);
	e.name = name;
	return e;
};
BEZIER.errors.illegal_argument_error = function (message) {
	return BEZIER.errors.error("IllegalArgumentError", message);
};

//leaving this in the global namespace for convenience purposes.
function assert(condition, message) {
	
	if (condition) {
		return;
	}
	
    if (window.console) {
        var console_message = "Assertion Violation: " + (message || "");
        console.group(console_message);
        console.trace();
        console.groupEnd(console_message);
    }
    
    throw BEZIER.errors.error("AssertionError", message);
	
}


//////////////////////////
//Dim3
//////////////////////////
//Basic Collection of x,y,z coordinates.  Useful as points, vectors, deltas, whatever.  Future iterations may 
//require actual classes for these but there is no reason to get caught up in that now.
BEZIER.core.dim3 = function (x, y, z) {
	return {
		x: x || 0,
		y: y || 0,
		z: z || 0
	};
};

/////////////////////////////////////////
//Bezier Calculations
/////////////////////////////////////////
//Calculates binomial coefficients for a single n.

BEZIER.core.binomial_coefficients = function (n) {
	assert(n >= 0, "n (" + n + ") cannot be negative.");
	
	
	var C = [1];
	for (var k = 0; k < n; ++ k) {
		C[k + 1] = (C[k] * (n - k)) / (k + 1);
	}
	    
	return C;
};

//calculates a single bezier curve at point t.
BEZIER.core.bezier_calculation = function (points, t) {

	assert(t >= 0 && t <= 1, "T (" + t + ") argument is out of range: 0 <= t <= 1");
	assert(points.length > 0, "No control point given.");
	
	var n = points.length - 1;
	var v = 0;
	var C = BEZIER.core.binomial_coefficients(n); //very inefficient but whatever.  Caching can be handled later.
	for (var i = 0; i < points.length; i++) {
		v += Math.pow(1 - t, n - i) * Math.pow(t, i) * points[i] * C[i];
	}
	return v;
};

///////////////////////////////////////////
//Bezier Curve Classes
///////////////////////////////////////////

BEZIER.core.bezier_curve_3 = function (control_points) {

	if (control_points) {
		control_points = control_points.slice();
	} else {
		control_points = [];
	}
	
	return {
		get_point: function (idx) {
			return control_points[idx];
		},
				
		append_point: function(new_point){
			control_points.push(new_point);
			return control_points.length - 1;
		},
		
		insert_point: function(idx, new_point){
			if(idx < 0 || idx >= control_points.length){
				throw BEZIER.errors.illegal_argument_error("Index " + idx + " is out of range.");
			}
			
			control_points.splice(idx, 0, new_point);
		},
		
		remove_point: function(idx){
			if(idx < 0 || idx >= control_points.length){
				throw BEZIER.errors.illegal_argument_error("Index " + idx + " is out of range.");
			}
			control_points.splice(idx, 1);
		},
		
		num_points: function () {
			return control_points.length;
		},
		
		calculate: function (t) {
			var x = [], 
				y = [], 
				z = [];
			var pt = null;
						
			if( t < 0 || t > 1 ){
				throw BEZIER.errors.illegal_argument_error("T (" + t + ") argument is out of range: 0 < t < 1");
			}
			
			if(this.num_points() == 0){
				return null;
			}
			
			for (var i = 0; i < this.num_points(); i++) {
				pt = this.get_point(i);
				x.push(pt.x); 
				y.push(pt.y); 
				z.push(pt.z);
			}
			
			return BEZIER.core.dim3(
				BEZIER.core.bezier_calculation(x, t),
				BEZIER.core.bezier_calculation(y, t),
				BEZIER.core.bezier_calculation(z, t)
			);
		}
	};

};
