<template>
    <v-container class="potree_container" style="position: absolute; width: 100%; height: 100%; left: 0px; top: 0px; ">
		<div id="potree_render_area" style="background-image: '../build/potree/resources/images/background.jpg';"></div>
	</v-container>
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

        // //Initialize Potree viewer
        // window.viewer = new Potree.Viewer(document.getElementById("potree_render_area"));

        // //Configure viewer settings
        // window.viewer.setEDLEnabled(true);
        // window.viewer.setFOV(60);
        // window.viewer.setPointBudget(1_000_000);
        // window.viewer.loadSettingsFromURL();

        // window.viewer.setDescription("");

        // window.viewer.loadGUI(() => {
        // window.viewer.setLanguage('en');
        // window.$("#menu_appearance").next().show();
        //     //viewer.toggleSidebar();   
        // });

        // // Load pointcloud
        // Potree.loadPointCloud("./assets/pointclouds/lion_takanawa/cloud.js", "lion", function(e){
        //     viewer.scene.addPointCloud(e.pointcloud);

        //     let material = e.pointcloud.material;
        //     material.size = 1;
        //     material.pointSizeType = Potree.PointSizeType.ADAPTIVE;

        //     window.viewer.fitToScreen();
        // });
    }
}

</script>
