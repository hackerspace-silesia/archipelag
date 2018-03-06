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
          {{service.service}}
        </b-btn>
      </b-card-header>
      <b-collapse v-bind:id="service.service" accordion="my-accordion" role="tabpanel">
                  <!--<button v-show="service.id"-->
                          <!--v-on:click="deleteMsg(service.msg_id)"-->
                          <!--type="button" class="close .btn-warning" id="x" >usuń</button>-->
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
      axios.defaults.headers.common['Authorization'] = `JWT ${localStorage.getItem('jwtToken')}`;
      axios.all([
          axios.get(process.env.BACKEND+`messages_types/`),
          axios.get(process.env.BACKEND+"message/?market_id="+this.$route.params.market_id)
        ])
        .then(axios.spread((types, marketMsg) => {
            console.log(types.data)
          this.types = this.getProperMessage(types.data, marketMsg.data)
          console.log(this.types)
        })).catch((err) => {
           console.log(err)
      });
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
        deleteMsg(id){
             axios.defaults.headers.common['Authorization'] = `JWT ${localStorage.getItem('jwtToken')}`;
              axios.delete(process.env.BACKEND+`message/`+id+"/")
              .then(response => {
                this.isLoading=false;
                console.log(response)
                if ('message' in response['data']){
                  this.showDismissibleSuccess = true;
                    this.showDismissibleAlertError = false;
                    this.info = "Usunięto wiadomość"
                }else{
                    console.log("yolo")
                  this.showDismissibleAlertError = true;
                  this.showDismissibleSuccess = false;
                    this.error = response.data['detail'];
                }

              })
              .catch(e => {
                   console.log(JSON.parse(err.error))
                  if (e.response.status==404) {
                    this.isLoading = false;
                    this.showDismissibleAlertError = true;
                    this.showDismissibleSuccess = false;
                    this.error = "Nie znaleziono wiadomości do usunięcia";
                  }
                console.log(e.response.status)
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
#x {
    position: absolute;
    background: darkslateblue;
    color: white;
    top: -5px;
    right: 5%;
  padding: 15px;
  opacity: 100;
  border-radius: 35%;
}
</style>
