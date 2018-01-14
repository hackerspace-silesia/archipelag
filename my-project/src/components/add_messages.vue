<template>
  <div role="tablist">
    <hr>
    <h2>Dodaj wydarzenie</h2>
        <h3>1/2</h3>
    <h4>Wybierz serwis na który ma być udostępniona wiadomość</h4>
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
                             :rows="3"
                             :maxlength="service.char_restriction"
                             required></textarea>
                             <p class='text-right text-small'>max liczba znaków {{service.char_restriction}}</p>
            <button class="btn btn-primary" type="submit" @click.prevent="getFormValues(service.id)"><i class="glyphicon glyphicon-ok"></i> Zapisz </button>

</b-form-group>
        </form>

      </b-collapse>
    </b-card>
        <loader v-show="isLoading"></loader>
  </div>
</template>

<script type="text/javascript">
  import axios from 'axios';

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
      getFormValues(type_id){
        const form={
          content:this.$refs[type_id][0].value,
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
                if ('success' in response['data']){
                  this.showDismissibleAlert = true;
                    this.info = "Dodano wiadomość do udostępniania.";
                }else{
                  this.showDismissibleAlertError = true;
                    this.error = response.data['error'];
                }

              })
              .catch(e => {
                this.isLoading=false;
                console.log(e)
              })
            }
        },
}
</script>
<style>

</style>
