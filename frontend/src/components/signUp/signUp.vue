<template>
<div id="signUp">

  <div class="col-md-8 mx-auto text-center" v-if="duringCreating">
    <form class="bg-dark" style="color:white" @submit.prevent="submitForm" @keyup.enter="submitForm">
      <b-card bg-variant="dark">
        <b-alert variant="danger"
       dismissible
       :show="showDismissibleAlert"
       @dismissed="showDismissibleAlert=false"
       >
        {{error}}
        </b-alert>
          <h2>Zarejestruj się</h2>
          <b-form-group vertical
                        label="Nick do logowania:"
                        label-class="text-sm-center"
                        label-for="username">
            <b-form-input v-model="form.username" id="username"></b-form-input>
          </b-form-group>
          <b-form-group vertical
                        label="Nazwa organizacji:"
                        label-class="text-sm-center"
                        label-for="organisation">
            <b-form-input v-model="form.organisation" id="organisation"></b-form-input>
          </b-form-group>
        <email-validator
            v-bind:onEmailValidateResult="emailCheck">
        </email-validator>
        <password-validator
            v-bind:onPasswordValidateResult="passwordCheck">
        </password-validator>
        <select-recomendators
            v-bind:onSelectRecomendators="recomendatorUpdate">
        </select-recomendators>
              </b-form-group>
        </b-form-group>
        <div class="form-group">
          <button class="btn btn-primary" type="submit"><i class="glyphicon glyphicon-ok"></i> Zarejestruj </button>
        </div>
      </b-card>
    </form>
</div>
<div v-else>
  <b-alert class="col-md-8 mx-auto text-center"  variant="success" show>
    Twoje konto zostało stworzone poprawnie
    zaloguj się za pomocą nicku
    <router-link to="/login">
      <a> tutaj</a>
    </router-link>
    </b-alert>
</div>

    <loader v-show="isLoading"></loader>
</div>
</template>
<script type="text/javascript">
  import passwordValidator from './passwordValidator';
  import emailValidator from './emailValidator';
  import selectRecomendators from './selectRecomendators';
  import axios from 'axios';

  export default {
    data() {
      return{
        isLoading:false,
          error:'',
          passwordValidate:false,
          form:{
            username:'',
            organisation:'',
            password:'',
            email:'',
            ngo : null,
          },
          duringCreating: true,
          showDismissibleAlert: false
    }
    },
    components: {
      axios,
      'password-validator':passwordValidator,
      'email-validator':emailValidator,
      'select-recomendators':selectRecomendators,
    },
    methods: {
      passwordCheck(isValid, passwordValue){
        this.isValid = isValid;
        this.form.password = passwordValue;
      },
      emailCheck(isValid, emailValue){
        this.isValid = isValid;
        this.form.email = emailValue;
      },
      recomendatorUpdate(ngoName){
          this.form.ngo = ngoName;
      },
      submitForm(){
        this.showDismissibleAlert = false;
        if(this.areFieldsCorrect() === true){
          this.isLoading=true;
          axios.post(process.env.BACKEND+"ngo/",this.form)
        .then(response =>{
           this.isLoading=false;
           if ("error" in response.data){
              this.showDismissibleAlert = true;
              this.error = response.data.error;
           }else{
             console.log("false")
             this.duringCreating = false;
           }
         }).
           catch(e => {
             this.isLoading = false;
             this.showDismissibleAlert = true;
             const error_msg = e.response
             if (error_msg == undefined){
                this.error = "Błąd po stronie serwera. Skontaktuj się z administratorem."
             }else{
                this.error = "Wpisz poprawną nazwę użytkownika i hasło."
             }
         })
        }
      },
      areFieldsCorrect(){
        if (this.form.username == "" | (this.form.organisation == "")) {
            this.showDismissibleAlert = true
            this.error = "Wypełnij puste pola"
            return false;
       } else if (this.isValid == false) {
            this.showDismissibleAlert = true
            this.error = "Nie wszystkie pola zostały wypełnione poprawnie";
            return false;
        }else{
            return true;
      }
    },
  }
}

</script>
