<template>
    <div id="potree_container" style="position: absolute; width: 100%; height: 100%; left: 0px; top: 0px; ">
        <v-container style="height: 5%; padding: 0">
            <v-btn>Test</v-btn>
        </v-container>
        <div id="potree_render_area" style="height: 95%; width: 100%; background-image: '../build/potree/resources/images/background.jpg';">
        </div>
    </div>
</template>

<script>   
//import libraries
// import THREE from 'three';

export default{

    mounted(){
        const Potree = window.Potree
        console.log(Potree)

        console.log(window)
        console.log(document.getElementById("potree_render_area"));

        //Initialize Potree viewer
        window.viewer = new Potree.Viewer(document.getElementById("potree_render_area"));

        //Configure viewer settings
        // window.viewer.setEDLEnabled(true);
        window.viewer.setFOV(60);
        window.viewer.setPointBudget(1_000_000);
        window.viewer.loadSettingsFromURL();

        window.viewer.setDescription("");

        window.viewer.loadGUI(() => {
        window.viewer.setLanguage('en');
        window.$("#menu_appearance").next().show();
            viewer.toggleSidebar();   
        });

        // Load pointcloud
        Potree.loadPointCloud("./assets/pointclouds/lion_takanawa/cloud.js", "lion", function(e){
            //Initialize some important variable
            let pointcloud = e.pointcloud;
			let scene = window.viewer.scene;
			let material = pointcloud.material;

            //Add pointcloud to seen
            scene.addPointCloud(pointcloud);

            //Setting for material
            material.size = 1;
            material.pointSizeType = Potree.PointSizeType.ADAPTIVE;

            window.viewer.fitToScreen();
        });
    }
}

</script>
