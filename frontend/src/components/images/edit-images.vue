<template>
  <section class="container edit-images-panel">
    <h4>Kliknij na obrazek by usunać</h4>
          <b-alert  :show="isError" variant="danger">{{error}}</b-alert>
        <b-alert  :show="isSuccess" variant="success">{{success}}</b-alert>
        <b-container fluid class="p-4 bg-white">
          <b-row >
            <b-col md="3" class="py-4 text-center" v-for="image in images">
              <b-img :id="'exPopover1-'+image.id"
               thumbnail fluid :src="backendUrl+image.image_path"
               alt="Thumbnail" class="img-thumbnail" width="175" height="175"/>
              <b-popover :target="'exPopover1-'+image.id"
                  triggers="click"
                  :content="'exPopover1-'+image.id">
                <b-btn @click="onClose(image.id)" size="sm" variant="danger">Usuń</b-btn>
              </b-popover>
            </b-col>
          </b-row>
    </b-container>
      <loader v-show="isLoading"></loader>
  </section>
</template>

<script type="text/javascript">

  import axios from 'axios';
  export default {
    created(){
    this.getImages()
  },
    data() {
      return {
        images :[],
        isLoading:false,
        isError:false,
        error:"",
        success:"",
        isSuccess:false,
        backendUrl : process.env.BACKEND.slice(0,21)
      }
    },
    methods: {
        getImages(){
          const market_id = this.$route.params.market_id;
          axios.defaults.headers.common['Authorization'] = `JWT ${localStorage.getItem('jwtToken')}`;
          axios.get(process.env.BACKEND+"images/?market_id="+market_id,)
          .then(response => {
            this.isError = false;
            this.isLoading = false;
            this.images = response["data"]
          })
          .catch(error => {
            this.isError = true;
            this.isLoading = false;
            this.error = error.response.data.error
            console.log(e)
      })
        },
      onClose(imageId){
      axios.defaults.headers.common['Authorization'] = `JWT ${localStorage.getItem('jwtToken')}`;
      axios.delete(process.env.BACKEND+"images/"+imageId+"/",)
      .then(response => {

        const arrayLength = this.images.length;
        for (let index = 0; index < arrayLength; index++) {
            if (this.images[index].id == imageId){
                console.log(imageId)
              console.log(this.images[index].id)
                this.images.splice(index, 1)
                break
            }
        }
      })
      .catch(e => {
        this.isLoading = false;
      })

      }
    },
  }

</script>
<style>
    .container{
    font-family: "Century Gothic", CenturyGothic, AppleGothic, sans-serif;

  }
  .edit-images-panel{
       margin-top: 1px !important;
  }
</style>
