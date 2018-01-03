<template>
  <section class="container">


    <div class="row">
      <div class="col-md-8">

        <div class="row">
          <div class="col-md-12">
            <button class="btn btn-default" @click.prevent="setNewValue()">Set new value pragmatically</button>
            <button class="btn btn-default" @click.prevent="updateConfig()">Reactive configs (Change viewMode)
            </button>
          </div>
        </div>

        <form method="post" action="/" @submit.prevent="submit()">

          <div class="form-group">
            <label>Select date (basic)</label>
            <date-picker v-model="form.date" :config="configs.basic" @dp-change="listenToChangeEvent"></date-picker>
          </div>

          <div class="form-group">
            <label for="date-time-input">Select date time (wrap)</label>
            <div class="input-group date">
              <date-picker v-model="form.dateWrap" id="date-time-input"
                           :wrap="true" :config="configs.wrap">
              </date-picker>
              <div class="input-group-addon">
                <span class="glyphicon glyphicon-calendar"></span>
              </div>
            </div>
          </div>

          <div class="form-group">
            <label>Select time</label>
            <div class="input-group">
              <date-picker :config="configs.timePicker" v-model="form.time" :wrap="true"
                           placeholder="Time"></date-picker>
              <div class="input-group-addon">
                <span class="glyphicon glyphicon-time"></span>
              </div>
            </div>
          </div>





          <div class="form-group">
            <label>Works in modals as well </label>
            <button type="button" class="btn btn-info" data-toggle="modal" data-target="#date-modal">Open in
              modal


            </button>
          </div>

          <div class="form-group">
            <label>Select date (localization)</label>
            <date-picker :config="configs.locale" v-model="form.dateLocale"></date-picker>
          </div>

          <div class="form-group">
            <label>Select date (inline)</label>
            <date-picker :config="configs.inline" v-model="form.dateInline"></date-picker>
            <p class="help-block">
              {{form.dateInline}}
            </p>
          </div>

          <div class="row">
            <div class="col-md-6">
              <div class="form-group">
                <label>Start date</label>
                <date-picker v-model="form.startDate" :config="configs.start" ref="startDate"
                             @dp-change="onStartChange"></date-picker>
              </div>
            </div>
            <div class="col-md-6">
              <div class="form-group">
                <label>End date</label>
                <date-picker v-model="form.endDate" :config="configs.end" ref="endDate"
                             @dp-change="onEndChange"></date-picker>
              </div>
            </div>
          </div>

          <hr>

          <div class="form-group">
            <button class="btn btn-primary" type="submit"><i class="glyphicon glyphicon-ok"></i> Validate form</button>
          </div>

        </form>
      </div>
    </div>

    <!-- bs modal -->
    <div class="modal fade" tabindex="-1" role="dialog" id="date-modal">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span
              aria-hidden="true">&times;</span></button>
            <h4 class="modal-title">Modal example</h4>
          </div>
          <div class="modal-body">
            <div class="form-group">
              <label>Select a date</label>
              <date-picker v-model="form.dateModal"></date-picker>
            </div>
            <pre>{{form.dateModal}}</pre>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" data-dismiss="modal">Save</button>
          </div>
        </div>
      </div>
    </div>

  </section>
</template>

<script type="text/javascript">

  import datePicker from 'vue-bootstrap-datetimepicker';
  import moment from 'moment';

  import 'eonasdan-bootstrap-datetimepicker/build/css/bootstrap-datetimepicker.css';
  export default {
    data() {
      return {
        form: {
          date: new Date(),
          dateWrap: null,
          dateModal: moment(),
          dateValidate: null,
          time: null,
          dateLocale: moment(),
          dateInline: moment().toString(),
          startDate: null,
          endDate: null
        },
        configs: {
          basic: {
            // https://momentjs.com/docs/#/displaying/format/
            format: 'DD/MM/YYYY'
          },
          wrap: {
            allowInputToggle: true
          },
          timePicker: {
            format: 'LT',
            useCurrent: false
          },
          locale: {
            // https://github.com/moment/moment/tree/develop/locale
            locale: 'hi',
          },
          inline: {
            format: 'LLL',
            inline: true,
            sideBySide: true
          },
          start: {
            format: 'DD/MM/YYYY',
            useCurrent: false,
            showClear: true,
            showClose: true,
            minDate: moment(),
            maxDate: false
          },
          end: {
            format: 'DD/MM/YYYY',
            useCurrent: false,
            showClear: true,
            showClose: true,
            minDate: moment()
          }
        },
      }
    },
    components: {
      datePicker
    },
    methods: {
      submit() {
        console.log('Form submit event');
        console.log(this.form);
        // http://vee-validate.logaretm.com/examples.html#component-example
        this.$validator.validateAll().then(result => {
          // eslint-disable-next-line
          alert(`Validation Result: ${result}`);
        });
      },
      setNewValue() {
        console.log('Set new value');
        // https://momentjs.com/docs/#/manipulating/
        this.form.date = moment().add(7, 'days');
      },
      updateConfig() {
        console.log('Update config');
        // Right way to update config
        this.$set(this.configs.basic, 'viewMode', 'years');
      },
      listenToChangeEvent(...args) {
        console.log('listen To dp.change event - ', ...args);
      },
      onStartChange(e) {
        console.log('onStartChange', e.date);
        this.$set(this.configs.end, 'minDate', e.date || null);
      },
      onEndChange(e) {
        console.log('onEndChange', e.date);
        this.$set(this.configs.start, 'maxDate', e.date || null);
      }
    },
  }
</script>
