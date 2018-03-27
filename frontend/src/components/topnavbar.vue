<template>
<div id="topnav" >
  <b-navbar class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top" toggleable="md" type="dark" variant="info">

    <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

    <b-navbar-brand href="#">{{name}} masz {{coins}} punktów</b-navbar-brand>

    <b-collapse is-nav id="nav_collapse">

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <router-link to="/market">
          <li class="nav-item">
            <a class="nav-link" href="#">Targ</a>
          </li>
        </router-link>
    <router-link to="/dodaj_market">
      <li class="nav-item">
          <a class="nav-link" href="#">Dodaj</a>
      </li>
    </router-link>
    <div v-on:click="logout">
       <li class="nav-item">
              <a class="nav-link" href="#">Wyloguj</a>
          </li></div>
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

</style>
