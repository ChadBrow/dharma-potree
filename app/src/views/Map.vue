<template>
    <div id="potree_container" style="position: absolute; width: 100%; height: 100%; left: 0px; top: 0px; ">
        <div id="potree_render_area">
            <div id="potree_toolbar">
			</div>
            <div id="cesiumContainer" style="position: absolute; width: 100%; height: 100%; background-color:green;"/>
            <!-- <v-card shaped id="potree_toolbar">
                <v-card-subtitle style="padding: 4px;">Viewer Settings</v-card-subtitle>
                <v-container style="padding-top: 0px;">
                    <v-switch v-model="showIntersectionOnClick" :label="`Show Pointcloud`"/>
                    <v-switch v-model="showPointcloud" :label="`Show Intrsection on Click`"/>
                    <v-btn v-on:click="displayCameraPos()"> Display Camera Position</v-btn>
                </v-container>
            </v-card> -->
        </div>
        <!-- <div class="credits">
			<div class="logo">
				<a href="https://dharma3d.org/" target="_blank">
					<img src="../../public/resources/images/DHARMA_logo_long.png" style="width: 100%;"/>
				</a>
			</div>
			
			<div style="background-color: rgba(255, 255, 255, 0.5); padding: 3px;" class="logo">
				<img src="../../public/resources/logo_small.png">
			</div>
		</div> -->
    </div>
</template>

<script>   
//import libraries
import * as THREE from 'three';
import { PLYLoader } from "../../public/libs/three.js/loaders/PLYLoader.js";

export default{
    data(){
        return {
            showIntersectionOnClick: false,
            data: null
            
        }
    },

    mounted(){
        //Load data about current map
        let data = require("../data/roman_forum.json");
        this.data = data;

        //Declare Potree and mesh loader
        const Potree = window.Potree;
        const loader = new PLYLoader();

        let resourcePath = '../resources';

        //Make Toolbar 
        const elToolbar = $("#potree_toolbar");
        elToolbar.html(`
            <span>
                <div class="potree_toolbar_label">
                    View
                </div>
                <div>
                    <img title="toggle mesh" name="action_mesh" src="${resourcePath}/icons/triangle.svg" class="annotation-action-icon" style="width: 2em; height: auto;"/>
                    <img title="toggle reconstructions" name="action_recon" src="${resourcePath}/icons/navigation_cube.svg" class="annotation-action-icon" style="width: 2em; height: auto;"/>
                    <img title="toggle pointcloud" name="action_point" src="${resourcePath}/icons/rgb.svg" class="annotation-action-icon" style="width: 2em; height: auto;"/>
                </div>
            </span>
            <span class="potree_toolbar_separator" />
            <span>
                <div class="potree_toolbar_label">
                    Measure
                </div>
                <div>
                    <img title="press esc to clear all measurements" name="action_measure_point" src="${resourcePath}/icons/point.svg" class="annotation-action-icon" style="width: 2em; height: auto;"/>
                    <img title="press esc to clear all measurements" name="action_measure_distance" src="${resourcePath}/icons/distance.svg" class="annotation-action-icon" style="width: 2em; height: auto;"/>
                </div>
            </span>
            <span class="potree_toolbar_separator" />
            <span>
                <div class="potree_toolbar_label">
                    Quality
                </div>
                <div>
                    <selectgroup id="quality_options"
                        <fieldset style="border:none; margin: 0px; padding: 0px;">
                            <legend></legend>
                            <span style="display:flex">
                                <span style="flex-grow: 1; display: inherit">	
                                    <label for="quality_options_low" class="ui-button ui-state-default" style="width: 100%; padding: 0.4em 0.1em; margin: 0px; border-radius: 4px 0px 0px 4px; border-top: 1px solid black; border-right: 1px solid black; border-bottom: 1px solid black; border-left: none; border-image: initial;">Low</label>
                                    <input type="radio" name="background_options" id="quality_options_low" value="low" style="display: none">
                                </span>
                                <span style="flex-grow: 1; display: inherit">
                                    <label for="quality_options_med" class="ui-button ui-state-default ui-state-active" style="width: 100%; padding: 0.4em 0.1em; margin: 0px; border-radius: 0px; border-top: 1px solid black; border-right: 1px solid black; border-bottom: 1px solid black; border-left: none; border-image: initial;">Medium</label>
                                    <input type="radio" name="background_options" id="quality_options_med" value="med" style="display: none">
                                </span>
                                <span style="flex-grow: 1; display: inherit">
                                    <label for="quality_options_high" class="ui-button ui-state-default " style="width: 100%; padding: 0.4em 0.1em; margin: 0px; border-radius: 0px 4px 4px 0px; border-top: 1px solid black; border-right: 1px solid black; border-bottom: 1px solid black; border-left: none; border-image: initial;">High</label>
                                    <input type="radio" name="background_options" id="quality_options_high" value="high" style="display: none">
                                </span>
                            </span>
                        </fieldset>
                    </selectgroup>
                </div>
            </span>
        `);

        {   // QUALITY TOGGLES  ---- TODO
            document.getElementById("quality_options_high").addEventListener("click", (el) => {
                elToolbar.find("label[for=quality_options_med]").removeClass("ui-state-active");
                elToolbar.find("label[for=quality_options_high]").addClass("ui-state-active");
                viewer.setPointBudget(10_000_000);
            });
        }

        {   // POINTCLOUD MESH AND RECON TOGGLES
            elToolbar.find("img[name=action_point]").click( () => {
                viewer.scene.pointclouds.forEach( pc => pc.visible = !pc.visible);
            });


            elToolbar.find("img[name=action_recon]").click( () => {
                viewer.scene.scene.children.forEach( rc => {
                    if(rc.name.includes('recon') && selector == rc.name.split(" ")[0]) {
                        if(rc.name.includes('reconline')) {
                                console.log(rc)
                                rc.material.color.setHex(0x4d3319);
                            }
                        rc.visible = !rc.visible; 
                        
                    }
                });
            });

            elToolbar.find("img[name=action_mesh]").click( () => {
                console.log("mesh");
                viewer.scene.scene.children.forEach( ms => {
                    console.log(ms.name.split(' ')[0]);
                    if (ms.name &&  ms.name.split(' ')[0] == selector) {
                        console.log(ms.name.split())
                        console.log(ms.name.split().length)
                        
                        if (ms.name.includes('reconline') || ms.name.split(' ').length == 1) {
                            ms.visible = !ms.visible;
                            if(ms.name.includes('reconline')) {
                                console.log(ms)
                                ms.material.color.setHex(0xecd9c6);
                            }
                        }
                    }

                });
            });
        }

        { // MEASUREMENT TOOLS
            elToolbar.find("img[name=action_measure_point]").click( () => {
                const measurement = viewer.measuringTool.startInsertion({
                    showDistances: false,
                    showAngles: false,
                    showCoordinates: true,
                    showArea: false,
                    closed: true,
                    maxMarkers: 1,
                    name: 'Point'
                });
            });

            elToolbar.find("img[name=action_measure_distance]").click( () => {
                const measurement = viewer.measuringTool.startInsertion({
                    showDistances: true,
                    showArea: false,
                    closed: false,
                    name: 'Distance'
                });
            });

            elToolbar.find("img[name=action_measure_circle]").click( () => {
                const measurement = viewer.measuringTool.startInsertion({
                    showDistances: false,
                    showHeight: false,
                    showArea: false,
                    showCircle: true,
                    showEdges: false,
                    closed: false,
                    maxMarkers: 3,
                    name: 'Circle'
                });
            });
        }

        //Initialize Cesium Viewer
        // window.CESIUM_BASE_URL = Potree.resourcePath + "/../libs/Cesium";
        window.cesiumViewer = new Cesium.Viewer('cesiumContainer', {
            useDefaultRenderLoop: false,
            animation: false,
            baseLayerPicker : false,
            fullscreenButton: false, 
            geocoder: false,
            homeButton: false,
            infoBox: false,
            sceneModePicker: false,
            selectionIndicator: false,
            timeline: false,
            navigationHelpButton: false,
            // imageryProvider : Cesium.createOpenStreetMapImageryProvider({url : 'https://a.tile.openstreetmap.org/'}),
            imageryProvider: new Cesium.BingMapsImageryProvider({
                url : 'https://dev.virtualearth.net',
                key : 'AkUghO_-dVbRnryWxAF63Uhb-NPNq7zo-wGinQMlqaMazeHNMyC3qoRq7sH-V_Jj',
                mapStyle : Cesium.BingMapsStyle.AERIAL
                }),
            terrainShadows: Cesium.ShadowMode.DISABLED,
        });

        // Set Cesium location. I don't think this does anything
        // let cp = new Cesium.Cartesian3(281238.4, 4632572.1, 15729.4);
        // cesiumViewer.camera.setView({
        //     destination : cp,
        //     orientation: {
        //         heading : 10, 
        //         pitch : -Cesium.Math.PI_OVER_TWO * 0.5, 
        //         roll : 0.0 
        //     }
        // });

        //Initialize Potree viewer and scene
        window.viewer = new Potree.Viewer(document.getElementById("potree_render_area"), {
            useDefaultRenderLoop: false //This setting is necessary to get cesium to work
        });
        let scene = window.viewer.scene;
        let aRoot = scene.annotations;

        //Configure viewer settings
        window.viewer.setDescription("");
        window.viewer.setEDLEnabled(true);
        window.viewer.setFOV(60);
        window.viewer.setPointBudget(3_000_000);
        window.viewer.loadSettingsFromURL();
        window.viewer.setBackground(null);
        window.viewer.setControls(window.viewer.earthControls);
        window.viewer.useHQ = true;
	
		
		// Lights
		let directionalLight, pointLight, ambientLight, hemiLight;

		hemiLight = new THREE.HemisphereLight(0xffeeb1, 0x080820, 2);
		window.viewer.scene.scene.add(hemiLight);

		window.viewer.pRenderer.threeRenderer.toneMapping = THREE.ReinhardToneMapping;
		window.viewer.pRenderer.threeRenderer.toneMappingExposure = 2.3;
		window.viewer.pRenderer.threeRenderer.shadowMap.enabled = true;

		pointLight = new THREE.SpotLight(0xffa95c, 4);
		pointLight.castShadow = true;
		pointLight.shadow.bias = -0.0001;
		pointLight.shadow.mapSize.width = 1024*4;
		pointLight.shadow.mapSize.height = 1024*4;
		viewer.scene.scene.add(pointLight);
        
        //Set initial view
        viewer.scene.view.position.set(data.view.pos[0], data.view.pos[1], data.view.pos[2]);
		viewer.scene.view.lookAt(data.view.lookAt[0], data.view.lookAt[1], data.view.lookAt[2]);

        //Load Potree GUI
        window.viewer.loadGUI(() => {
            potreeViewer.setLanguage('en');
            $("#menu_appearance").next().show();
        });

        // Load pointcloud
        Potree.loadPointCloud("http://10.0.0.229:8080/metadata.json", "lion", function(e){
            //Initialize some important variable
            let pointcloud = e.pointcloud;
			let material = pointcloud.material;

            //Add pointcloud to seen
            scene.addPointCloud(pointcloud);

            //Place and orient pointcloud so that it lines up with cesium
            pointcloud.position.set(data.pos[0], data.pos[1], data.pos[2]);
		    pointcloud.rotation.set(0, 0, data.rot);

            //Setting for material
            material.pointSizeType = Potree.PointSizeType.ATTENUATED;
            material.size = data.materialSize;

            //Create projections
            let pointcloudProjection = "+proj=utm +zone=33 +ellps=WGS84 +datum=WGS84 +units=m +no_defs";
			let mapProjection = proj4.defs("WGS84");

			window.toMap = proj4(pointcloudProjection, mapProjection);
			window.toScene = proj4(mapProjection, pointcloudProjection);

            {//Declare bounding box and projections. I believe Cesium uses these
                let bb = window.viewer.getBoundingBox();

                let minWGS84 = proj4(pointcloudProjection, mapProjection, bb.min.toArray());
                let maxWGS84 = proj4(pointcloudProjection, mapProjection, bb.max.toArray());
            }

            //Add annotations
            let anno = new Potree.Annotation({
                title: "Test",
                position: [291276, 4640928, 35],
                cameraPosition: [291294, 4640953, 30],
                cameraTarget: [291276, 4640929, 21]
            });
            aRoot.add(anno);
            // let addAnno = function(currAnno, parAnno){
            //     let anno = new Potree.Annotation({
            //         title: currAnno.title,
            //         position: [291276, 4640928, 35],
            //         cameraPosition: [291294, 4640953, 30],
            //         cameraTarget: [291276, 4640929, 21],
            //     });

            //     if (currAnno.children){
            //         for (let i = 0; i < currAnno.children.length; i++){
            //             addAnno(currAnno.children[i], anno);
            //         }
            //     }

            //     parAnno.add(anno);
            // }

            // if (data.annos){
            //     for (let i = 0; i < data.annos.length; i++){
            //         addAnno(data.annos[i], aRoot);
            //     }
            // }
        });//end load pointcloud

        // //Create lighting for meshes
        // const light = new THREE.AmbientLight(); // soft white light
        // scene.scene.add( light );

        // load mesh
		loader.load(Potree.resourcePath + "/models/toaf.ply", (geometry) => {
			const textureLoader = new THREE.TextureLoader();

			const diffuseMap = textureLoader.load(Potree.resourcePath + "/models/toaf_tex.jpg");
			diffuseMap.encoding = THREE.sRGBEncoding;

			const normalMap = textureLoader.load(Potree.resourcePath + "/models/toaf_norm.jpg");
			normalMap.encoding = THREE.sRGBEncoding;

			geometry.computeVertexNormals();

			let mesh;
			{
				const material = new THREE.MeshStandardMaterial({
					color: 0xffffff,
					roughness: 0.5,
					map: diffuseMap,
					normalMap: normalMap,
					normalMapType: THREE.ObjectSpaceNormalMap,
				});
				mesh = new THREE.Mesh(geometry, material);
				// mesh.position.set(48.5, 238.5, -13);
                mesh.position.set(570547.7, 5400268.1, 62.2);
				mesh.rotation.set(0, 0, -Math.PI * .19);
				mesh.visible = true;

				scene.scene.add(mesh);
			}

            //This adds the mesh to the sidebar. Since we don't use the sidebar we do not need this
			viewer.onGUILoaded(() => {
				// Add entries to object list in sidebar
				let tree = $(`#jstree_scene`);
				let parentNode = "other";

				let meshID = tree.jstree('create_node', parentNode, {
					"text": "Temple of Antoninus and Faustina",
					"icon": `${Potree.resourcePath}/icons/triangle.svg`,
					"data": geometry
				},
					"last", false, false);
				tree.jstree(mesh.visible ? "check_node" : "uncheck_node", meshID);

			});
        });

        // Add annotations
        // if (data.annos){
        //     for (let i = 0; i < data.annos.length; i++){
        //         this.addAnno(data.annos[i], aRoot);
        //     }
        // }

        //Add event listner for mouse movement. This allows us to get pointcloud intersection with mouse
        window.viewer.renderer.domElement.addEventListener('mousedown', (event) => {
            if (this.showIntersectionOnClick){
                let mouseLoc = window.viewer.inputHandler.mouse;
                let camera = scene.getActiveCamera();
                console.log(Potree.Utils);

                let hit = Potree.Utils.getMousePointCloudIntersection(mouseLoc, camera, viewer, scene.pointclouds);
                console.log(hit);
            }
        });

        //Add event listener for cesium coords
        let handler = new Cesium.ScreenSpaceEventHandler(viewer.scene.canvas);
        handler.setInputAction((event) => {
            if (this.showIntersectionOnClick){
                let ray = window.cesiumViewer.camera.getPickRay(event.position);
                let cartesian = window.cesiumViewer.scene.globe.pick(ray, window.cesiumViewer.scene);
                let cartographic = Cesium.Cartographic.fromCartesian(cartesian);
                let lng = Cesium.Math.toDegrees(cartographic.longitude); // longitude
                let lat = Cesium.Math.toDegrees(cartographic.latitude); // latitude
                let alt = cartographic.height; // height
                let coordinate = {
                    longitude: Number(lng.toFixed(6)),
                    latitude: Number(lat.toFixed(6)),
                    altitude: Number(alt.toFixed(2))
                };
                console.log(cartesian);
                console.log(coordinate);
            }
        }, Cesium.ScreenSpaceEventType.LEFT_CLICK);

        function loop(timestamp){
            window.requestAnimationFrame(loop);

            window.viewer.update(window.viewer.clock.getDelta(), timestamp);

            window.viewer.render();

            //Light position
            pointLight.position.set(
				viewer.scene.cameraP.position.x + 10,
				viewer.scene.cameraP.position.y + 10,
				viewer.scene.cameraP.position.z + 10
			);
            
            if(window.toMap !== undefined){
                {
                    let camera = window.viewer.scene.getActiveCamera();

                    let pPos		= new THREE.Vector3(0, 0, 0).applyMatrix4(camera.matrixWorld);
                    let pRight  = new THREE.Vector3(600, 0, 0).applyMatrix4(camera.matrixWorld);
                    let pUp		 = new THREE.Vector3(0, 600, 0).applyMatrix4(camera.matrixWorld);
                    let pTarget = window.viewer.scene.view.getPivot();

                    let toCes = (pos) => {
                        let xy = [pos.x, pos.y];
                        let height = pos.z;
                        let deg = toMap.forward(xy);
                        let cPos = Cesium.Cartesian3.fromDegrees(...deg, height);

                        return cPos;
                    };

                    let cPos = toCes(pPos);
                    let cUpTarget = toCes(pUp);
                    let cTarget = toCes(pTarget);

                    let cDir = Cesium.Cartesian3.subtract(cTarget, cPos, new Cesium.Cartesian3());
                    let cUp = Cesium.Cartesian3.subtract(cUpTarget, cPos, new Cesium.Cartesian3());

                    cDir = Cesium.Cartesian3.normalize(cDir, new Cesium.Cartesian3());
                    cUp = Cesium.Cartesian3.normalize(cUp, new Cesium.Cartesian3());

                    window.cesiumViewer.camera.setView({
                        destination : cPos,
                        orientation : {
                            direction : cDir,
                            up : cUp
                        }
                    });
                    
                }

                let aspect = window.viewer.scene.getActiveCamera().aspect;
                if(aspect < 1){
                    let fovy = Math.PI * (window.viewer.scene.getActiveCamera().fov / 180);
                    window.cesiumViewer.camera.frustum.fov = fovy;
                }else{
                    let fovy = Math.PI * (window.viewer.scene.getActiveCamera().fov / 180);
                    let fovx = Math.atan(Math.tan(0.5 * fovy) * aspect) * 2
                    window.cesiumViewer.camera.frustum.fov = fovx;
                }  
            }
            window.cesiumViewer.render();
        }
        window.requestAnimationFrame(loop);
    },

    methods: {
        displayCameraPos(){
            console.log(window.viewer.scene.getActiveCamera());
        },
        
        addArrays(arr1, arr2){
            console.log(arr1, " --- ", arr1[0] + arr2[0]);
            //Adds elements in arr2 to arr1. arr1 better not be longer than arr2
            for (let i = 0; i < arr1.length; i++){
                arr1[i] += arr2[i];
            }

            console.log(arr1);
            return arr1;
        },

        transformCoords(coords){
            let len = Math.sqrt(coords[0] * coords[0] + coords[1] * coords[1] + coords[2] * coords[2]);
            let angle = Math.atan(coords[1] / coords[0]);
            
        },

        addAnno(currAnno, parAnno){
            console.log(currAnno);
            console.log(parAnno);
            let anno = new Potree.Annotation({
				title: currAnno.title,
                position: currAnno.position,
                cameraPosition: currAnno.cameraPosition,
                cameraTarget: currAnno.cameraTarget
			});
            parAnno.add(anno);

            if (currAnno.children){
                for (let i = 0; i < currAnno.children.length; i++){
                    this.addAnno(currAnno.children[i], anno);
                }
            }
        }
        
    },
}

</script>

<style>
    /* This import statement is necessary to make annotations appear correctly */
    @import "../../public/build/potree/potree.css";
    /* This import statement is necessary to make cesium work */
    @import "../../public/libs/Cesium/Widgets/CesiumWidget/CesiumWidget.css";
    @import "../../public/libs/jquery-ui/jquery-ui.min.css"; 
    @import "../../public/libs/openlayers3/ol.css";
    @import "../../public/libs/spectrum/spectrum.css";
    @import "../../public/libs/jstree/themes/mixed/style.css";

    div.annotation {    
        opacity: 1 !important;
    }
    /* div.annotation-titlebar {
        background-color: white;
        color: black;
    } */
    .popup {
        position: fixed;
        top: 5%;
        right: 5%;
        width: 20%;
        z-index: 10000;
        background-color: rgba(255, 255, 255, 0.8);
        padding: 10px;
        border-radius: 10px;
        visibility: hidden;
        font-size: 20px;
        font-family: Garamond,Baskerville,Baskerville Old Face,Hoefler Text,Times New Roman,serif;
        /* garmond */
    }
    .credits {
        position: fixed;
        bottom:0px;
        left: 0px;
        z-index: 10000;
        width: 100%;
        padding: 5px;
        display: flex;
        justify-content: space-between;
    }
    .logo {
        width: 15%;
    }
    .button {
        background-color: #d37243;
        border-radius: 10px;
        margin: 10px;
        text-decoration: none;
        text-align: center;
        display: inline-block;
        font-size: 24px;
        padding: 5px;
        color: black;
    }
    .lesson {
        position: fixed;
        top: 5%;
        right: 5%;
        width: 20%;
        z-index: 9000;
        background-color: rgba(255, 255, 255, 0.8);
        padding: 10px;
        border-radius: 10px;
        visibility: hidden;
        font-size: 20px;
        font-family: Garamond,Baskerville,Baskerville Old Face,Hoefler Text,Times New Roman,serif;
        /* garmond */
    }
        
    #potree_toolbar{
        position: absolute; 
        z-index: 10000; 
        left: 5px; 
        top: 0px;
        background: black;
        color: white;
        padding: 0.3em 0.8em;
        font-family: "system-ui";
        border-radius: 0em 0em 0.3em 0.3em;
        display: flex;
        flex-direction: row;
    }

    .potree_menu_toggle {
        z-index: 0;
        display: none;
    }

    .potree_toolbar_label{
        text-align: center;
        font-size: smaller;
        opacity: 0.9;
    }

    .potree_toolbar_separator{
        background: white;
        padding: 0px;
        margin: 5px 10px;
        width: 1px;
    }
</style>
