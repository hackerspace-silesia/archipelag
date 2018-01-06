<template>
  <div role="tablist">
    <hr>
    <h2>Wybierz serwis na który ma być udostępniona wiadomość</h2>
    <hr>
    <b-alert variant="success"
       dismissible
       :show="showDismissibleAlert"
       @dismissed="showDismissibleAlert=false"
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
        <b-btn block v-b-toggle="service.service"  v-b-toggle.service.service variant="info" size="lg">{{service.service}}</b-btn>
      </b-card-header>
      <b-collapse v-bind:id="service.service" accordion="my-accordion" role="tabpanel">
          <form >
<b-form-group class="col-md-12 center">
            <textarea class="col-md-12 center" id="textarea2"
                             state="invalid"
                             :ref="service.id"
                             placeholder="Wpisz wiadomość"
                             :rows="3"></textarea>
            <button class="btn btn-primary" @click.prevent="getFormValues(service.id)"><i class="glyphicon glyphicon-ok"></i> Zapisz </button>
</b-form-group>
        </form>

      </b-collapse>
    </b-card>
  </div>
</template>

<script type="text/javascript">
  import axios from 'axios';

  export default {
    name:'AddMessages',
    created(){
       axios.defaults.headers.common['Authorization'] = `JWT ${localStorage.getItem('jwtToken')}`;
      axios.get(`http://127.0.0.1:8000/messages_types/`)
      .then(response => {
        this.types = response.data;
      })
      .catch(e => {
        console.log(e)
      })

      },
    data() {
      return {
        types:[],
        showDismissibleAlert: false,
        showDismissibleAlertError: false,
        info:'',
        error:'',
      }
    },
    components: {
      axios
    },
    methods: {
      submitForm(){

      },
      getFormValues(type_id){
        const form={
          content:this.$refs[type_id][0].value,
          type:type_id,
          market:this.$route.params.market_id,
        };
        axios.defaults.headers.common['Authorization'] = `JWT ${localStorage.getItem('jwtToken')}`;
              axios.post(`http://127.0.0.1:8000/message/`, {
                body: form
              })
              .then(response => {
                console.log(response)
                if ('success' in response['data']){
                  this.showDismissibleAlert = true;
                    this.info = "Dodano wiadomość do udostępniania.";
                }else{
                  this.showDismissibleAlertError = true;
                    this.error = response.data['error'];
                }

              })
              .catch(e => {
                console.log(e)
              })
            }
        },
}
</script>
<style>

</style>
