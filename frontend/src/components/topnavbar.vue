<template>
<div id="topnav" >
  <b-navbar class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top" toggleable="md" type="dark" variant="info">

    <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
    <router-link to="/" v-if="isLogged" >
            <b-navbar-brand >{{name}} masz {{coins}} punktów</b-navbar-brand>
    </router-link>
    <b-collapse is-nav id="nav_collapse">
      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto" v-if="isLogged" >
        <router-link to="/market">
          <li class="nav-item">
            <a class="nav-link">Baza</a>
          </li>
        </router-link>
    <router-link to="/dodaj_market">
      <li class="nav-item">
          <a class="nav-link">Dodaj</a>
      </li>
    </router-link>
    <div v-on:click="logout">
       <li class="nav-item">
              <a class="nav-link">Wyloguj</a>
          </li></div>
      </b-navbar-nav>
           <b-navbar-nav class="ml-auto" v-else>
        <router-link to="/login">
          <li class="nav-item">
            <a class="nav-link">Logowanie</a>
          </li>
        </router-link>
           </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</div>
</template>

<script>
  import EventBus from '../event-bus';
export default {

created(){
        EventBus.$on('logged', this.checkIfIsLogged );

  this.getNgoName();
  this.getCoins();
},
  beforeDestroy(){
     EventBus.$off('logged');
  },
  mounted(){
         this.isLogged = this.checkIfIsLogged();
  },
data() {
  return {
    coins:0,
    name:'',
    isLogged: this.checkIfIsLogged(),
}
},
watch:{
    '$route' (to, from){
        this.getCoins();
        this.getNgoName();
    }
},
components: {

},

methods:{
  logout: function() {
    localStorage.removeItem('jwtToken');
    this.isLogged = false;
     this.$router.push('/');
 },
 getNgoName: function(){
   this.name = localStorage.getItem('ngo_name');
 },
 getCoins: function(){
   this.coins = localStorage.getItem('coins') | 0;
 },

  checkIfIsLogged: function(){
   if (localStorage.getItem('jwtToken') == null){
     this.isLogged = false;
   }else{
       this.isLogged = true;

   }
 },

}}

</script>

<style scoped>
.navbar-brand{
  white-space:normal;
}
</style>
