<template>
<div id="edit-panel" style="margin-top: 90px;">
    <h2>Panel edycji</h2>
    <router-link :to="{path: basic_edit}" > <b-btn style="background-color: rgb(90, 128, 204);" block variant="info" size="lg">Edytuj bazowe dane</b-btn> </router-link>
      <h2></h2>
    <router-link :to="{path: image_edit}" > <b-btn style="background-color: rgb(90, 128, 204);" block variant="info" size="lg">Edytuj obrazki</b-btn> </router-link>
        <h2></h2>
  <router-link :to="{path: messages_services_edit}" > <b-btn style="background-color: rgb(90, 128, 204);" block variant="info" size="lg">Edytuj wiadomości</b-btn> </router-link>
</div>
</template>

<script>
  export default {
data() {
  return {
    basic_edit:"/edytuj_market/"+this.$route.params.market_id,
    image_edit:"/edytuj_obrazki/"+this.$route.params.market_id,
    messages_services_edit:"/edytuj_wiadomosci/"+this.$route.params.market_id,
  }
}}
</script>

<style>
  h2,h3,h4{
  font-family: "Century Gothic", CenturyGothic, AppleGothic, sans-serif;
}

  .edit-panel {
    margin-top: 100px;
  }
</style>
