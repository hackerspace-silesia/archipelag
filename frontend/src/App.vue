<template>
  <div id="app">
    <topnavbar v-show="$route.path==='/login' | $route.path==='/signUp' ? false : true"/>
    {{ready()}}
    <router-view/>
  </div>
</template>

<script>
import topnavbar from '@/components/topnavbar.vue'

export default {
  name: 'app',
  components:{
    topnavbar,

  },

methods:{
  ready : function (){
       console.log(this.$route.path);
   }
}
}
</script>

<style>
#app {

  font-family: 'Segoe UI', Helvetica, Arial, sans-serif !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 40px;
}
    h2,h3,h4{
  font-family: "Century Gothic", CenturyGothic, AppleGothic, sans-serif;
}
</style>
