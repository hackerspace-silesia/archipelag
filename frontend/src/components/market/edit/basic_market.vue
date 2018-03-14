<template>
  <section class="container">
    <b-alert variant="danger"
       dismissible
       :show="showDismissibleAlertError"
       @dismissed="showDismissibleAlertError=false"
       >
    {{error}}
    </b-alert>
    <b-alert variant="success"
       dismissible
       :show="showDismissibleSuccess"
       @dismissed="showDismissibleSuccess=false"
       >
    Dane przesłano poprawnie
    </b-alert>
    <div class="row">
      <div class="col-md-3 center" >
      </div>
      <div class="col-md-6 center" >

    <b-card bg-variant="light">
        <h2>Edytuj dane</h2>
        <hr>
        <form @submit.prevent="submitForm">
          <div class="row">
            <div class="col-md-12 text-center" >
              <b-form-group
                  label="Tytuł"
                  label-for="title"
                  :invalid-feedback="invalidFeedback">
              <b-form-input
                  id="title"
                  type="text"
                  :state="state"
                  v-model="form.title">
                </b-form-input>
              </b-form-group>
                <b-form-group vertical
                    label="Hashtag:"
                    label-class="text-sm-right"
                    label-for="hashtag">
                    <b-form-input v-model="form.hashtag" id="hashtag"></b-form-input>
                  </b-form-group>
              <div class="form-group">
                <label>Rozpoczęcie: </label>

                <date-picker v-model="form.date_starting" :config="configs.start" ref="date_starting"
                             @dp-change="onStartChange"> </date-picker>
              </div>
            </div>
            <div class="col-md-12 text-center">
              <div class="form-group">
                <label>Zakończenie: </label>
                <date-picker v-model="form.date_ending" :config="configs.end" ref="date_ending"
                             @dp-change="onEndChange" ></date-picker>
              </div>
            </div>
          </div>
          <hr>
          <div class="form-group">
            <button class="btn btn-primary" type="submit"><i class="glyphicon glyphicon-ok"></i> Zapisz </button>
          </div>

        </form>
          <router-link :to="{path: pathToEditPanel}"> <button class="btn btn-primary" ><i class="glyphicon glyphicon-ok"></i>Wróć do panelu edycji </button></router-link>
        </b-card>
      </div>
      <div class="col-md-3 center" >
      </div>
    </div>
      <loader v-show="isLoading"></loader>
  </section>
</template>

<script type="text/javascript">

  import datePicker from 'vue-bootstrap-datetimepicker';
  import moment from 'moment';

  import 'eonasdan-bootstrap-datetimepicker/build/css/bootstrap-datetimepicker.css';
  import axios from 'axios';

  export default {
    created(){
      const market_id = this.$route.params.market_id;
      axios.defaults.headers.common['Authorization'] = `JWT ${localStorage.getItem('jwtToken')}`;
      axios.get(process.env.BACKEND+"market/"+market_id+"/",)
      .then(response => {
        this.isLoading = false;
        if ('error' in response){
          this.showDismissibleAlertError = true;
          this.error = response['error'];
          this.isLoading = false;
        }
        else{
          const market_data = response.data;
          this.form.title = String(market_data.title);
          this.form.hashtag = String(market_data.hashtag);
          this.form.date_starting = moment(market_data.date_starting).format('YYYY-MM-DD HH:mm')
          this.form.date_ending =  moment(market_data.date_ending).format('YYYY-MM-DD HH:mm')
          }
      })
      .catch(error => {
              const response = error.response
              this.isLoading = false;
              if (response.status == 400){
                this.showDismissibleAlertError = true;
                console.log(response)
                const errors = response['data']['error'];
                if (typeof errors === "object"){
                  let index = 0;
                  for (let key in response['data']['error']) {
                    this.error = response['data']['error'][key][0];
                  }
                }else{
                    this.error = response['data']['error']
                }

              }else{
              this.error = "Błąd po stronie serwera. Skontaktuj się z administratorem."
            }
      })

  },
    computed: {
        state () {
          return this.form.title.length == 0 ? false : true
        },
        invalidFeedback () {
          if (this.form.title.length == 0) {
            return 'pole wymagane'
          }
        },

      },
    data() {
      return {
        pathToEditPanel: "/panel_edycji/"+this.$route.params.market_id,
        isLoading:false,
        showDismissibleAlertError:false,
        showDismissibleSuccess:false,
        error:"",
        formSubmitted:false,
        form: {
          title:"",
          hashtag:"",
          date_starting: moment(null),
          date_ending: moment(null),
        },
        configs: {
          start: {
            format: 'YYYY-MM-DD HH:mm',
            sideBySide: true,
          },
          end: {
            format: 'YYYY-MM-DD HH:mm',
            sideBySide: true,
          }
        },
      }
    },
    components: {
      datePicker,
      axios,
    },
    methods: {

    submitForm(){
      this.showDismissibleAlertError = false;
        this.showDismissibleSuccess = false;
      if (this.form.title.length > 0){
            this.isLoading = true
            const market_id = this.$route.params.market_id;
            axios.defaults.headers.common['Authorization'] = `JWT ${localStorage.getItem('jwtToken')}`;
            axios.put(process.env.BACKEND+"market/"+market_id+"/", this.form )
            .then(response => {
              this.isLoading = false;
              if ('error' in response){
                this.showDismissibleAlertError = true;
                this.error = response['error'];
                this.isLoading = false;
              }
              else{
                  this.showDismissibleSuccess = true;
              }
            })
            .catch(e => {
              this.isLoading = false;
              this.error = "Błąd po stronie serwera. Skontaktuj się z administratorem."
              console.log(e)
            })
          }
      },

      onStartChange(e) {
        console.log('onStartChange', e.date);
        this.$set(this.configs.end, 'minDate', e.date || null);
      },
      onEndChange(e) {
        console.log('onEndChange', e.date);

      },
    },
  }

</script>
