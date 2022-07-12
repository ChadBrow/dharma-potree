const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  alias: {
    'src': path.resolve(__dirname, '../src')
  },
  transpileDependencies: [
    'vuetify'
  ]
})
