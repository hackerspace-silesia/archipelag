<template>
<div id="topnav">
  <b-navbar toggleable="md" type="dark" variant="info">

    <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

    <b-navbar-brand href="#">{{name}} masz {{coins}} punktów</b-navbar-brand>

    <b-collapse is-nav id="nav_collapse">

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
    <router-link to="/market"><b-button class="col-12">Targ</b-button></router-link>
    <router-link to="/dodaj_market"> <b-button class="col-12">Dodaj</b-button></router-link>
    <b-button v-on:click="logout">Wyloguj</b-button>
      </b-navbar-nav>

    </b-collapse>
  </b-navbar>
</div>
</template>

<script>
  import axios from 'axios';
export default {
created(){

  this.getNgoName();
  this.getCoins();
},
data() {
  return {
    coins:0,
    name:'',
}
},
watch:{
    '$route' (to, from){
        this.getCoins();
    }
},
components: {

},
methods:{
  logout: function() {
    localStorage.setItem('jwtToken', '');
    this.$router.push('/login');
 },
 getNgoName: function(){
   this.name = localStorage.getItem('ngo_name');
 },
 getCoins: function(){
   this.coins = localStorage.getItem('coins');
 },

}}

</script>

<style scoped>
    button {
        background-color:#ffdb93;
        color:black;
    }
</style>
