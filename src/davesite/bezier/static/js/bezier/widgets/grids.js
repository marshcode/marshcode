/*global $ */

var BEZIER = BEZIER || {};
BEZIER.widgets = BEZIER.widgets || {};


BEZIER.widgets.control_point_grid = function (storage, curve_name) {
	
	var container = $("<div></div>");
	
	container.handsontable({
		data: [],
		minSpareRows: 0,
		contextMenu: ['row_above', 'row_below', 'remove_row', 'hsep3', 'undo', 'redo'],
		fillHandle: false,
		colHeaders: ['X', 'Y', 'Z'], //, 'Highlight'],
		rowHeaders: true,
	    columns: [
	        {data: 'x', type: "numeric", allowInvalid: false},
	        {data: 'y', type: "numeric", allowInvalid: false},
	        {data: 'z', type: "numeric", allowInvalid: false}
	        //{data: 'highlight', type: 'checkbox', allowInvalid: false, readOnly: false}
	    ],

		afterRemoveRow: function (index) {
                if (!storage.has_curve(curve_name)) {
				    return;
	            }

                var curve = storage.get_curve(curve_name);
                curve.remove_point(index);
                storage.updated(curve_name);
		    },

		beforeChange: function (changes, source) {
            if (!changes) {
                return;
	        }

            $(changes).each(function (idx, change) {
                //typeof(change[3] == 'string' && change[3].length === 0
                //redundant when new value is 0 but it catches all of the empty rows
                if (!change[3] && change[1] !== "highlight") {
                    changes[idx][3] = 0;
                }
            });
			
			
		},

		afterChange: function (changes, source) {

            if (!changes) {
                return;
            }
            if (!storage.has_curve(curve_name)) {
				return;
            }

			var curve = storage.get_curve(curve_name);
            var row, prop, old_val, new_val;
            var point;

            $(changes).each(function (idx, change) {
                row = change[0]; prop = change[1]; old_val = change[2]; new_val = change[3];
                point = curve.get_point(row);

                if (old_val === new_val) {
                    return; //nothing to do here
                }

                if (prop === 'x') {
                    point.x = new_val;
                } else if (prop === 'y') {
                    point.y = new_val;
                } else if (prop === 'z') {
                    point.z = new_val;
                }
                
            });

            storage.updated(curve_name);

		},
		
		afterCreateRow: function (index) {

			if (!storage.has_curve(curve_name)) {
				return;
			}

			var curve = storage.get_curve(curve_name);
			var pt = BEZIER.core.dim3(0, 0, 0);
	
			console.log(index);
			console.log(curve.num_points())
            if (index < curve.num_points() ) {

                curve.insert_point(index, pt);
			} else {
				curve.append_point(pt);
			}
				
			storage.updated(curve_name);

		}
		

		
	});
	
	var that = {
			dom_element: container,
			curve_name: curve_name,
			
			update: function () {				
				if(!storage.has_curve(curve_name)){
					return
				}
				
				var data = [];
				var curve = storage.get_curve(curve_name);
				var pt;
				
				for (var i = 0; i < curve.num_points(); i++) {
					pt = curve.get_point(i);
					data.push({x: pt.x, 
							   y: pt.y, 
							   z: pt.z});
				}
				this.dom_element.handsontable("loadData", data);
				
				
			}
			
		};
	
	
	storage.on(storage.EVENT_UPDATED, function (updated_curve_name) {
		
		if(that.curve_name != updated_curve_name){
			return;
		}
		
		that.update();
		
	});
	
	that.update();
	return that;
};