<template>
  <v-app>
    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>

export default {
  name: 'App',

  data: () => ({
    maps: [ // these are place-holders, will need to change them to jsons for the actual thing
      new MapData("Example 1", 0, null, "http://127.0.0.1:5500/Potree/potree-1.8/examples/cesium_ca13.html"),
      new MapData("Example 2", 1, null, "http://127.0.0.1:5500/Potree/potree-1.8/examples/cesium_ca13.html"),
      new MapData("Example 3", 2, null, "http://127.0.0.1:5500/Potree/potree-1.8/examples/cesium_sorvilier.html"),
      new MapData("Example 4", 3, null, null),
      new MapData("Example 5", 4, null, null)
    ],
    currMapIndex: -1
  }),
};
</script>
