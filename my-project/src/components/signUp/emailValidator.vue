<template>
<div id="emailValidator">
  <b-form-group vertical
                label="e-mail:"
                label-class="text-sm-center"
                label-for="email">
    <b-form-input
        :state="isValid"
        id="email"
        aria-describedby="inputLiveFeedback"
        @change.native="validateEmail">
      </b-form-input>
    <b-form-invalid-feedback id="inputLiveFeedback">
      {{error}}
    </b-form-invalid-feedback>
              </b-form-group>
</div>

</template>

<script type="text/javascript">
  export default {
        props:['onEmailValidateResult'],
    data() {
      return{
        isValid:false,
        error:"",
    }
    },
    methods: {
      showErrorMessage(msg){
        this.error = msg;
        this.isValid = false;

      },
      validateEmail(event){
        // Validate lowercase letters
        let input = event.target.value;

        if(this.isEmailCorrect(input) == true){
          this.isValid = true;
          this.error = "";

         }else{
           this.isValid = false;
          this.error = "Niepoprawny email";
         }
         this.onEmailValidateResult( this.isValid, input );
       },
         isEmailCorrect(email) {
         var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
         return re.test(String(email).toLowerCase());
       }

  }
  }
</script>
