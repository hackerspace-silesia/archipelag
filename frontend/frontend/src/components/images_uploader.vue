<template>
  <div id="app">
    <p>Welcome to your Vue.js app!</p>

    <vueDropzone ref="myVueDropzone" id="myVueDropzone" v-on:vdropzone-success="showSuccess" v-on:vdropzone-error="showError" v-on:vdropzone-sending="sending" :options="dropzoneOptions">

    </vueDropzone>

  </div>
</template>

<script>
  import vue2Dropzone from 'vue2-dropzone';
  import 'vue2-dropzone/dist/vue2Dropzone.css';
  export default {
    props: ['myUrl'],
    data(){
    return {
dropzoneOptions: {
        url:this.myUrl,
        thumbnailWidth: 150,
        maxFilesize: 0.5,
        headers: { "My-Awesome-Header": "header value" },
        acceptedFiles:'image/*',
        maxFiles:4,
        dictDefaultMessage: 'Kliknij aby dodać obrazki z komputera, lub przeciągnij je tutaj.',
        addRemoveLinks: true,
        dictFileTooBig:"Zbyt duży",
        dictInvalidFileType:"Zły typ",
        dictRemoveFile:"Usuń",
        dictMaxFilesExceeded:"Za dużo plików",
        uploadMultiple:false,
        autoProcessQueue:false,

    }}
    },
    components: {
      vueDropzone: vue2Dropzone
    },
    methods: {
      getUploader(){
        return this.$refs.myVueDropzone;
      },
      'sending': function(file, xhr, formData){
          console.log(this.$refs.myVueDropzone.processQueue())

        console.log(file);
        console.log("jjj")
      },
      'showSuccess': function (file) {
        this.$emit("uploadInformation", { success: file });
        console.log('A file was successfully uploaded')
      },
      'showError':function(file, message, xhr){
            this.$emit("uploadInformation", { error: file });
        console.log('Błąd')
        console.log(message);
      }

  }}
</script>
