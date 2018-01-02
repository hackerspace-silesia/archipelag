<template>

  <div class="market">
     <hr>
    <h1>Witaj na targu</h1>
    <hr>
  <b-container fluid>
    <!-- User Interface controls -->
    <b-row>
      <b-col md="4" class="my-1">
        <b-form-group horizontal label="Szukaj" class="mb-0">
          <b-input-group>
            <b-form-input v-model="filter" placeholder="Wpisz szukane słowo" />
            <b-input-group-button>
              <b-btn :disabled="!filter" @click="filter = ''">Czyść</b-btn>
            </b-input-group-button>
          </b-input-group>
        </b-form-group>
      </b-col>

      <b-col md="4" class="my-1">
        <b-form-group horizontal label="Liczba wyników" class="mb-0">
          <b-form-select :options="pageOptions" v-model="perPage" />
        </b-form-group>
      </b-col>

      <b-col md="4" class="my-1">
        <b-pagination :total-rows="totalRows" :per-page="perPage" v-model="currentPage" class="my-0" />
      </b-col>

    </b-row>

    <!-- Main table element -->
    <b-table show-empty
             stacked="md"
             :items="items"
             :fields="fields"
             :current-page="currentPage"
             :per-page="perPage"
             :filter="filter"
             :sort-by.sync="sortBy"
             :sort-desc.sync="sortDesc"
             @filtered="onFiltered"
    >

       <template slot="id" scope="row">
        <b-button size="sm" @click.stop="row.toggleDetails"
                  variant="success"
                  v-if="get_market_messages(row.item.id).length > 0">
          {{ row.detailsShowing ? 'Schowaj' : 'Pokaż' }} udostępnianie
        </b-button>
         <div v-else>
        Brak wiadomości
      </div>
      </template>
      <template slot="row-details" scope="row">
        <b-card ref="buttons_view">
            <b-button v-for="message in get_market_messages(row.item.id)"
                      variant="primary" size=""
                      @click.stop="info(message, row.item, $event.target)"
                      class="mr-1">
              {{ message.type }}
            </b-button>
            <b-button variant="warning" size="" @click.stop="logs()" class="mr-1">
              Zobacz kto już udostępnił
            </b-button>
           </b-card>
      </template>

    </b-table>
    <b-modal id="modalInfo"  @ok="handleOk" @hide="resetModal" :title="modalInfo.title" ok-title="Udostępniono" cancel-title="Anuluj">

              <b-form-textarea id="textarea1"
                     :value="modalInfo.content">

               </b-form-textarea>

    </b-modal>

        <b-modal id="modalPoints"  @hide="resetModal" ok-only>
          Naliczono punkty za udostępnienie

    </b-modal>

        </b-modal>

    <b-modal id="modalLogs"  @hide="resetModal" ok-only>
          Log log

    </b-modal>


  </b-container>
    </div>
</template>

<script>
import axios from 'axios';
import moment from 'moment';

const items = [
]

export default {
  data () {
    return {
      items: items,
      fields: [
        { key: 'owner', label: 'Organizacja', sortable: true, 'class': 'text-center' },
        { key: 'title', label: 'tytuł' , sortable: true,},
        { key: 'url', label: 'url',sortable: true, },
        { key: 'date_starting', label: "Rozpoczęcie" , sortable: true, formatter: 'getHumanDate'},
        { key: 'date_ending', label: 'Zakończenie', sortable: true, formatter: 'getHumanDate'},
        { key: 'hashtag', label: 'hashtag', sortable: true, },
        { key: "id", label:"Akcje"}
      ],
      currentPage: 1,
      perPage: 10,
      totalRows: items.length,
      pageOptions: [ 5, 10, 15, 20 ],
      sortBy: null,
      sortDesc: false,
      filter: null,
      modalInfo: { title: '', content: '' },
      modalPoints: { title: '', content: '' },
      modalLogs: { title: '', content: '' },
      messages : {},
    }
  },
  created(){
    this.get_market();
    this.get_all_messages();
},
  computed: {
    sortOptions () {
      // Create an options list from our fields
      return this.fields
        .filter(f => f.sortable)
        .map(f => { return { text: f.label, value: f.key } })
    }
  },
  methods: {
    info (message, row, button) {
      this.modalInfo.title = `Serwis: ${message["type"]}`;
      //JSON.stringify(item, null, 2)
      const content = message["content"]+" "+row.hashtag;
      this.modalInfo.content = content;

      this.$root.$emit('bv::show::modal', 'modalInfo', button)
    },
    resetModal () {
      this.modalInfo.title = ''
      this.modalInfo.content = ''
    },
    onFiltered (filteredItems) {
      // Trigger pagination to update the number of buttons/pages due to filtering
      this.totalRows = filteredItems.length
      this.currentPage = 1
    },
    getHumanDate : function (date) {
        return moment(date).format('YYYY-MM-DD HH:MM');
    },
   get_all_messages: function () {

     axios.get("http://127.0.0.1:8000/message/?format=json")
    .then(response =>{
    // JSON responses are automatically parsed.
    this.messages= response.data;
    }).
      catch(e => {
        this.errors.push(e)
      console.log(e);
    })
    },
    get_market:function(){
          axios.get("http://127.0.0.1:8000/market/?format=json")
    .then(response =>{
    // JSON responses are automatically parsed.
    this.items= response.data;
    }).catch(e => {
        this.errors.push(e)
      console.log(e);
    })
    },
    get_market_messages:function (row_id) {

      const arrayLength = this.messages.length;
        let market_messages = []
        for (let i = 0; i < arrayLength; i++) {
            if (this.messages[i]['market'] == row_id){
                market_messages.push(this.messages[i]);
            }
        }
      return market_messages;
    },
    handleOk () {
      this.$root.$emit('bv::show::modal', 'modalPoints');
    },
    logs(){
        this.$root.$emit('bv::show::modal', 'modalLogs');
    },
    changeColor: function() {
		if (this.color == 'blue') {
			this.color = 'red';
		} else {
			this.color = 'blue';
		}
	}
  }
}
</script>

<!-- table-complete-1.vue -->
