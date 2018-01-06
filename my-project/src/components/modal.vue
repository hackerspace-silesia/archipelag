<template id="modal-template">
  <div class="modal" v-show="show" v-transition="modal">
    <div class="modal-wrapper">
      <div class="modal-container">
        <content select=".modal-header">
          <div class="modal-header">
            <h3>
              Hello World
            </h3>
          </div>
        </content>
        <div class="modal-body">
          I said hello to world not you
        </div>
        <div class="modal-footer uk-clearfix">
            <button v-on="click: show = false" class="uk-button uk-button-success uk-float-right">Ok, I hear!</button>
        </div>
      </div>
    </div>
  </div>
</template>
