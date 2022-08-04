<template>
    <div id="potree_container" style="position: absolute; width: 100%; height: 100%; left: 0px; top: 0px; ">
        <div id="potree_render_area">
            <div id="potree_toolbar">
                <v-toolbar rounded style="outline: 2px solid #d87444">
                    <v-container>
                        <v-row class="height: 20%" full-width justify="center">
                            <div>Models</div>
                        </v-row>
                        <v-row class="height: 80%">
                            <v-col justify="center" md="4">
                                <v-btn v-on:click="togglePointcloud()" icon title="Toggle Pointcloud">
                                    <v-icon>mdi-image-filter-hdr</v-icon>
                                </v-btn>
                            </v-col>
                            <v-col justify="center" md="4">
                                <v-btn v-on:click="toggleMesh()" icon title="Toggle Mesh">
                                    <v-icon>mdi-home-variant</v-icon>
                                </v-btn>
                            </v-col>
                            <v-col justify="center" md="4">
                                <v-btn v-on:click="toggleRecon()" icon title="Toggle Reconstruction">
                                    <v-icon>mdi-cube-outline</v-icon>
                                </v-btn>
                            </v-col>
                        </v-row>
                    </v-container>
                    <v-divider color="#d87444"/>
                    <v-container>
                        <v-row class="height: 20%" full-width justify="center">
                            <div>Navigation</div>
                        </v-row>
                        <v-row class="height: 80%" justify="center">
                            <v-col justify="center">
                                <v-btn v-on:click="toggleMesh()" icon title="Return">
                                    <v-icon>mdi-keyboard-return</v-icon>
                                </v-btn>
                            </v-col>
                            <v-col justify="center">
                                <v-btn v-on:click="toggleRecon()" icon title="Return to Start">
                                    <v-icon>mdi-cube-outline</v-icon>
                                </v-btn>
                            </v-col>
                        </v-row>
                    </v-container>
                    <!-- <v-btn icon>
                        <v-icon>mdi-magnify</v-icon>
                    </v-btn>

                    <v-btn icon>
                        <v-icon>mdi-heart</v-icon>
                    </v-btn>

                    <v-btn icon>
                        <v-icon>mdi-dots-vertical</v-icon>
                    </v-btn> -->
                </v-toolbar>
			</div>
            <div id="cesiumContainer" style="position: absolute; width: 100%; height: 100%; background-color:green;"/>
        </div>
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
            data: null,
            parentAnno: null,
            selectedMesh: null,
            selectedLine: null,
            selectedRecon: null
            
        }
    },

    mounted(){
        //Load data about current map
        let data = require("../data/roman_forum.json");
        this.data = data;

        //Declare Potree and mesh loader
        const Potree = window.Potree;
        this.loader = new PLYLoader();

        let resourcePath = '../resources';

        //Make Toolbar 
        // const elToolbar = $("#potree_toolbar");
        // elToolbar.html(`
        //     <span>
        //         <div class="potree_toolbar_label">
        //             View
        //         </div>
        //         <div>
        //             <img title="toggle mesh" name="action_mesh" src="${resourcePath}/icons/triangle.svg" class="annotation-action-icon" style="width: 2em; height: auto;"/>
        //             <img title="toggle reconstructions" name="action_recon" src="${resourcePath}/icons/navigation_cube.svg" class="annotation-action-icon" style="width: 2em; height: auto;"/>
        //             <img title="toggle pointcloud" name="action_point" src="${resourcePath}/icons/rgb.svg" class="annotation-action-icon" style="width: 2em; height: auto;"/>
        //         </div>
        //     </span>
        //     <span class="potree_toolbar_separator" />
        //     <span>
        //         <div class="potree_toolbar_label">
        //             Measure
        //         </div>
        //         <div>
        //             <img title="press esc to clear all measurements" name="action_measure_point" src="${resourcePath}/icons/point.svg" class="annotation-action-icon" style="width: 2em; height: auto;"/>
        //             <img title="press esc to clear all measurements" name="action_measure_distance" src="${resourcePath}/icons/distance.svg" class="annotation-action-icon" style="width: 2em; height: auto;"/>
        //         </div>
        //     </span>
        //     <span class="potree_toolbar_separator" />
        //     <span>
        //         <div class="potree_toolbar_label">
        //             Quality
        //         </div>
        //         <div>
        //             <selectgroup id="quality_options"
        //                 <fieldset style="border:none; margin: 0px; padding: 0px;">
        //                     <legend></legend>
        //                     <span style="display:flex">
        //                         <span style="flex-grow: 1; display: inherit">	
        //                             <label for="quality_options_low" class="ui-button ui-state-default" style="width: 100%; padding: 0.4em 0.1em; margin: 0px; border-radius: 4px 0px 0px 4px; border-top: 1px solid black; border-right: 1px solid black; border-bottom: 1px solid black; border-left: none; border-image: initial;">Low</label>
        //                             <input type="radio" name="background_options" id="quality_options_low" value="low" style="display: none">
        //                         </span>
        //                         <span style="flex-grow: 1; display: inherit">
        //                             <label for="quality_options_med" class="ui-button ui-state-default ui-state-active" style="width: 100%; padding: 0.4em 0.1em; margin: 0px; border-radius: 0px; border-top: 1px solid black; border-right: 1px solid black; border-bottom: 1px solid black; border-left: none; border-image: initial;">Medium</label>
        //                             <input type="radio" name="background_options" id="quality_options_med" value="med" style="display: none">
        //                         </span>
        //                         <span style="flex-grow: 1; display: inherit">
        //                             <label for="quality_options_high" class="ui-button ui-state-default " style="width: 100%; padding: 0.4em 0.1em; margin: 0px; border-radius: 0px 4px 4px 0px; border-top: 1px solid black; border-right: 1px solid black; border-bottom: 1px solid black; border-left: none; border-image: initial;">High</label>
        //                             <input type="radio" name="background_options" id="quality_options_high" value="high" style="display: none">
        //                         </span>
        //                     </span>
        //                 </fieldset>
        //             </selectgroup>
        //         </div>
        //     </span>
        //     <span class="potree_toolbar_separator" />
        //     <span>
        //         <div class="potree_toolbar_label">
        //             Navigation
        //         </div>
        //         <button name="return_to_parent" class="ui-button" style="border-radius: 4px">
        //             Return
        //         </button>

        //     </span>
        // `);

        // {   // QUALITY TOGGLES  ---- TODO
        //     document.getElementById("quality_options_high").addEventListener("click", (el) => {
        //         elToolbar.find("label[for=quality_options_med]").removeClass("ui-state-active");
        //         elToolbar.find("label[for=quality_options_high]").addClass("ui-state-active");
        //         viewer.setPointBudget(10_000_000);
        //     });
        // }

        // {   // POINTCLOUD MESH AND RECON TOGGLES
        //     elToolbar.find("img[name=action_point]").click( () => {
        //         viewer.scene.pointclouds.forEach( pc => pc.visible = !pc.visible);
        //     });


        //     elToolbar.find("img[name=action_recon]").click( () => {
        //         // viewer.scene.scene.children.forEach( rc => {
        //         //     if(rc.name.includes('recon') && selector == rc.name.split(" ")[0]) {
        //         //         if(rc.name.includes('reconline')) {
        //         //                 console.log(rc)
        //         //                 rc.material.color.setHex(0x4d3319);
        //         //             }
        //         //         rc.visible = !rc.visible; 
                        
        //         //     }
        //         // });
        //         if (this.selectedRecon){
        //             this.selectedRecon.visible = !this.selectedRecon.visible;
        //         }
        //         if (this.selectedLine){
        //             this.selectedLine.material.color.setHex(0x4d3319);
        //             this.selectedLine.visible = !this.selectedLine.visible;
        //         }
        //     });

        //     elToolbar.find("img[name=action_mesh]").click( () => {
        //         // console.log("mesh");
        //         // viewer.scene.scene.children.forEach( ms => {
        //         //     console.log(ms.name.split(' ')[0]);
        //         //     if (ms.name &&  ms.name.split(' ')[0] == selector) {
        //         //         console.log(ms.name.split())
        //         //         console.log(ms.name.split().length)
                        
        //         //         if (ms.name.includes('reconline') || ms.name.split(' ').length == 1) {
        //         //             ms.visible = !ms.visible;
        //         //             if(ms.name.includes('reconline')) {
        //         //                 console.log(ms)
        //         //                 ms.material.color.setHex(0xecd9c6);
        //         //             }
        //         //         }
        //         //     }

        //         // });
        //         if (this.selectedMesh){
        //             this.selectedMesh.visible = !this.selectedMesh.visible;
        //         }
        //         if (this.selectedLine){
        //             this.selectedLine.material.color.setHex(0xecd9c6);
        //             this.selectedLine.visible = !this.selectedLine.visible;
        //         }
        //     });
        // }

        // { // MEASUREMENT TOOLS
        //     elToolbar.find("img[name=action_measure_point]").click( () => {
        //         const measurement = viewer.measuringTool.startInsertion({
        //             showDistances: false,
        //             showAngles: false,
        //             showCoordinates: true,
        //             showArea: false,
        //             closed: true,
        //             maxMarkers: 1,
        //             name: 'Point'
        //         });
        //     });

        //     elToolbar.find("img[name=action_measure_distance]").click( () => {
        //         const measurement = viewer.measuringTool.startInsertion({
        //             showDistances: true,
        //             showArea: false,
        //             closed: false,
        //             name: 'Distance'
        //         });
        //     });

        //     elToolbar.find("img[name=action_measure_circle]").click( () => {
        //         const measurement = viewer.measuringTool.startInsertion({
        //             showDistances: false,
        //             showHeight: false,
        //             showArea: false,
        //             showCircle: true,
        //             showEdges: false,
        //             closed: false,
        //             maxMarkers: 3,
        //             name: 'Circle'
        //         });
        //     });
        // }

        // {
        //     elToolbar.find("button[name=return_to_parent]").click( () => {
        //         this.returnToParent();
        //     });
        // }

        //Initialize Cesium Viewer
        // window.CESIUM_BASE_URL = Potree.resourcePath + "/../libs/Cesium";
        window.cesiumViewer = new Cesium.Viewer('cesiumContainer', {
            // sceneMode : Cesium.SceneMode.COLUMBUS_VIEW,
            // mapProjection: new Cesium.WebMercatorProjection(Cesium.Ellipsoid.WGS84),
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

        //Initialize Potree viewer and scene
        window.viewer = new Potree.Viewer(document.getElementById("potree_render_area"), {
            useDefaultRenderLoop: false //This setting is necessary to get cesium to work
        });
        let scene = window.viewer.scene;

        //Configure viewer settings
        window.viewer.setDescription("");
        window.viewer.setEDLEnabled(true);
        window.viewer.setFOV(60);
        window.viewer.setPointBudget(3_000_000);
        window.viewer.loadSettingsFromURL();
        window.viewer.setBackground(null);
        window.viewer.setControls(window.viewer.earthControls);
        // window.viewer.setControls(window.viewer.fpControls);
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
		window.viewer.scene.scene.add(pointLight);
        
        //Set initial view
        // viewer.scene.view.position.set(data.view.pos[0], data.view.pos[1], data.view.pos[2]);
		// viewer.scene.view.lookAt(data.view.lookAt[0], data.view.lookAt[1], data.view.lookAt[2]);
        window.viewer.scene.view.position.set(data.view.pos[0], data.view.pos[1], data.view.pos[2]);
		window.viewer.scene.view.lookAt(data.view.lookAt[0], data.view.lookAt[1], data.view.lookAt[2]);

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

            //We do not place the pointcloud. Cesium gets oriented instead

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
        });//end load pointcloud

        // //Create lighting for meshes
        // const light = new THREE.AmbientLight(); // soft white light
        // scene.scene.add( light );

        // ADD ANNOTATIONS
        // //First declare aRoot
        let aRoot = scene.annotations;

        data.annos.forEach((anno) => {
            this.addParentAnno(anno, aRoot);
        });
        this.parentAnno = aRoot;

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

                    // let pPos		= new THREE.Vector3(0, 0, 0).applyMatrix4(camera.matrixWorld);
                    // let pRight  = new THREE.Vector3(600, 0, 0).applyMatrix4(camera.matrixWorld);
                    let pUp		 = new THREE.Vector3(0, 600, 0).applyMatrix4(camera.matrixWorld);
                    let pPos = new THREE.Vector3(0, 0, 0).applyMatrix4(camera.matrixWorld); //Gets camera position relative to origin
                    let pTarget = scene.view.getPivot(); //Gets camera target relative to origin
                    pPos.applyAxisAngle(new THREE.Vector3(0, 0, 1), data.rot); //Rotate vectors around origin
                    pTarget.applyAxisAngle(new THREE.Vector3(0, 0, 1), data.rot);
                    
                    //Offset the viewer by the position of the pointcloud
                    pPos.x += data.pos[0];
                    pPos.y += data.pos[1];
                    pPos.z += 20;
                    pUp.y += data.pos[1];
                    pTarget.x += data.pos[0];
                    pTarget.y += data.pos[1];
                    pTarget.z += 20;

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
                    cUp = Cesium.Cartesian3.normalize(cUpTarget, new Cesium.Cartesian3());

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
            let x = coords[0] + 17.3;
            let y = coords[1] - 23.31;
            let len = Math.sqrt((x * x) + (y * y));
            let angle = Math.atan(y / x);
            // angle *= -1;
            // angle += this.data.rot;
            // angle = angle * -1;

            console.log([291275.97 + len * Math.cos(angle), 4640928.21 + len * Math.sin(angle), coords[2] + 15.71]);//z is pretty easy 

        },

        addParentAnno(currAnno, parAnno){
            //Add mesh if annotation has that
            let mesh = null;
            if (currAnno.mesh){
                this.loader.load(Potree.resourcePath + "/models/" + currAnno.mesh.name + ".ply", (geometry) => {
                    const textureLoader = new THREE.TextureLoader();

                    const diffuseMap = textureLoader.load(Potree.resourcePath + "/models/" + currAnno.mesh.name + "_tex.jpg");
                    diffuseMap.encoding = THREE.sRGBEncoding;

                    const normalMap = textureLoader.load(Potree.resourcePath + "/models/" + currAnno.mesh.name + "_norm.jpg");
                    normalMap.encoding = THREE.sRGBEncoding;

                    geometry.computeVertexNormals();

                    {
                        const material = new THREE.MeshStandardMaterial({
                            color: 0xffffff,
                            roughness: 0.5,
                            map: diffuseMap,
                            normalMap: normalMap,
                            normalMapType: THREE.ObjectSpaceNormalMap,
                        });
                        mesh = new THREE.Mesh(geometry, material);
                        mesh.position.set(currAnno.mesh.position[0], currAnno.mesh.position[1], currAnno.mesh.position[2]);
                        mesh.rotation.set(0, 0, Math.PI * currAnno.mesh.rotation);
                        mesh.name = currAnno.mesh.name;
                        mesh.visible = false;

                        mesh.traverse(n => {
                            if(n.isMesh) {
                                n.castShadow = true;
                                n.recieveShadow = true;
                                if(n.material.map) n.material.map.anisotropy = 16;
                            }
                        });

                        window.viewer.scene.scene.add(mesh);
                    }
                });
            }

            //Add recon if annotation has that
            let line = null;
            let recon = null;
            if (currAnno.recon){
                this.loader.load(Potree.resourcePath + "/models/recon/" + currAnno.recon.name + ".ply", (geometry) => {

                    // Creating and Adding lines
                    const edges = new THREE.EdgesGeometry( geometry );
                    line = new THREE.LineSegments( edges, new THREE.LineBasicMaterial( { color: 0xecd9c6 } ) );

                    line.position.set(currAnno.recon.position[0], currAnno.recon.position[1], currAnno.recon.position[2]);
                    line.rotation.set(0, 0, Math.PI * currAnno.recon.rotation) // 
                    line.name = currAnno.recon.name + " reconline"
                    line.visible = false;
                    viewer.scene.scene.add( line );


                    // Creating Recon mesh
                    {
                        const material = new THREE.MeshStandardMaterial({
                            color: 0x4d3319,
                            roughness: 0.5,
                        });

                        recon = new THREE.Mesh(geometry, material);
                        recon.position.set(currAnno.recon.position[0], currAnno.recon.position[1], currAnno.recon.position[2]);
                        recon.rotation.set(0, 0, Math.PI * currAnno.recon.rotation) //
                        recon.visible = false;
                        recon.name = currAnno.recon.name + " recon";

                        viewer.scene.scene.add(recon);
                    }
                });
            }

            let anno = new Potree.Annotation({
				title: currAnno.title,
                position: [currAnno.position[0], currAnno.position[1], currAnno.position[2]],
                cameraPosition: [currAnno.cameraPosition[0], currAnno.cameraPosition[1], currAnno.cameraPosition[2]],
                cameraTarget: [currAnno.cameraTarget[0], currAnno.cameraTarget[1], currAnno.cameraTarget[2]],
                collapseThreshold: 400
			});
            parAnno.add(anno);

            currAnno.children.forEach((child) => {this.addChildAnno(child, anno);});

            anno.addEventListener('click', () => {
                if (anno.children){
                    this.parentAnno = anno;
                    anno.collapseThreshold = 10;
                    anno.children.forEach((child) => {
                        child.visible = true;
                    });
                }
                this.selectedMesh = mesh;
                this.selectedLine = line;
                this.selectedRecon = recon;
            });
        },

        addChildAnno(currAnno, parAnno){
            let anno = new Potree.Annotation({
				title: currAnno.title,
                position: [currAnno.position[0], currAnno.position[1], currAnno.position[2]],
                cameraPosition: [currAnno.cameraPosition[0], currAnno.cameraPosition[1], currAnno.cameraPosition[2]],
                cameraTarget: [currAnno.cameraTarget[0], currAnno.cameraTarget[1], currAnno.cameraTarget[2]],
                collapseThreshold: 200
			});
            parAnno.add(anno);
            anno.visible = false;
        },

        returnToParent(){
            if (this.parentAnno.level() > 0){
                this.parentAnno.children.forEach((child) => {
                    child.visible = false;
                });
                this.parentAnno.collapseThreshold = 400;

                this.selectedMesh = null; //This could cause problems if we have nested meshes, but I think that is unlikely to happen

                this.parentAnno.moveHere(window.viewer.scene.getActiveCamera()); //This moves the camera to give a good view of the parent
                this.parentAnno = this.parentAnno.parent;
            }
            else{
                Potree.Utils.moveTo(window.viewer.scene, new THREE.Vector3(this.data.view.pos[0], this.data.view.pos[1], this.data.view.pos[2]), 
                                    new THREE.Vector3(this.data.view.lookAt[0], this.data.view.lookAt[1], this.data.view.lookAt[2])); //This moves the camera back to the start in a smooth fashion
            }
        },

        togglePointcloud(){
            window.viewer.scene.pointclouds.forEach( pc => pc.visible = !pc.visible);
        },
        toggleMesh(){
            if (this.selectedMesh){
                this.selectedMesh.visible = !this.selectedMesh.visible;
            }
            if (this.selectedLine){
                this.selectedLine.material.color.setHex(0xecd9c6);
                this.selectedLine.visible = !this.selectedLine.visible;
            }
        },
        toggleRecon(){
            if (this.selectedRecon){
                this.selectedRecon.visible = !this.selectedRecon.visible;
            }
            if (this.selectedLine){
                this.selectedLine.material.color.setHex(0x4d3319);
                this.selectedLine.visible = !this.selectedLine.visible;
            }
        },
        
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
    div.annotation-titlebar {
        background-color: white;
        color: black;
    }
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
        border-radius: 0.4em 0.4em 0.4em 0.4em;
        display: flex;
        /* flex-direction: row; */
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
