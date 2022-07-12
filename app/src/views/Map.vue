<template>
    <div class="potree_container" style="position: absolute; width: 100%; height: 100%; left: 0px; top: 0px; ">
		<div id="potree_render_area" style="background-image: url('../build/potree/resources/images/background.jpg');"></div>
		<div id="potree_sidebar_container"> </div>
	</div>
</template>

<style>
    import THREE from 'three';
	
    window.viewer = new Potree.Viewer(document.getElementById("potree_render_area"));
    
    viewer.setEDLEnabled(true);
    viewer.setFOV(60);
    viewer.setPointBudget(1_000_000);
    viewer.loadSettingsFromURL();
    
    viewer.setDescription("");
    
    viewer.loadGUI(() => {
        viewer.setLanguage('en');
        $("#menu_appearance").next().show();
        //viewer.toggleSidebar();
    });
    
    // Lion
    Potree.loadPointCloud("../pointclouds/lion_takanawa/cloud.js", "lion", function(e){
        viewer.scene.addPointCloud(e.pointcloud);
        
        let material = e.pointcloud.material;
        material.size = 1;
        material.pointSizeType = Potree.PointSizeType.ADAPTIVE;
        
        viewer.fitToScreen();
    });
</style>
