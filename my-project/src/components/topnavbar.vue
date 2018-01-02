<template>
<div id="topnav">
  <b-navbar toggleable="md" type="dark" variant="info">

    <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>

    <b-navbar-brand href="#">masz 0 punktów</b-navbar-brand>

    <b-collapse is-nav id="nav_collapse">

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
    <router-link to="/market"><b-button >Targ</b-button></router-link>
    <router-link to="/dodaj_market"> <b-button >Dodaj</b-button></router-link>
    <router-link to="/wyloguj"> <b-button >Wyloguj</b-button></router-link>
      </b-navbar-nav>

    </b-collapse>
  </b-navbar>
</div>
</template>

<style scoped>
    button {
        background-color:#ffdb93;
        color:black;
    }
</style>
