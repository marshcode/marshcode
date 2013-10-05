/*global THREE */ 
/*global assert */
/*global $ */
/*global jQuery */

var BEZIER = BEZIER || {};
BEZIER.widgets = BEZIER.widgets  || {};


///////////////////////
//3D Visualizer Class
//main interface to THREE.js
///////////////////////

BEZIER.widgets.visualizer_3d = function (curve_storage, width, height, stage_factory) {
	//FIXME: constructor is getting a little long.  Consider adding some setters and making some sensible defaults
	//it is also getting tougher to understand the constructor since a lot of the arguments are simple integers
	
	if (!curve_storage) {
		throw BEZIER.errors.illegal_argument_error("curve_storage cannot be null");
	}
	
	var num_points = 100;
	stage_factory = stage_factory || BEZIER.widgets.stage_basic;
	var curve_factory = BEZIER.widgets.render_solid_tube;
	
	
	var curves = {};
	var default_options = {points_visible:  true,
						   polygon_visible: true,
						   curve_visible:   true,
						   size:          0.25};
	
	
	
	var stage = stage_factory(width || 500, height || 500);	
	var scene = stage.make_scene();
	
	
	var render_trigger = false;
	function render() {
		stage.renderer.render(scene, stage.camera);
		render_trigger = true;
	}
		
	
	function set_visibility_helper(curve_name, is_visible, option_name, mesh_name) {
		var curve_info = curves[curve_name];
		if (!curve_info) {
			return;
		}
		var options = curve_info.options;			
		var mesh = curve_info.meshes[mesh_name];
		
		if (is_visible !== null) {
			options[option_name] = Boolean(is_visible);
			mesh.traverse(function (o) {
				o.visible = is_visible;
			});				
		}
	}
	
	

	
	var that = {
		///////Options///////////	
		get_options: function (curve_name) {
			
			if(curve_name === "default"){
				return jQuery.extend({}, default_options);
			}
			
			var curve_info = curves[curve_name];
			if (!curve_info) {
				return;
			}
			
			return jQuery.extend({}, curve_info.options);
		},
			
		/////////POINTS//////////
		get_num_points: function () {
			return num_points;
		},

		set_num_points: function (num) {
			num_points = num;
		},
	
		////////RENDERING////////////
		
		set_curve_factory: function (_curve_factory) {
			curve_factory  = _curve_factory || curve_factory;
		},
				
		update: function () {
			render_trigger = false;
			stage.camera_controls.update();
			
			if (!render_trigger) {
				render();
			}
		},
		
		////////RENDERING OPTIONS////////////
		get_view: function () {
			var target = stage.camera_controls.target;
			var position = stage.camera_controls.object.position;
			//copying the positions protects them from outside modification
			return {"target": BEZIER.core.dim3(target.x, target.y, target.z),
				    "position": BEZIER.core.dim3(position.x, position.y, position.z)};
		},
		
		set_view: function (target, position) {
			
			if (!target) {
				throw BEZIER.errors.illegal_argument_error("Target cannot be null.");
			}
			
			//copying the positions protects them from outside modification
			stage.camera_controls.target = new THREE.Vector3(target.x, target.y, target.z);
			if (position) {
				stage.camera_controls.object.position = new THREE.Vector3(position.x, position.y, position.z);
			}
			
			this.update();
		},
		
		set_curve_size: function (curve_name, radius){
			var curve_info = curves[curve_name];
			if (!curve_info) {
				return;
			}
			var options = curve_info.options;
			options.size = Math.max(radius, 0);
		},
		
		set_points_visibility: function (curve_name, is_visible) {
			set_visibility_helper(curve_name, is_visible, "points_visible", "control_points");
		},

		set_polygon_visibility: function (curve_name, is_visible) {
			set_visibility_helper(curve_name, is_visible, "polygon_visible", "control_polygon");
		},
		set_curve_visibility: function (curve_name, is_visible) {
			set_visibility_helper(curve_name, is_visible, "curve_visible", "curve");
		},		
		
		//////////DOM Manipulaion/////////////////////
		get_dom_element: function () {
			return stage.renderer.domElement;
		}
		
	};
	
	
	
	function process_removed_curve(curve_name) {
			
			var curve = curves[curve_name];
			if (curve) {
				var meshes = curve.meshes;
				scene.remove(meshes.control_points);
				scene.remove(meshes.control_polygon);
				scene.remove(meshes.curve);	
			}
	
			delete curves[curve_name];
			
		}
	
	function process_edited_curve(curve_name) {
			
			var previous_curve = curves[curve_name];
			var options = null;
			if (previous_curve) {
				options = previous_curve.options;
			} else {
				options = jQuery.extend({}, default_options);
			}
		
			var curve = curve_storage.get_curve(curve_name);
			var meshes = curve_factory(curve, options.size, that.get_num_points());
			
			process_removed_curve(curve_name);
			
			curves[curve_name] = {meshes: meshes, options: options};
			scene.add(meshes.control_points);
			scene.add(meshes.control_polygon);
			scene.add(meshes.curve);
			
			that.set_points_visibility(curve_name, options.points_visible);
			that.set_polygon_visibility(curve_name, options.polygon_visible);
			that.set_curve_visibility(curve_name, options.curve_visible);
			
			that.update();
		}
	
	
	
	curve_storage.on(curve_storage.EVENT_UPDATED, process_edited_curve);
	curve_storage.on(curve_storage.EVENT_ADDED, process_edited_curve);
	
	curve_storage.on(curve_storage.EVENT_CLEARED, process_removed_curve);
	
	stage.camera_controls.addEventListener('change', render);
	return that;

};

////////////////////
//Rendering Strategies
////////////////////

BEZIER.widgets.render_solid_tube = function (curve, radius, num_points) {
	assert(radius > 0, "radius must be greater than 0.");
	assert(num_points > 0, "num_points must be greater than 0.");
	
	var control_point_material =  new THREE.MeshLambertMaterial({ color: 0x0000ff, emissive: 0x000000, ambient: 0x000000, shading: THREE.SmoothShading });
	var control_polygon_material =  new THREE.MeshLambertMaterial({color: 0x00ff00, emissive: 0x000000, ambient: 0x000000, shading: THREE.SmoothShading});
	var curve_material =  new THREE.MeshLambertMaterial({ color: 0xff0000, emissive: 0x000000, ambient: 0x000000, shading: THREE.SmoothShading });

	
	//control points
	var control_points = new THREE.Object3D();
	var control_point_geom = new THREE.SphereGeometry(radius * 1.5, 16, 16);
	var cp, cp_mesh;
	for (var i = 0; i < curve.num_points(); i++) {
		cp = curve.get_point(i);
		cp_mesh = new THREE.Mesh(control_point_geom, control_point_material);
		cp_mesh.position.x = cp.x;
		cp_mesh.position.y = cp.y;
		cp_mesh.position.z = cp.z;
		control_points.add(cp_mesh);
	}
	
	
	//control polygon
	var curve_path = new THREE.CurvePath();
	var pt1, pt2, line, lineGeometry, lineMesh;
	for (i = 0; i < curve.num_points() - 1; i++) {
		pt1 = curve.get_point(i);
		pt2 = curve.get_point(i + 1);
	
		line = new THREE.LineCurve3(new THREE.Vector3(pt1.x, pt1.y, pt1.z), new THREE.Vector3(pt2.x, pt2.y, pt2.z));
		curve_path.add(line);
	}
	var control_polygon = new THREE.Mesh(new THREE.TubeGeometry(curve_path, 64, radius, 8, false), 
										control_polygon_material);
	
	
	
	//curve
	var points = [];
	var pt;
	var tdelta = 1 / num_points;
	for (var t = 0; t <= 1; t += tdelta) {
		pt = curve.calculate(t);
		points.push(new THREE.Vector3(pt.x, pt.y, pt.z));
	}
	var spline = new THREE.SplineCurve3(points);
	var spline_geometry = new THREE.TubeGeometry(spline, 64, radius, 8, false);
	var curve_mesh = new THREE.Mesh(spline_geometry, curve_material);
	
	var meshes = {};
	meshes.control_points  = control_points;
	meshes.control_polygon = control_polygon;
	meshes.curve           = curve_mesh;
	return meshes;
};

/////////////////////////
//STAGE STRATEGIES
/////////////////////////

BEZIER.widgets.stage_basic = function (width, height) {	
	var clear_color = 0xcccccc;
	
	//RENDERER
	var renderer = new THREE.WebGLRenderer({antialias: false});
	renderer.setClearColor(new THREE.Color(clear_color), 1);
	renderer.setSize(width, height);
	
	//CAMERA AND CONTROLS
	var camera = new THREE.PerspectiveCamera(60, width / height, 1, 1000);
	var camera_controls = new THREE.TrackballControls(camera, renderer.domElement);

	camera.position.z = 1;
	
	camera_controls.rotateSpeed = 3.0;
	camera_controls.zoomSpeed = 1.2;
	camera_controls.panSpeed = 0.8;
	
	camera_controls.noZoom = false;
	camera_controls.noPan = false;
	

	//SCENE
	function make_scene() {
		var scene = new THREE.Scene();
		scene.fog = new THREE.FogExp2(clear_color, 0.002);
		
		var light = new THREE.DirectionalLight(0xffffff);
		light.position.set(1, 1, 1);
		scene.add(light);

		light = new THREE.DirectionalLight(0xffffff);
		light.position.set(-1, -1, -1);
		scene.add(light);

		light = new THREE.AmbientLight(0xffffff);
		scene.add(light);
		
		return scene;
		
	}
	
	return {
		camera:          camera,
		camera_controls: camera_controls,
		make_scene:      make_scene,
		renderer:        renderer

	};

};

