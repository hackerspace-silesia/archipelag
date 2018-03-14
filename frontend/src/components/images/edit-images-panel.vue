<template>
  <div role="tablist">
        <h2>Panel edycji obrazków</h2>

    <b-card no-body class="mb-1">
      <b-card-header header-tag="header" class="p-1" role="tab">
        <b-btn block href="#" v-b-toggle.accordion2 variant="info">Usuń obrazki z marketu</b-btn>
      </b-card-header>
      <b-collapse v-on:show="onOpen" id="accordion2" accordion="my-accordion" role="tabpanel">
        <b-card-body>
            <edit_images ref="editImage"></edit_images>
        </b-card-body>
      </b-collapse>
    </b-card>
    <b-card no-body class="mb-1">
      <b-card-header header-tag="header" class="p-1" role="tab">
        <b-btn block href="#" v-b-toggle.accordion1 variant="info">Dodaj obrazki</b-btn>
      </b-card-header>
      <b-collapse id="accordion1"  accordion="my-accordion" role="tabpanel">
        <b-card-body>
          <add-image></add-image>
        </b-card-body>
      </b-collapse>
    </b-card>

   <router-link :to="{path: pathToEditPanel}"> <button class="btn btn-primary" ><i class="glyphicon glyphicon-ok"></i>Wróć do panelu edycji </button></router-link>

  </div>

</template>

<script>
   import add_image from './add-market-images';
   import adit_images from './edit-images';
export default {
  data () {
    return {
      isOpenEditor:false,
      pathToEditPanel: "/panel_edycji/"+this.$route.params.market_id,
    }
  },
      components: {
        'add-image':add_image,
        'edit_images':adit_images,
    },
  methods:{
      onOpen(yolo){
        this.$refs['editImage'].getImages()
      }
  }
}
</script>

