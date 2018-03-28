<template>
<div>
  <form >
<b-form-group class="col-md-12 center">
    <textarea class="col-md-12 center" id="textarea2"
                     state="invalid"
                     placeholder="Wpisz wiadomość"
                     v-model="message"
                     :rows="3"
                     required
                     @input="progressBarChange()"></textarea>

                     <b-progress height="2rem" class="col" :max="max" show-value>
                       <b-progress-bar :value="success" variant="success"></b-progress-bar>
                       <b-progress-bar :value="warning" variant="danger"></b-progress-bar>
                     </b-progress>
                        <b-alert show class="col" :variant="getVariant()"> limit znaków to {{service.char_restriction}} </b-alert>
    <button style="background-color: rgb(90, 128, 204);" class="btn btn-primary" type="submit" @click.prevent="getFormValues(message, service.id, service.char_restriction)">
     Zapisz </button>

</b-form-group>
</form>
</div>
</template>

<script type="text/javascript">

  export default {
      created(){
        if("content" in this.service){
            this.message = this.service.content;
        }
      },
    props:['service', 'getFormValues', ],
    data: function (){
        return {
          message: "",
           max:this.service.char_restriction,
           success: 0,
          warning: 0,
     };
    },
    methods:{
      progressBarChange(){
        console.log("Długość waidomość")
        console.log(this.message.length)
        this.success = this.message.length;
    if (this.message.length <= this.service.char_restriction){
          this.max = this.service.char_restriction;
          this.warning = 0;
      }
      else{
        let number_of_to_many_chars = this.message.length-this.service.char_restriction;
        this.warning = number_of_to_many_chars;
        this.max = this.message.length;

        console.log("WARNING")
        console.log(number_of_to_many_chars)
      }
      console.log("Maksymalna")
      console.log(this.max)
      },
      getVariant(){

      if (this.message.length > this.service.char_restriction){
        return "danger";
      }
      return "success";
    }
    }
  }
</script>
