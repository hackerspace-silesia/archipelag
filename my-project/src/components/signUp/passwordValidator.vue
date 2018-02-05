<template>
<div id="passwordValidator">
          <b-form-group vertical
                        label="Hasło:"
                        label-class="text-sm-center"
                        label-for="password">
                  <b-form-input
                    id="password"
                    type="password"
                    :state="isValid"
                     aria-describedby="inputLiveFeedback"
                   @change.native="validatePassword">
                </b-form-input>
<b-form-invalid-feedback id="inputLiveFeedback">
  {{error}}
</b-form-invalid-feedback>
              </b-form-group>
</div>

</template>

<script type="text/javascript">
  export default {
        props:['onPasswordValidateResult'],
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
      validatePassword(event){
        // Validate lowercase letters
        let input = event.target.value;
         var lowerCaseLetters = /[a-z]/g;
         var upperCaseLetters = /[A-Z]/g;
         var numbers = /[0-9]/g;
         if(input.match(lowerCaseLetters) == null) {
           this.showErrorMessage("hasło musi zawierać małe litery");
         }
         else if(input.match(upperCaseLetters) == null) {
           this.showErrorMessage("hasło musi zawierać duże litery");
         }
         else if(input.match(numbers) == null) {
           this.showErrorMessage("hasło musi zawierać liczby");
         }
         else if(input.length <= 8) {
           this.showErrorMessage("hasło musi się składać z minimum 8 znaków");
         }else{
          this.isValid = true;
          this.onPasswordValidateResult( this.isValid, input );
         }
        }
  }
  }
</script>
