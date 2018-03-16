<template>
  <section class="container">
     <h4>Kliknij na obrazek by usunać z panelu przesyłania</h4>
    <div>
        <b-alert v-for="alert in errorsAlerts" dismissible show @dismissed="true" variant="danger">{{alert}}</b-alert>
        <b-alert v-for="alert in successAlerts" dismissible show variant="success" @dismissed="true">{{alert}}</b-alert>
        <form @submit.prevent="submitForm" >
          <vueDropzone ref="myVueDropzone" id="myVueDropzone"
          v-on:vdropzone-success="showSuccess"
          v-on:vdropzone-error="showError"
          v-on:vdropzone-sending="sending"
          :options="dropzoneOptions"
          >
          </vueDropzone>
        <div class="form-group">
              <button class="btn btn-primary" type="submit"> Prześlij obrazki </button>
        </div>
        </form>
    </div>
      <loader v-show="isLoading"></loader>
  </section>
</template>

<script type="text/javascript">

import vue2Dropzone from 'vue2-dropzone';
import 'vue2-dropzone/dist/vue2Dropzone.css';

  export default {

    data() {
      return {
        dropzoneOptions: {
                parallelUploads:1,
                url:process.env.BACKEND+'images/',
                myOwnOpt:7676,
                thumbnailWidth: 150,
                maxFilesize: 0.5,
                acceptedFiles:'image/*',
                maxFiles:4,
                dictDefaultMessage: 'Kliknij aby dodać obrazki z komputera, lub przeciągnij je tutaj.',
                addRemoveLinks: true,
                dictFileTooBig:"Zbyt duży plik, max 0.5 MB",
                dictInvalidFileType:"Dozwolone są jedynie obrazki",
                dictRemoveFile:"Usuń",
                dictMaxFilesExceeded:"Nie można dodać więcej niż 4 obrazki",
                uploadMultiple:false,
                autoProcessQueue:false,
                autoQueue:true,
                params: {
                    market_id:this.$route.params.market_id,
                }
            },
        isLoading:false,
        errorsAlerts:[],
        successAlerts:[]
      }
    },
    components: {
      vueDropzone: vue2Dropzone
    },
    methods: {
      'vdropzone-max-files-exceeded':function(file){
          this.$refs.myVueDropzone.removeFile(file)
      },
      'duplicate-file':function(file){
        this.$refs.myVueDropzone.removeFile(file)
      },
      'vdropzone-files-added':function(file){
          this.removeAlerts();
      },
      'sending': function(file, xhr, formData){
        this.isLoading = true;
      },
      'removeAlerts': function(){
        this.errorsAlerts = []
        this.successAlerts = []
      },
      'showSuccess': function (file, message) {
          this.$refs.myVueDropzone.removeFile(file)
          if ('message' in message) {
            this.successAlerts.push(message.message);
          }else{
              console.log(message)
              this.errorsAlerts.push("Nieznany status przesłanych obrazków, skontaktuj się z adminsitratorem");
          }
          this.isLoading = false;
      },
      'showError':function(file, message, xhr){
          this.$refs.myVueDropzone.removeFile(file)
          this.isLoading = false;
          this.parseError(message);
      },
      parseError(message){
                    if (typeof message == "object"){
              if ( typeof message.error == "object" && "market_id" in message.error){
                  this.errorsAlerts.push("Prośba o wysłanie obrazków na nieistniejący market")
              }else {
                this.errorsAlerts.push(message.error)
              }
          }else{
              if(message == "Server responded with 0 code."){
                  this.errorsAlerts.push("Błąd po stronie serwera, skontaktuj się z administratorem.")
              }else {
                this.errorsAlerts.push(message)
              }
          }
      },
      getFilesSendInformation(info){
        this.isLoading = false;
      },

    submitForm(){
      this.removeAlerts();
      this.imagesUrl = process.env.BACKEND+'images/';
      this.$refs.myVueDropzone.setOption('url', this.imagesUrl)
      this.$refs.myVueDropzone.setOption('headers', {"Authorization":  `JWT ${localStorage.getItem('jwtToken')}`})
      if (this.$refs.myVueDropzone.getAcceptedFiles().length>0){
        this.$refs.myVueDropzone.processQueue();
      }else{
        this.isLoading = false;
      }
      },
    },
  }

</script>
