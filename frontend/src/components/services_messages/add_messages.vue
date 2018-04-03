<template>
  <div role="tablist">
    <hr>
    <h2>Dodaj wydarzenie</h2>
        <h3>3/3</h3>
    <h4>Wybierz serwis na który ma być udostępniona wiadomość</h4>
    <h5>Rozwijając każdą opcję, zobaczysz wskazówki odnośnie formy udostępnianej treści.
Polecamy trzymać się tych zasad – lepiej skonstruowane komunikaty są bardziej popularne.
Jeśli masz więcej wątpliwości, sięgnij do naszego poradnika,
który znajduje się na stronie głównej #archipelagu.</h5>
    <hr>
    <b-alert variant="success"
       dismissible
       :show="showDismissibleSuccess"
       @dismissed="showDismissibleSuccess=false"
       >
    {{info}}
    </b-alert>
    <b-alert variant="danger"
       dismissible
       :show="showDismissibleAlertError"
       @dismissed="showDismissibleAlertError=false"
       >
    {{error}}
    </b-alert>
    <b-card no-body class="mb-1" v-for="service in types">
      <b-card-header header-tag="header" class="p-1" role="tab">
        <b-btn style="background-color: rgb(90, 128, 204);"  block v-b-toggle="service.service" v-on:click="closeInformations" v-b-toggle.service.service variant="info" size="lg">{{service.service}}</b-btn>
      </b-card-header>
      <b-collapse v-bind:id="service.service" accordion="my-accordion" role="tabpanel">
          <text-area-counter v-bind:service="service" v-bind:getFormValues="getFormValues"></text-area-counter>
      </b-collapse>
    </b-card>
        <loader v-show="isLoading"></loader>
  </div>
</template>

<script type="text/javascript">
  import axios from 'axios';
 import textAreaCounter from './text-area-with-counter';
  export default {
    name:'AddMessages',

    created(){
       axios.defaults.headers.common['Authorization'] = `JWT ${localStorage.getItem('jwtToken')}`;
      axios.get(process.env.BACKEND+`messages_types/`)
      .then(response => {
        this.types = response.data;
      })
      .catch(e => {
        console.log(e)
      })

      },
    data() {
      return {
        isLoading:false,
        types:[],
        showDismissibleSuccess: false,
        showDismissibleAlertError: false,
        info:'',
        error:'',
      }
    },
    components: {
      'axios':axios,
      'text-area-counter':textAreaCounter,
    },
    methods: {
      getCharNumber(content){
        return content.length
      },
      closeInformations(){
        this.showDismissibleSuccess = false;
        this.showDismissibleAlertError = false;
      },
      getFormValues(message, type_id, restriction){
        if (message.length <= 0){
          this.showDismissibleSuccess = false;
          this.showDismissibleAlertError = true;
          this.error = "Wiadomosć nie może być pusta";
        }
        else if (message.length>restriction) {
          let distinction = message.length - restriction;
          this.showDismissibleSuccess = false;
          this.showDismissibleAlertError = true;
          this.error = "Przekroczono maksymalną ilość znaków o "+distinction;
        }
        else{
        const form={
          content:message,
          type:type_id,
          market:this.$route.params.market_id,
        };
        this.isLoading=true;
        axios.defaults.headers.common['Authorization'] = `JWT ${localStorage.getItem('jwtToken')}`;
              axios.post(process.env.BACKEND+`message/`, {
                body: form
              })
              .then(response => {
                this.isLoading=false;
                console.log(response)
                if ('message' in response['data']){
                  this.showDismissibleSuccess = true;
                    this.showDismissibleAlertError = false;
                    this.info = response.data.message
                }else{
                  this.showDismissibleAlertError = true;
                  this.showDismissibleSuccess = false;
                    this.error = response.data['error'];
                }

              })
              .catch(e => {
                this.isLoading=false;
                console.log(e)
              })
            }
          }
        },
}
</script>
<style>
h2,h4{
  font-family: "Century Gothic", CenturyGothic, AppleGothic, sans-serif;
}
</style>
