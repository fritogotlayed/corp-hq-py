<template>
  <div id="app">
    <!--<img src="./assets/logo.png">-->
    <site-header></site-header>
    <router-view></router-view>
  </div>
</template>

<script>
  import SiteHeader from './components/SiteHeader.vue'
  export default {
    name: 'app',
    components: {
      'site-header': SiteHeader
    }
  }
</script>

<style>
#app {
  /*font-family: 'Avenir', Helvetica, Arial, sans-serif;*/
  /*-webkit-font-smoothing: antialiased;*/
  /*-moz-osx-font-smoothing: grayscale;*/
  /*text-align: center;*/
  /*color: #2c3e50;*/
  /*margin-top: 60px;*/
}
</style>
