<template>
    <div class="potree_container" style="position: absolute; width: 100%; height: 100%; left: 0px; top: 0px; ">
		<div id="potree_render_area" style="background-image: url('../build/potree/resources/images/background.jpg');"></div>
		<div id="potree_sidebar_container"> </div>
	</div>
</template>

<script>   
    //import libraries
    import THREE from 'three';
    import * as Potree from '../potree/Potree.js'

    //Initialize Potree viewer
    window.viewer = new Potree.Viewer(document.getElementById("potree_render_area"));

    //Configure viewer settings
    window.viewer.setEDLEnabled(true);
    window.viewer.setFOV(60);
    window.viewer.setPointBudget(1_000_000);
    window.viewer.loadSettingsFromURL();

    window.viewer.setDescription("");

    window.viewer.loadGUI(() => {
    window.viewer.setLanguage('en');
    window.$("#menu_appearance").next().show();
        //viewer.toggleSidebar();   
    });

    // Load pointcloud
    Potree.loadPointCloud("../renderingData/pointclouds/lion_takanawa/cloud.js", "lion", function(e){
        viewer.scene.addPointCloud(e.pointcloud);

        let material = e.pointcloud.material;
        material.size = 1;
        material.pointSizeType = Potree.PointSizeType.ADAPTIVE;

        window.viewer.fitToScreen();
    });
</script>
