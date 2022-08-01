import * as THREE from "../../three.js/build/three.module.js";

export class annotationChild {
    constructor (name, type, location, data) {
        this.name = name || "default";
        this.type = type || "default";
        this.location = location || new THREE.Vector3();
        this.symbol = null; // this should be an image that we load... right?

        this.data = data || "sorry, not available"; // ok, we need to decide on a data loading method so the site is not super slow

        this.domElement = $(

        ); // I dont know, I hate HTML

        // this class needs to be completed, but this is the basics




    };
}