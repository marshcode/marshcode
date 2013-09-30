var BEZIER = BEZIER || {};
BEZIER.parsers = BEZIER.parsers  || {};


BEZIER.parsers.single = function (data) {
	
	var points = [];
	
	
	JSON.parse(data).forEach(function (point) {
		points.push(BEZIER.core.dim3(Number(point[0]), Number(point[1]), Number(point[2])));
		
	});
	
	
	return BEZIER.core.bezier_curve_3(points);
	
};