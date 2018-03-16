<template>
  <section class="container">
    <b-alert variant="danger"
       dismissible
       :show="showDismissibleAlertError"@dismissed="showDismissibleAlertError=false">
    {{error}}
    </b-alert>

    <div class="row">
      <div class="col-md-3 center" >
      </div>
      <div class="col-md-6 center" >

    <b-card bg-variant="light">
        <h2>Dodaj wydarzenie</h2>
        <h3>1/3</h3>
        <h4>Dodaj podstawowe informacje</h4>
        <hr>
        <form @submit.prevent="submitForm" v-if="!formSubmitted">
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
        <div v-else>
          Dodano wydarzenie, dodaj wiadomości do udostępniania
        </div>
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
        isLoading:false,
        showDismissibleAlertError:false,
        error:"",
        formSubmitted:false,
        form: {
          owner:1,
          title:"",
          hashtag:"",
          date_starting: null,
          date_ending: null,
        },
        configs: {
          start: {
            format: 'YYYY-MM-DD HH:mm',
            minDate: moment(),
            maxDate: false,
            sideBySide: true,
          },
          end: {
            format: 'YYYY-MM-DD HH:mm',
            minDate: moment(),
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
        isFormValidate(){
          if (this.form.title.length == 0){
              return false;
          }else if(this.form["date_starting"] == null && this.form["date_ending"] != ""){
              this.showDismissibleAlertError = true;
               this.error = "Data zakończenia musi mieć datę rozpoczęcia."
              return false;
          }else if(this.form["date_starting"] != "" && this.form["date_ending"] == null) {
               this.showDismissibleAlertError = true;
               this.error = "Data rozpoczęcia musi mieć datę zakończenia."
              return false;
          }
          this.showDismissibleAlertError = false;
          return true;
        },
    submitForm(){
      if (this.isFormValidate() == true){
            this.isLoading = true
            axios.defaults.headers.common['Authorization'] = `JWT ${localStorage.getItem('jwtToken')}`;
            axios.post(process.env.BACKEND+`market/`, {
              body: this.form
            })
            .then(response => {
              this.isLoading = false;
              this.redirectOrReturnError(response);
            })
            .catch(error => {
                console.log(error)
              const response = error.response
              this.isLoading = false;
              if (error.status == 400){
                this.showDismissibleAlertError = true;
                const errors = response['data']['error'];
                if (typeof errors === "object"){
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
          }
      },

      redirectOrReturnError(response){
        this.isLoading = false;
        console.log(response.status_code)
          this.imagesUrl = process.env.BACKEND+'images/';
          const market_id = response['data']['message']['market_id'];
          this.$router.push('/dodaj_obrazek/'+market_id);
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
