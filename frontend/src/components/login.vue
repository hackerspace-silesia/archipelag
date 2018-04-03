<template>
<div id="login">
    <div class="col-md-2 text-center" >
    </div>
  <div class="col-md-8 mx-auto text-center" >

    <form  @submit.prevent="submitForm">
      <b-card bg-variant="light" class="bg-dark" style="color:white">
        <b-alert variant="danger"
       dismissible
       :show="showDismissibleAlert"
       @dismissed="showDismissibleAlert=false"
       >
        {{error}}
        </b-alert>
          <h2>Witaj w archipelagu</h2>

          <b-form-group vertical
                        label="Nick:"
                        label-class="text-sm-center"
                        label-for="username">
            <b-form-input v-model="form.username" id="lousernamegin"></b-form-input>
          </b-form-group>
          <b-form-group vertical
                        label="Hasło:"
                        label-class="text-sm-center"
                        label-for="password">
            <b-form-input v-model="form.password" id="password" type="password"></b-form-input>
          </b-form-group>

        </b-form-group>
        <div class="form-group">
          <button class="btn btn-primary" type="submit" @keyup.enter="submitForm"><i class="glyphicon glyphicon-ok"></i> Zaloguj </button>
        </div>
        <div class="col-md-12 text-center" >
          Jeżeli jeszcze nie masz konta, zarejestruj się <router-link to="/signUp"><a> tutaj</a></router-link>
        </div>
      </b-card>
    </form>

</div>

    <loader v-show="isLoading"></loader>
</div>
</template>

<script type="text/javascript">

  import axios from 'axios';

  export default {
    data() {
      return{
        isLoading:false,
          error:'',
          form:{
            username:'',
            password:''
          },
          showDismissibleAlert: false
    }

    },
    components: {
      axios
    },
    methods: {
      submitForm(){
        if(this.areFieldsCorrect() === true){
          this.isLoading=true;
          axios.post(process.env.BACKEND+"ngo/login/",this.form)
         .then(response =>{

           this.isLoading=false;
            localStorage.setItem('jwtToken', response.data.token);
            console.log(response.data.user.organisation)
            localStorage.setItem('ngo_name',  response.data.user.organisation);
            localStorage.setItem('coins',  response.data.user.coins);
            this.$eventHub.$emit('logged-in');
            this.$router.push('/');
         }).
           catch(e => {
             this.isLoading=false;
             this.showDismissibleAlert=true
             const error_msg = (e.response)
             if (e.response == undefined){
                this.error = "Błąd po stronie serwera. Skontaktuj się z administratorem."
             }else{
                this.error = "Wpisz poprawną nazwę użytkownika i hasło."

             }

         })
        }

      },

      areFieldsCorrect(){
        if (this.form.login == 0) {
          this.showDismissibleAlert=true
         this.error = "Wprowadż login"
         return false;
        } else if (this.form.password == 0) {
          this.showDismissibleAlert=true
          this.error = "Wprowadż hasło"
          return false;
        }else{
          return true;
      }

    },
  }
}

</script>
