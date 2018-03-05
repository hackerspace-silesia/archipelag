<template>
<div id="edit-panel">
    <h2>Panel edycji</h2>
    <router-link :to="{path: basic_edit}"> <b-btn block variant="info" size="lg">Edytuj bazowe dane</b-btn> </router-link>
      <h2></h2>
    <router-link :to="{path: basic_edit}"> <b-btn block variant="info" size="lg">Edytuj obrazki</b-btn> </router-link>
        <h2></h2>
  <router-link :to="{path: messages_services_edit}"> <b-btn block variant="info" size="lg">Edytuj wiadomości</b-btn> </router-link>
</div>
</template>

<script>
  export default {
data() {
  return {
    basic_edit:"/edytuj_market/"+this.$route.params.market_id,
    image_edit:"/edytuj_wiadomosci/"+this.$route.params.market_id,
    messages_services_edit:"/edytuj_wiadomosci/"+this.$route.params.market_id,
  }
}}
</script>
