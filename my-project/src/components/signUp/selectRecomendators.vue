<template>
<div id="selectNGO">
  <b-form-group
        label="Wybierz NGO, które poleciło Archipelag:"
        label-for="exampleInput3">
          <b-form-select id="exampleInput3"
                        :options="ngos"
                        v-model="ngo"
                        @change="onSelectRecomendators">
          </b-form-select>

    </b-form-group>
  </div>

</template>

<script type="text/javascript">
  import axios from 'axios';
  export default {
    props:['onSelectRecomendators'],
    created(){

      this.get_all_ngos();
  },

    data() {
      return{
        isValid:false,
        error:"",
        ngos: [
          { text: 'Wybierz jeden', value: null },
        ],
        ngo:null,
    }
    },
    components: {
      axios,
    },
    methods: {
      showErrorMessage(msg){
        this.error = msg;
        this.isValid = false;

      },
      get_all_ngos() {
        this.isLoading = true;
        axios.get(process.env.BACKEND+"ngo/")

       .then(response =>{
       // JSON responses are automatically parsed.
       let i = 0
       const ngosLenght = response.data.length;
       for (i ; i < ngosLenght; i++) {
         let id = response.data[i].id;
         let name = response.data[i].organisation;
            this.ngos.push(name);
        }

       }).
         catch(e => {
           this.error = e
         console.log(e);
       })
       },

  }
  }
</script>
