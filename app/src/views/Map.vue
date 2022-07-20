<template>
    <div id="potree_container" style="position: absolute; width: 100%; height: 100%; left: 0px; top: 0px; ">
        <!-- <v-container style="height: 5%; padding: 0">
                <v-btn 
                    v-on:click="()=>{showIntersectionOnClick = !showIntersectionOnClick}" >
                    Show Intersection on Click
                </v-btn>
                <v-btn v-on:click="displayCameraPos()"> Display Camera Position</v-btn>
            </v-container> -->
        <div id="potree_render_area" style="height: 100%; width: 100%; background-image: '../build/potree/resources/images/background.jpg';">
            <div id="cesiumContainer" style="position: absolute; width: 100%; height: 100%; background-color:green"/>
            <div id="potree_toolbar">
                <v-container>
                    <v-row>
                        <v-col cols="4">
                            <v-btn 
                                v-on:click="()=>{showIntersectionOnClick = !showIntersectionOnClick}" >
                                Show Intersection on Click
                            </v-btn>
                        </v-col>
                        <v-col cols="4">
                            <v-btn v-on:click="displayCameraPos()"> Display Camera Position</v-btn>
                        </v-col>
                        <!-- <v-col cols="4">
                            <v-row>
                                <v-btn>Return to Parent Annotation</v-btn>
                            </v-row>
                            <v-row>
                                <v-btn v-on:click="returnToRoot()">Return to Root Annotation</v-btn>
                            </v-row>
                        </v-col> -->
                    </v-row>
                </v-container>
            </div>
        </div>
        <!-- <div  id="potree_sidebar_container"/> -->
    </div>
</template>

<script>   
//import libraries
// import * as THREE from 'three';
import proj4 from "proj4";
import $ from "jquery";
import * as Cesium from "cesium";

export default{
    data(){
        return {
            showIntersectionOnClick: false,
            scene: null
        }
    },

    mounted(){
        const Potree = window.Potree;

        //Initialize Cesium Viewer
        window.CESIUM_BASE_URL = Potree.resourcePath + "/../libs/Cesium";
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
            imageryProvider : new Cesium.OpenStreetMapImageryProvider({url : 'https://a.tile.openstreetmap.org/'}),
            terrainShadows: Cesium.ShadowMode.DISABLED,
        });

        //Set Cesium location
        let cp = new Cesium.Cartesian3(4303414.154026048, 552161.235598733, 4660771.704035539);
        cesiumViewer.camera.setView({
            destination : cp,
            orientation: {
                heading : 10, 
                pitch : -Cesium.Math.PI_OVER_TWO * 0.5, 
                roll : 0.0 
            }
        });

        //Initialize Potree viewer and scene
        window.viewer = new Potree.Viewer(document.getElementById("potree_render_area"), {
            useDefaultRenderLoop: false //This setting seems to be necessary to get cesium to work
        });
        let scene = window.viewer.scene;
        this.scene = scene;

        //Configure viewer settings
        window.viewer.setEDLEnabled(true);
        window.viewer.setFOV(60);
        window.viewer.setPointBudget(1_000_000);
        window.viewer.loadSettingsFromURL();

        window.viewer.setDescription("");
        
        //Set initial view
        viewer.scene.view.position.set(570975.577, 5398630.521, 1659.311);
		viewer.scene.view.lookAt(570115.285, 5400866.092, 30.009);

        //Load Potree GUI
        window.viewer.loadGUI(() => {
            potreeViewer.setLanguage('en');
            $("#menu_appearance").next().show();
            $("#menu_tools").next().show();
            $("#menu_scene").next().show();
			// window.viewer.toggleSidebar();
        });

        // Load pointcloud
        Potree.loadPointCloud("http://5.9.65.151/mschuetz/potree/resources/pointclouds/riegl/retz/cloud.js", "Retz",  function(e){
            //Initialize some important variable
            let pointcloud = e.pointcloud;
			let material = pointcloud.material;

            //Add pointcloud to seen
            scene.addPointCloud(pointcloud);

            //Place and orient pointcloud so that it lines up with cesium
            e.pointcloud.position.set(569277.402752, 5400050.599046, 0);
		    e.pointcloud.rotation.set(0, 0, -0.035);

            //Setting for material
            // material.pointSizeType = Potree.PointSizeType.ATTENUATED;
            material.pointSizeType = Potree.PointSizeType.ADAPTIVE;
            material.size = 0.7;
            material.elevationRange = [0, 70];
            material.weightRGB = 1.0;
            material.weightElevation = 1.0;

            //Create projections
            // let pointcloudProjection = proj4.defs(pointcloud.projection);
            let pointcloudProjection = "+proj=utm +zone=33 +ellps=WGS84 +datum=WGS84 +units=m +no_defs";
			let mapProjection = proj4.defs("WGS84");

			window.toMap = proj4.defs(pointcloudProjection, mapProjection);
			window.toScene = proj4.defs(mapProjection, pointcloudProjection);

            {
                let bb = window.viewer.getBoundingBox();

                let minWGS84 = proj4(pointcloudProjection, mapProjection, bb.min.toArray());
                let maxWGS84 = proj4(pointcloudProjection, mapProjection, bb.max.toArray());
            }

            // //I have no clue what this does
            // window.viewer.onGUILoaded(() => {
			// 	// Add entries to object list in sidebar
			// 	let tree = window.$(`#jstree_scene`);
			// 	let parentNode = "other";

			// 	let meshID = tree.jstree('create_node', parentNode, {
			// 		"text": "Temple of Antoninus and Faustina",
			// 		"icon": `${Potree.resourcePath}/icons/triangle.svg`,
			// 		"data": geometry
			// 	},
			// 		"last", false, false);
			// 	tree.jstree(mesh.visible ? "check_node" : "uncheck_node", meshID);

			// });

            // {//Add annotations
            //     //Declare root annotation
            //         let aRoot = scene.annotations;
            //     {//Base annotations

            //         //Declare base annotation
            //         let aBase = new Potree.Annotation({
            //             title: "Base Pedestal",
            //             position: [1.51, -1.98, 4.13],
            //             cameraPosition: [3.08, -4.72, 6.14],
            //             cameraTarget: [1.51, -1.98, 4.13]
            //         });
            //         aRoot.add(aBase);

            //         //Child annos
            //         let aTest1 = new Potree.Annotation({
            //             title: "Test 1",
            //             position: [0.602, -2.128, 3.733],
            //             cameraPosition: [-0.299, -3.536, 5.020],
            //             cameraTarget: [0.602, -2.128, 3.733]
            //         })
            //         aBase.add(aTest1);

            //     }

            //     {
            //         //Create title element. This is only necessary if we want to put images in the name
            //         let returnTitle = $(`
            //         <span>
            //             Tree Returns:
            //             <img name="action_return_number" src="${Potree.resourcePath}/icons/return_number.svg" class="annotation-action-icon"/>
            //             <img name="action_rgb" src="${Potree.resourcePath}/icons/rgb.png" class="annotation-action-icon"/>
            //         </span>`);

            //         //give on click effects to its two icons
            //         returnTitle.find("img[name=action_return_number]").click( () => {
            //             event.stopPropagation();
            //             material.activeAttributeName = "return_number";
            //             material.pointSizeType = Potree.PointSizeType.FIXED;
            //             material.size = 5;
            //             window.viewer.setClipTask(Potree.ClipTask.SHOW_INSIDE);
            //         });
                    
            //         returnTitle.find("img[name=action_rgb]").click( () => {
            //             event.stopPropagation();
            //             material.activeAttributeName = "rgba";
            //             material.pointSizeType = Potree.PointSizeType.ADAPTIVE;
            //             material.size = 1;
            //             window.viewer.setClipTask(Potree.ClipTask.HIGHLIGHT);
            //         });

            //         returnTitle.toString = () => "Tree Returns";
                    

            //         let aTreeReturns = new Potree.Annotation({
            //             title: returnTitle,
            //             position: [0.807, -1.700, 6.999],
            //             cameraPosition: [5.141, -7.602, 9.546],
            //             cameraTarget: [0.807, -1.700, 6.999],
            //         });
            //         aRoot.add(aTreeReturns);
            //         // aTreeReturns.domElement.find(".annotation-action-icon:first").css("filter", "invert(1)");
            //     }
			// }// end load annotations
        });//end load pointcloud

        //Add event listner for mouse movement. This allows us to get pointcloud intersection with mouse
        window.viewer.renderer.domElement.addEventListener('mousedown', (event) => {
            if (this.showIntersectionOnClick){
                let mouseLoc = window.viewer.inputHandler.mouse;
                let camera = scene.getActiveCamera();

                let hit = Potree.Utils.getMousePointCloudIntersection(mouseLoc, camera, viewer, scene.pointclouds);
                console.log(hit);
            }
        });

        function loop(timestamp){
            requestAnimationFrame(loop);
            console.log("We do a little looping...");

            window.viewer.update(window.viewer.clock.getDelta(), timestamp);

            window.viewer.render();

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

                    window.viewer.camera.setView({
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
                    window.viewer.camera.frustum.fov = fovy;
                }else{
                    let fovy = Math.PI * (window.viewer.scene.getActiveCamera().fov / 180);
                    let fovx = Math.atan(Math.tan(0.5 * fovy) * aspect) * 2
                    window.viewer.camera.frustum.fov = fovx;
                }
                        
            }
            window.cesiumViewer.render();
        }
        requestAnimationFrame(loop);
    },
    methods: {
        displayCameraPos(){
            console.log(window.viewer.scene.getActiveCamera());
        },
        returnToRoot(){
            console.log(this.scene);
        },
        
    },
}

</script>

<style>
    /* This import statement is necessary to make annotations appear correctly */
    @import "../../public/build/potree/potree.css";
    /* This import statement is necessary to make cesium work */
    @import "../../public/libs/Cesium/Widgets/CesiumWidget/CesiumWidget.css";
    /* @import "../../public/libs/jquery-ui/jquery-ui.min.css";
    @import "../../public/libs/openlayers3/ol.css";
    @import "../../public/libs/spectrum/spectrum.css";
    @import "../../public/libs/jstree/themes/mixed/style.css"; */

    #potree_toolbar{
        position: absolute; 
        z-index: 10000; 
        top: 0px;
        background: rgba(255, 255, 255, 0.5);
        color: white;
        padding: 0.3em 0.8em;
        font-family: "system-ui";
        border-radius: 0em 0em 0.3em 0.3em;
        /* display: flex;
        flex-direction: row; */
        height: 8%;
        width: 50%;
    }
</style>
