<template>
  <section class="container">
    <h2>Edytuj dodane obrazki</h2>
      <loader v-show="isLoading"></loader>
  </section>
</template>

<script type="text/javascript">

  import axios from 'axios';
  export default {
    created(){
      const market_id = this.$route.params.market_id;
      axios.defaults.headers.common['Authorization'] = `JWT ${localStorage.getItem('jwtToken')}`;
      axios.get(process.env.BACKEND+"images/?market_id="+market_id,)
      .then(response => {
        this.isLoading = false;
        if ('error' in response){
          this.showDismissibleAlertError = true;
          this.error = response['error'];
          this.isLoading = false;
        }
        else{
          console.log(response)
          }
      })
      .catch(e => {
        this.showDismissibleAlertError = true;
        this.isLoading = false;
        this.error = "Prośba o edycję nieistniejącego marketu."
        console.log(e)
      })

  },
    data() {
      return {
        isLoading:false,
        isError:false,
        error:"",
        formSubmitted:false,
        success:"",
        isSuccess:false,
      }
    },
    methods: {

    },
  }

</script>
