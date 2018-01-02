<template>
  <div id="app">
    <topnavbar />
    <router-view/>
  </div>
</template>

<script>
import topnavbar from '@/components/topnavbar.vue'
export default {
  name: 'app',
  components:{
    topnavbar
    }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 0px;
}
</style>
