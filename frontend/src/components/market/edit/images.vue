<template>
  <section class="container">
    <h2>Edytuj dodane obrazki</h2>
        <b-container fluid class="p-4 bg-white">
          <b-row >
            <b-col md="3" class="py-4 text-center" v-for="image in images">
              <b-img :id="'exPopover1-'+image.id"
               thumbnail fluid :src="backendUrl+image.image_path"
               alt="Thumbnail" class="img-thumbnail" width="175" height="175"/>
              <b-popover :target="'exPopover1-'+image.id"
                  title="Prop Examples"
                  triggers="hover focus"
                  :content="'exPopover1-'+image.id">
              </b-popover>
            </b-col>
          </b-row>
        <div class="clearfix">
            <div v-for="image in images" class="clearfix">

               <b-popover target="image-with-popover" title="Popover">
                 Hello <strong>World!</strong>
              </b-popover>
            </div>
          </div>
    </b-container>
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
            this.images = response["data"]
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
        images :[],
        isLoading:false,
        isError:false,
        error:"",
        formSubmitted:false,
        success:"",
        isSuccess:false,
        backendUrl : process.env.BACKEND.slice(0,21)
      }
    },
    methods: {

    },
  }

</script>
