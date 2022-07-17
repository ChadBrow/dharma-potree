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
// import THREE from 'three';
import proj4 from "proj4";
import $ from "jquery";

export default{
    data(){
        return {
            showIntersectionOnClick: false,
            scene: null
        }
    },

    mounted(){
        const Potree = window.Potree
        // console.log(Potree)

        // console.log(window)
        // console.log(document.getElementById("potree_render_area"));

        //Initialize Potree viewer and scene
        window.viewer = new Potree.Viewer(document.getElementById("potree_render_area"));
        let scene = window.viewer.scene;
        this.scene = scene;

        //Configure viewer settings
        window.viewer.setEDLEnabled(true);
        window.viewer.setFOV(60);
        window.viewer.setPointBudget(1_000_000);
        window.viewer.loadSettingsFromURL();

        window.viewer.setDescription("");

        //Load Potree GUI
        window.viewer.loadGUI(() => {
            window.viewer.setLanguage('en');
            // window.$("#menu_appearance").next().show();
			// window.$("#menu_tools").next().show();
			window.$("#menu_scene").next().show();
			// window.viewer.toggleSidebar();
        });

        // Load pointcloud
        Potree.loadPointCloud("./assets/pointclouds/RomeForum/metadata.json", "lion", function(e){
            //Initialize some important variable
            let pointcloud = e.pointcloud;
			let material = pointcloud.material;

            //Add pointcloud to seen
            scene.addPointCloud(pointcloud);

            //Setting for material
            material.size = 1;
            material.pointSizeType = Potree.PointSizeType.ATTENUATED;

            window.viewer.fitToScreen();

            //Create projections
            let pointcloudProjection = e.pointcloud.projection;
			let mapProjection = proj4.defs("WGS84");

			window.toMap = proj4.defs(pointcloudProjection, mapProjection);
			window.toScene = proj4.defs(mapProjection, pointcloudProjection);

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
			// }
        });

        //Add event listner for mouse movement. This allows us to get pointcloud intersection with mouse
        window.viewer.renderer.domElement.addEventListener('mousedown', (event) => {
            if (this.showIntersectionOnClick){
                let mouseLoc = window.viewer.inputHandler.mouse;
                let camera = scene.getActiveCamera();

                let hit = Potree.Utils.getMousePointCloudIntersection(mouseLoc, camera, viewer, scene.pointclouds);
                console.log(hit);
            }
        });
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
    /* @import "../../public/libs/jquery-ui/jquery-ui.min.css"; */
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
