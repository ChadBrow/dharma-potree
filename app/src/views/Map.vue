<template>
    <div id="potree_container" style="position: absolute; width: 100%; height: 100%; left: 0px; top: 0px; ">
        <div id="potree_render_area">
            <div id="potree_toolbar">
                <v-app-bar rounded class="toolbar">
                    <span>
                        <div class="potree_toolbar_label">Views</div>
                        <v-btn v-on:click="togglePointcloud()" :color="!showPointcloud ? '#d87444' : ''" icon small title="Toggle Point Cloud Data">
                            <v-icon>mdi-image-filter-hdr</v-icon>
                        </v-btn>
                        <v-btn v-on:click="toggleCesium()" :color="!showCesium ? '#d87444' : ''" icon small title="Toggle Base Map">
                            <v-icon>mdi-earth</v-icon>
                        </v-btn>
                        <v-btn v-on:click="toggleMesh()" :color="!showMesh ? '#d87444' : ''" icon small title="Toggle Wire Frame Model">
                            <v-icon>mdi-cube-outline</v-icon>
                        </v-btn>
                        <v-btn v-on:click="toggleRecon()" :color="!showRecon ? '#d87444' : ''" icon small title="Toggle Reconstruction Model">
                            <v-icon>mdi-home-variant</v-icon>
                        </v-btn>
                    </span>
                    <v-divider vertical class="potree_toolbar_separator"/>
                    <span>
                        <div class="potree_toolbar_label">Navigation</div>
                        <v-btn v-on:click="returnToParent()" small outlined color="#d87444">Back</v-btn>
                        <v-btn v-on:click="returnToStart()" small outlined color="#d87444">Reset</v-btn>
                    </span>
                    <v-divider vertical class="potree_toolbar_separator"/>
                    <span>
                        <div class="potree_toolbar_label">Pointcloud Quality</div>
                        <v-btn
                            class="square-right" 
                            v-on:click="updateQuality(0)" 
                            small outlined color="#d87444" v-bind:disabled="pointcloudQuality==0">
                            Low
                        </v-btn>
                        <v-btn 
                            class="square" 
                            v-on:click="updateQuality(1)" 
                            small outlined color="#d87444" v-bind:disabled="pointcloudQuality==1">
                            Medium
                        </v-btn>
                        <v-btn 
                            class="square-left" 
                            v-on:click="updateQuality(2)" 
                            small outlined color="#d87444" v-bind:disabled="pointcloudQuality==2">
                            High
                        </v-btn>
                    </span>
                    <v-divider vertical class="potree_toolbar_separator"/>
                    <v-btn icon title="Expand Toolbar" v-on:click="toolbarExpanded = true" v-if="!toolbarExpanded">
                        <v-icon color="#d87444">mdi-chevron-right</v-icon>
                    </v-btn>
                    <span v-if="toolbarExpanded">
                        <div class="potree_toolbar_label">Camera Controls</div>
                        <v-btn
                            class="square-right" 
                            v-on:click="updateControls('earth')" 
                            small outlined color="#d87444" v-bind:disabled="controlMethod=='earth'">
                            Earth
                        </v-btn>
                        <v-btn 
                            class="square-left" 
                            v-on:click="updateControls('firstPerson')" 
                            small outlined color="#d87444" v-bind:disabled="controlMethod=='firstPerson'">
                            First Person
                        </v-btn>
                    </span>
                    <!-- Start Debug Stuff -->
                    <!-- <v-divider vertical v-if="toolbarExpanded" class="potree_toolbar_separator"/>
                    <span v-if="toolbarExpanded">
                        <div class="potree_toolbar_label">Measurements</div>
                        <v-btn icon small title="Locate Point" v-on:click="locatePoint()">
                            <v-img src="../../public/resources/icons/point.svg"/>
                        </v-btn>
                        <v-btn icon small title="Measure Distance" v-on:click="measureDistance()">
                            <v-img src="../../public/resources/icons/distance.svg"/>
                        </v-btn>
                        <v-btn v-on:click="clearMeasurements()" small outlined color="#d87444">Clear</v-btn>
                    </span>
                    <v-divider vertical v-if="toolbarExpanded" class="potree_toolbar_separator"/>
                    <span v-if="toolbarExpanded">
                        <div class="potree_toolbar_label">Debug</div>
                        <v-btn small outlined color="#d87444" v-on:click="displayAxes()">Display Axes</v-btn>
                        <v-btn small outlined color="#d87444" v-on:click="displayCameraPos()">Print Camera Position</v-btn>
                    </span> -->
                    <!-- End Debug Stuff -->
                    <v-divider vertical v-if="toolbarExpanded" class="potree_toolbar_separator"/>
                    <span v-if="toolbarExpanded">
                        <v-btn icon title="Shrink Toolbar" v-on:click="toolbarExpanded = false">
                            <v-icon color="#d87444">mdi-chevron-left</v-icon>
                        </v-btn>
                    </span>
                </v-app-bar>
			</div>
            <div id="monument_selector">
                <v-app-bar rounded dense class="toolbar">
                    <v-select color="#d87444"
                    dense :items="monuments" item-text="name" item-value="" return-object 
                    v-model="selectedMonument" v-on:change="monumentSelected()" />
                </v-app-bar>
            </div>
            <div id="cesiumContainer" style="position: absolute; width: 100%; height: 100%; background-color:green;"/>
        </div>
        <v-card class="popup" v-if="showPopup">
            <v-app-bar rounded color="#d87444" class="toolbar" style="margin-bottom: 2px">
                <v-card-title>{{popupTitle}}</v-card-title>
                <v-spacer/>
                <v-btn icon v-on:click="showPopup = false">
                    <v-icon>mdi-close</v-icon>
                </v-btn>
            </v-app-bar>
            <v-img v-if="popupImage" v-bind:src="require('../../public/resources/images/' + this.popupImage)"/>
            <v-card-text v-if="popupText" style="color: black;">
                {{popupText}}
            </v-card-text>
        </v-card>
        <div class="credits">
			<div class="logo">
				<a href="https://www.google.com/url?q=https://dharma3d.org/&amp;source=gmail-imap&amp;ust=1646262702000000&amp;usg=AOvVaw3mD5yiM9b7u91M1gzyNrJa" target="_blank">
					<img src="../../public/resources/images/DHARMA_logo_long.png" style="width: 100%;">
				</a>
			</div>
			
			<div style="background-color: rgba(255, 255, 255, 0.5); padding: 3px;" class="logo">
				<img src="../../public/resources/logo_small.png" style="max-width: 60%; max-height: 60%;">
			</div>
		</div>
    </div>
</template>

<script>   
//Import components
import AppDropdown from '../components/AppDropdown.vue'
import AppDropdownContent from '../components/AppDropdownContent.vue'
import AppDropdownItem from '../components/AppDropdownItem.vue'
//import libraries
import * as THREE from 'three';
import { PLYLoader } from "../../public/libs/three.js/loaders/PLYLoader.js";
import { OBJLoader2 } from '../../public/libs/three.js/loaders/OBJLoader2.js';
/*
make video
different view modes


//arch of augustus
main arch goes over point: 78, 183, -14
pillar top right of arch goes at point: 81, 181, -12
// for rot -0.5 scale 20
//    "position": [-955, 602.3, -13.8]


Devine Julius: I have no idea what this is, we do not have text for it
leaving the details for it here so it does not show up in the website
{
    "title": "Devine Julius",
    "position": [56.9, 185, 8],
    "cameraPosition": [47.9, 143.5, 22.1],
    "cameraTarget": [57, 202.5, -4],
    "text": "Devine Julius: Please add real text and remove placeholder coordinates",
    "children": [

    ],
    "recon": {
        "name": "Devine_Julius",
        "position": [0, 0, 0],
        "rotation": [0, 0, 0],
        "scale": [0.001, 0.001, 0.001]
    }
},

Arch of Septimus Severus Children:
{
    "title": "Arch",
    "position": [-28, 76, 2],
    "cameraPosition": [-28, 76, -8],
    "cameraTarget": [-28, 76, 2]
},
{
    "title": "Figure",
    "position": [-21, 77, -5],
    "cameraPosition": [-16, 84, -2],
    "cameraTarget": [-21, 77, -7]
}

TODO: fix spotlight casting weird shadows on models when viewed from a specific location

*/
export default{
    name: 'Map',

    components: {
        AppDropdown,
        AppDropdownContent,
        AppDropdownItem
    },

    data(){
        return {
            toolbarExpanded: false, 
            pointcloudQuality: 1,
            data: null,
            selectedMonument: {name: "No Monument Selected", event: this.returnToStar},
            monuments: [{name: "No Monument Selected", event: this.returnToStart}], 
            parentAnno: null,
            popupTitle: null,
            popupImage: null,
            popupText: null,
            showPopup: false,
            showPointcloud: true,
            showCesium: true,
            showMesh: false,
            showRecon: false,
            controlMethod: "earth"
        }
    },

    mounted(){
        //Load data about current map
        let data = require("../data/roman_forum.json");
        this.data = data;

        //Declare threejs loaders and manager
        let threeJSManager = new THREE.LoadingManager();
        threeJSManager.onStart = function ( url, itemsLoaded, itemsTotal ) {
            console.log( 'Started loading file: ' + url + '.\nLoaded ' + itemsLoaded + ' of ' + itemsTotal + ' files.' );
        };

        threeJSManager.onLoad = function ( ) {
            console.log( 'Loading complete!');
        };


        threeJSManager.onProgress = function ( url, itemsLoaded, itemsTotal ) {
            console.log( 'Loading file: ' + url + '.\nLoaded ' + itemsLoaded + ' of ' + itemsTotal + ' files.' );
        };

        threeJSManager.onError = function ( url ) {
            console.log( 'There was an error loading ' + url );
        };

        const Potree = window.Potree;
        this.plyLoader = new PLYLoader(threeJSManager);
        this.objLoader = new OBJLoader2(threeJSManager);

        //Initialize Cesium Viewer
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

        //Initialize Potree viewer and scene
        window.viewer = new Potree.Viewer(document.getElementById("potree_render_area"), {
            useDefaultRenderLoop: false //This setting is necessary to get cesium to work
        });
        let scene = window.viewer.scene;

        //Configure viewer settings
        window.viewer.setDescription("");
        window.viewer.setEDLEnabled(true);
        window.viewer.setFOV(60);
        window.viewer.loadSettingsFromURL();
        window.viewer.setBackground(null);
        window.viewer.setControls(window.viewer.earthControls);
        window.viewer.useHQ = true;

        //Initialize pointcloud budget
        window.viewer.setPointBudget(3_000_000);
		
		// Lights
		let pointLight, hemiLight;

		hemiLight = new THREE.HemisphereLight(0xffeeb1, 0x080820, 2);
		window.viewer.scene.scene.add(hemiLight);

		window.viewer.pRenderer.threeRenderer.toneMapping = THREE.ReinhardToneMapping;
		window.viewer.pRenderer.threeRenderer.toneMappingExposure = 2.3;
		window.viewer.pRenderer.threeRenderer.shadowMap.enabled = true;

        // https://threejs.org/examples/webgl_lights_spotlight.html
		pointLight = new THREE.SpotLight(0xffa95c, 4);
        pointLight.angle = Math.PI;
		pointLight.castShadow = false;

        // add the light
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
        Potree.loadPointCloud("https://dharma3dz.aws.nd.edu/pointclouds/roman-forum/metadata.json", "lion", function(e){
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
        const light = new THREE.AmbientLight(); // soft white light
        scene.scene.add( light );

        // ADD ANNOTATIONS
        // //First declare aRoot
        let aRoot = scene.annotations;

        data.annos.forEach((anno) => {
            this.addParentAnno(anno, aRoot);
        });
        this.parentAnno = aRoot;

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
            // light target position
            /*
            pointLight.target.position.set(
                viewer.scene.cameraP.target.x,
                viewer.scene.cameraP.target.y,
                viewer.scene.cameraP.target.z
            )
            */
            
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

        addParentAnno(currAnno, parAnno){
            //Create annotation object
            let anno = new Potree.Annotation({
				title: currAnno.title,
                position: [currAnno.position[0], currAnno.position[1], currAnno.position[2]],
                cameraPosition: [currAnno.cameraPosition[0], currAnno.cameraPosition[1], currAnno.cameraPosition[2]],
                cameraTarget: [currAnno.cameraTarget[0], currAnno.cameraTarget[1], currAnno.cameraTarget[2]],
                collapseThreshold: 400
			});

            //Add mesh if annotation has that
            let mesh = null;
            if (currAnno.mesh){
                this.plyLoader.load(Potree.resourcePath + "/models/" + currAnno.mesh.name + ".ply", (geometry) => {
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
                        mesh.rotation.set(Math.PI * currAnno.mesh.rotation[0], Math.PI * currAnno.mesh.rotation[1], Math.PI * currAnno.mesh.rotation[2]);
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
                        anno.meshModel = mesh;
                    }
                });
            }

            //Add recon if annotation has that
            let line = null;
            let recon = null;
            if (currAnno.recon){
                this.plyLoader.load(Potree.resourcePath + "/models/recon/" + currAnno.recon.name + ".ply", (geometry) => {

                    // Creating and Adding lines
                    const edges = new THREE.EdgesGeometry( geometry );
                    line = new THREE.LineSegments( edges, new THREE.LineBasicMaterial( { color: 0xecd9c6 } ) );

                    line.position.set(currAnno.recon.position[0], currAnno.recon.position[1], currAnno.recon.position[2]);
                    line.rotation.set(Math.PI * currAnno.recon.rotation[0], Math.PI * currAnno.recon.rotation[1], Math.PI * currAnno.recon.rotation[2]) // 
                    if (currAnno.recon.scale){
                        line.scale.set(currAnno.recon.scale[0], currAnno.recon.scale[1], currAnno.recon.scale[2]);
                    }
                    line.name = currAnno.recon.name + " reconline"
                    line.visible = false;
                    viewer.scene.scene.add( line );
                    anno.lineModel = line;


                    // Creating Recon mesh
                    {
                        const material = new THREE.MeshStandardMaterial({
                            color: 0x6e6863,
                            // color: 0xFF0000,
                            roughness: 0.5,
                        });

                        recon = new THREE.Mesh(geometry, material);
                        recon.position.set(currAnno.recon.position[0], currAnno.recon.position[1], currAnno.recon.position[2]);
                        recon.rotation.set(Math.PI * currAnno.recon.rotation[0], Math.PI * currAnno.recon.rotation[1], Math.PI * currAnno.recon.rotation[2]) //
                        if (currAnno.recon.scale){
                            recon.scale.set(currAnno.recon.scale[0], currAnno.recon.scale[1], currAnno.recon.scale[2]);
                        }
                        recon.visible = false;
                        recon.name = currAnno.recon.name + " recon";

                        viewer.scene.scene.add(recon);
                        anno.reconModel = recon;
                    }
                });
            }
            else if (currAnno.obj){//add obj if they have that instead
                this.objLoader.load(Potree.resourcePath + "/models/obj/" + currAnno.obj.name + ".obj" , ( recon ) => {
                    recon.rotation.set(Math.PI * currAnno.obj.rotation[0], Math.PI * currAnno.obj.rotation[1], Math.PI * currAnno.obj.rotation[2]) //
                    recon.scale.multiplyScalar(currAnno.obj.scale);
                    recon.position.set(currAnno.obj.position[0], currAnno.obj.position[1], currAnno.obj.position[2]);
                    recon.visible = true;
                    recon.name = currAnno.obj.name + " recon";

                    const material = new THREE.MeshStandardMaterial({
                        color: 0xFF0000,
                        roughness: 0.5,
                    });

                    recon.children.forEach((reconChild) => {
                        reconChild.material = material;
                    });

                    console.log(recon);

                    viewer.scene.scene.add(recon);
                    anno.reconModel = recon;
                } );
            }

            parAnno.add(anno);
            currAnno.children.forEach((child) => {this.addChildAnno(child, anno);});

            //Add a function that executes the on click effect. This function will be used later by the selector
            anno.clicked = () => {
                //hide currently selected anno if one is selected
                if (this.parentAnno.level() > 0){
                    this.parentAnno.children.forEach((child) => {
                        child.visible = false;
                    });
                    this.parentAnno.collapseThreshold = 400;
                }

                this.hideModels(this.parentAnno);

                this.parentAnno = anno;
                this.updateModels()

                anno.collapseThreshold = 10;
                anno.children.forEach((child) => {
                    child.visible = true;
                });

                //Display popup
                this.popupText = currAnno.text;
                this.popupImage = currAnno.image;
                this.popupTitle = currAnno.title;
                this.showPopup = true;
            };

            anno.addEventListener('click', () => {
                this.selectedMonument = {name: currAnno.title, annotation: anno}
                anno.clicked();
            });

            //Add this monument to this list of all monuments. This is used by the monument selector
            this.monuments.push({name: currAnno.title, annotation: anno})
        },

        addChildAnno(currAnno, parAnno){
            let annoTitle = $(`
                        <img src="${Potree.resourcePath}/icons/child_annotation.png" style="height: 30px">`)

            let anno = new Potree.Annotation({
				title: annoTitle,
                position: [currAnno.position[0], currAnno.position[1], currAnno.position[2]],
                cameraPosition: [currAnno.cameraPosition[0], currAnno.cameraPosition[1], currAnno.cameraPosition[2]],
                cameraTarget: [currAnno.cameraTarget[0], currAnno.cameraTarget[1], currAnno.cameraTarget[2]],
                collapseThreshold: 200
			});

            anno.addEventListener('click', () => {
                this.popupText = currAnno.text;
                this.popupImage = currAnno.image;
                this.popupTitle = currAnno.title;
                this.showPopup = true;
            });

            anno.domElement[0].firstElementChild.className = "annotation-child-titlebar";
            parAnno.add(anno);
            anno.visible = false;
        },

        //NAVIGATION
        returnToParent(){
            //Close popup if it is open
            this.showPopup = false;

            if (this.parentAnno.level() > 0){
                this.parentAnno.children.forEach((child) => {
                    child.visible = false;
                });
                this.parentAnno.collapseThreshold = 400;

                //Hide all the old parent's models
                if (this.parentAnno.meshModel){this.parentAnno.meshModel.visible = false};
                if (this.parentAnno.reconModel){this.parentAnno.reconModel.visible = false};
                if (this.parentAnno.lineModel){this.parentAnno.lineModel.visible = false};

                this.parentAnno.moveHere(window.viewer.scene.getActiveCamera()); //This moves the camera to give a good view of the parent
                this.parentAnno = this.parentAnno.parent;
                this.updateModels() //update new parent's models
            }
            else{
                Potree.Utils.moveTo(window.viewer.scene, new THREE.Vector3(this.data.view.pos[0], this.data.view.pos[1], this.data.view.pos[2]), 
                                    new THREE.Vector3(this.data.view.lookAt[0], this.data.view.lookAt[1], this.data.view.lookAt[2])); 
                                    //This moves the camera back to the start in a smooth fashion
            }
            //Reset the selected monument
            this.selectedMonument = {name: "No Monument Selected", event: this.returnToStar};
        },
        returnToStart(){
            //Close popup if it is open
            this.showPopup = false;

            if (this.parentAnno.level() > 0){
                this.parentAnno.children.forEach((child) => {
                    child.visible = false;
                });
                this.parentAnno.collapseThreshold = 400;

                //Hide all the old parent's models
                if (this.parentAnno.meshModel){this.parentAnno.meshModel.visible = false};
                if (this.parentAnno.reconModel){this.parentAnno.reconModel.visible = false};
                if (this.parentAnno.lineModel){this.parentAnno.lineModel.visible = false};

                Potree.Utils.moveTo(window.viewer.scene, new THREE.Vector3(this.data.view.pos[0], this.data.view.pos[1], this.data.view.pos[2]), 
                                    new THREE.Vector3(this.data.view.lookAt[0], this.data.view.lookAt[1], this.data.view.lookAt[2])); //This moves the camera back to the start in a smooth fashion  
                this.parentAnno = this.parentAnno.parent; //This needs to set parentAnno to aRoot TODO
                this.updateModels() //update new parent's models
            }
            else{
                Potree.Utils.moveTo(window.viewer.scene, new THREE.Vector3(this.data.view.pos[0], this.data.view.pos[1], this.data.view.pos[2]), 
                                    new THREE.Vector3(this.data.view.lookAt[0], this.data.view.lookAt[1], this.data.view.lookAt[2])); //This moves the camera back to the start in a smooth fashion
            }

            //Reset the selected monument
            this.selectedMonument = {name: "No Monument Selected", event: this.returnToStar};
        },

        //MODELS
        togglePointcloud(){
            this.showPointcloud = !this.showPointcloud;
            window.viewer.scene.pointclouds.forEach( pc => pc.visible = !pc.visible);
        },
        toggleCesium(){
            this.showCesium = !this.showCesium;
            window.cesiumViewer.scene._globe.show = !window.cesiumViewer.scene._globe.show;
            window.cesiumViewer.scene.skyBox.show = !window.cesiumViewer.scene.skyBox.show;
            window.cesiumViewer.scene.skyAtmosphere.show = !window.cesiumViewer.scene.skyAtmosphere.show;
        },
        toggleMesh(){
            this.showMesh = !this.showMesh;
            this.updateModels();
        },
        toggleRecon(){
            this.showRecon = !this.showRecon;
            this.updateModels();
        },
        updateModels(){
            if (this.parentAnno.level() > 0){
                if (this.parentAnno.meshModel) this.parentAnno.meshModel.visible = this.showMesh;
                if (this.parentAnno.reconModel) this.parentAnno.reconModel.visible = this.showRecon;
                if (this.parentAnno.lineModel) this.parentAnno.lineModel.visible = (this.showMesh || this.showRecon);
            }
            else{
                this.parentAnno.children.forEach( child => {
                    if (child.meshModel) child.meshModel.visible = this.showMesh;
                    if (child.reconModel) child.reconModel.visible = this.showRecon;
                    if (child.lineModel) child.lineModel.visible = (this.showMesh || this.showRecon);
                });
            }
        },
        hideModels(anno){
            if (anno.level() > 0){
                if (anno.meshModel) anno.meshModel.visible = false;
                if (anno.reconModel) anno.reconModel.visible = false;
                if (anno.lineModel) anno.lineModel.visible = false;
            }
            else{
                anno.children.forEach( child => {
                    if (child.meshModel) child.meshModel.visible = false;
                    if (child.reconModel) child.reconModel.visible = false;
                    if (child.lineModel) child.lineModel.visible = false;
                });
            }
        },

        //NAVIGATION CONTROLS
        updateControls(newMethod){
            //This function updates what kind of control method Potree uses for navigation
            this.controlMethod = newMethod;
            if (this.controlMethod == "earth"){
                window.viewer.setControls(window.viewer.earthControls);
            }
            else{
                window.viewer.setControls(window.viewer.fpControls);
            }

        },

        //MEASUREMENTS
        locatePoint(){
            const measurement = viewer.measuringTool.startInsertion({
                showDistances: false,
                showAngles: false,
                showCoordinates: true,
                showArea: false,
                closed: true,
                maxMarkers: 1,
                name: 'Point'
            });
        },
        measureDistance(){
            const measurement = viewer.measuringTool.startInsertion({
                showDistances: true,
                showArea: false,
                closed: false,
                name: 'Distance'
            });
        },
        clearMeasurements(){
            window.viewer.scene.removeAllMeasurements();
        },
        
        displayAxes(){
            var axesHelper = new THREE.AxesHelper( 5 );
            window.viewer.scene.scene.add( axesHelper );
        },

        //UPDATE POINTCLOUD QUALITY
        updateQuality(qual){
            if (qual == 0){
                window.viewer.setPointBudget(1_000_000);
                this.pointcloudQuality = 0;
            }
            else if (qual == 1){
                window.viewer.setPointBudget(3_000_000);
                this.pointcloudQuality = 1;
            }
            else if (qual == 2){
                window.viewer.setPointBudget(5_000_000);
                this.pointcloudQuality = 2;
            }
        },

        //Monument selector function(s)
        monumentSelected(){
            if (this.selectedMonument.annotation){
                this.selectedMonument.annotation.moveHere(window.viewer.scene.getActiveCamera());
                this.selectedMonument.annotation.clicked();
            }
            else{
                this.selectedMonument.event();
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
    div.annotation-titlebar {
        background-color: white;
        color: black;
    }
    /* div.annotation-child-titlebar{
        
    } */
    
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
    /* .lesson {
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
    } */
        
    #potree_toolbar{
        position: absolute; 
        z-index: 10000; 
        left: 5px; 
        top: 0px;
        display: flex;
    }

    #monument_selector{
        position: absolute; 
        z-index: 10001; 
        left: 10px; 
        top: 70px;
        display: flex;
    }

    .potree_toolbar_label{
        text-align: center;
        font-size: smaller;
        opacity: 0.9;
    }

    .potree_toolbar_separator{
        background: #d87444;
        align-self: center;
        margin: 5px 10px;
    }

    .popup {
        position: fixed;
        top: 5%;
        right: 5%;
        width: 30%;
        z-index: 10000;
        outline: 2px solid #d87444;
    }

    .toolbar {
        outline: 2px solid #d87444;
    }

    .square {
        border-radius: 0px;
    }
    .square-right {
        border-top-right-radius: 0px;
        border-bottom-right-radius: 0px;
    }
    .square-left {
        border-top-left-radius: 0px;
        border-bottom-left-radius: 0px;
    }
</style>
