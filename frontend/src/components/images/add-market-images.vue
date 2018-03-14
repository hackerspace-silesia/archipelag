<template>
  <section class="container">
     <h4>Kliknij na obrazek by usunać z panelu przesyłania</h4>
    <div>
      <b-alert  :show="isError" variant="danger">{{error}}</b-alert>
        <b-alert  :show="isSuccess" variant="success">{{success}}</b-alert>
        <form @submit.prevent="submitForm" >
          <vueDropzone ref="myVueDropzone" id="myVueDropzone"
          v-on:vdropzone-success="showSuccess"
          v-on:vdropzone-error="showError"
          v-on:vdropzone-sending="sending"
          :options="dropzoneOptions"
          >
          </vueDropzone>
      <div class="form-group">
            <button class="btn btn-primary" type="submit"><i class="glyphicon glyphicon-ok"></i> Prześlij obrazki </button>
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
                dictInvalidFileType:"Zły typ",
                dictRemoveFile:"Usuń",
                dictMaxFilesExceeded:"Za dużo plików, max 4",
                uploadMultiple:false,
                autoProcessQueue:false,
                autoQueue:true,
                params: {
                    market_id:this.$route.params.market_id,
                }
            },
        isLoading:false,
        isError:false,
        error:"",
        formSubmitted:false,
        success:"",
        isSuccess:false,
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
          this.isError = false;
          this.isSuccess = false;
      },

      'sending': function(file, xhr, formData){
        console.log(file);
        this.isLoading = true;
      },
      'showSuccess': function (file, message) {
          this.isError = false
          this.isSuccess = true;
          if ('message' in message) {
            this.success = message.message;
          }else{
            this.success = "Nieznany status przesłanych obrazków, skontaktuj się z adminsitratorem"
          }
          this.formSubmitted = true;
          this.isLoading = false;
      },
      'showError':function(file, message, xhr){
          console.log(message)
          this.$refs.myVueDropzone.removeFile(file)
          this.isLoading = false;
          this.isError = true;
          this.isSuccess = false;
          if (typeof message == "object"){
              if ( typeof message.error == "object" && "market_id" in message.error){
                   this.error = "Prośba o wysłanie obrazków na nieistniejący market";
              }
              this.error = message.error;
          }else{
              if(message == "Server responded with 0 code."){
                  this.error = "Błąd po stronie serwera, skontaktuj się z administratorem."
              }else {
                this.error = message;
              }
          }

      },
      getFilesSendInformation(info){
        this.isSubmitted = true;
        this.isLoading = false;
      },

    submitForm(){
      this.imagesUrl = process.env.BACKEND+'images/';
      this.$refs.myVueDropzone.setOption('url', this.imagesUrl)
      this.$refs.myVueDropzone.setOption('headers', {"Authorization":  `JWT ${localStorage.getItem('jwtToken')}`})
      if (this.$refs.myVueDropzone.getAcceptedFiles().length>0){
        this.$refs.myVueDropzone.processQueue();
      }else{
        this.isSubmitted = true;
        this.isLoading = false;
      }
      },
    },
  }

</script>
