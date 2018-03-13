<template>
  <section class="container">
        <h2>Dodaj wydarzenie</h2>
        <h3>2/3</h3>
          <h4>Dodaj obrazki do marketu - maksymalnie 4 po 0.5 MB</h4>
    <add-image></add-image>
              <button class="btn btn-primary" v-on:click="nextPage"><i class="glyphicon glyphicon-ok"></i> Przejdź dalej </button>

  </section>
</template>

<script type="text/javascript">

 import add_image from './add-market-images';

  export default {
    data() {
      return {}
    },
    components: {
        'add-image':add_image,
    },
    methods: {

      'nextPage':function(){
        this.$router.push('/dodaj_wiadomosc/'+this.$route.params.market_id);
      },
    },
  }

</script>
