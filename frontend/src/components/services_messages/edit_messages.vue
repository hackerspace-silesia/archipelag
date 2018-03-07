<template>
  <div role="tablist">
    <hr>
    <h2>Edytuj wiadomości</h2>
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
        <b-btn block v-b-toggle="service.service" v-on:click="closeInformations"
               v-b-toggle.service.service variant="info" size="lg">
                {{ service.content ? 'Edytuj' : 'Dodaj' }}
                  {{service.service}}

        </b-btn>
      </b-card-header>
      <b-collapse v-bind:id="service.service" accordion="my-accordion" role="tabpanel">
                  <button v-show="service.content"
                          v-on:click="deleteMsg(service.msg_id)"
                          type="button" class="close .btn-warning" id="x" >usuń</button>
          <text-area-counter v-bind:service="service" v-bind:getFormValues="getFormValues"></text-area-counter>
      </b-collapse>
    </b-card>
              <router-link :to="{path: pathToEditPanel}"> <button class="btn btn-primary" ><i class="glyphicon glyphicon-ok"></i>Wróć do panelu edycji </button></router-link>

        <loader v-show="isLoading"></loader>
  </div>
</template>

<script type="text/javascript">
  import axios from 'axios';
 import textAreaCounter from './text-area-with-counter';
  export default {
    name:'EditMessages',
    created(){
      this.setMessagesTypesAndEditableCreated();
      },
    data() {
      return {
        pathToEditPanel: "/panel_edycji/"+this.$route.params.market_id,
        isLoading:false,
        types:[],
        messageToEdit:{},
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
      setMessagesTypesAndEditableCreated(){
        axios.defaults.headers.common['Authorization'] = `JWT ${localStorage.getItem('jwtToken')}`;
        axios.all([
            axios.get(process.env.BACKEND+`messages_types/`),
            axios.get(process.env.BACKEND+"message/?market_id="+this.$route.params.market_id)
          ])
          .then(axios.spread((types, marketMsg) => {
            this.types = this.getProperMessage(types.data, marketMsg.data)
          })).catch((err) => {
             console.log(err)
        });
      },
        deleteMsg(id){
             axios.defaults.headers.common['Authorization'] = `JWT ${localStorage.getItem('jwtToken')}`;
              axios.delete(process.env.BACKEND+`message/`+id+"/")
              .then(response => {
                this.isLoading=false;
                if ( response.status == 204){
                    this.showDismissibleSuccess = true;
                    this.showDismissibleAlertError = false;
                    this.info = "Usunięto wiadomość"
                    this.setMessagesTypesAndEditableCreated();
                }else{
                    console.log("yolo")
                  this.showDismissibleAlertError = true;
                  this.showDismissibleSuccess = false;
                    this.error = response.data['detail'];
                }

              })
              .catch(e => {
                   console.log(e)
                  if (e.response.status==404) {
                    this.isLoading = false;
                    this.showDismissibleAlertError = true;
                    this.showDismissibleSuccess = false;
                    this.error = "Nie znaleziono wiadomości do usunięcia";
                  }
              })
        },
        getProperMessage(types, msg){
            const numberOfMessages = msg.length;
            const numberOfTypes = types.length;
            for (let typesIndex = 0; typesIndex < numberOfTypes; ++typesIndex) {
               for (let msgIndex = 0; msgIndex < numberOfMessages; ++msgIndex) {
                   if (msg[msgIndex]["type"] === types[typesIndex]["service"]) {
                       console.log(types[typesIndex])
                       types[typesIndex]["content"]= msg[msgIndex]["content"]
                       types[typesIndex]["msg_id"]= msg[msgIndex]["id"]
                   }
                 }
                }
          return types;
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
                    this.info = response.data.message;
                    this.setMessagesTypesAndEditableCreated();
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
#x {
  position: absolute;
    background: red;
    color: white;
    top: 6px;
    right: 4%;
    padding: 10px;
    opacity: 100;
    width: 90px;
}
</style>
