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
    <template slot="description" scope="row">
     <b-button size="lg"
              v-if="isDescription(row.item.description)"
               variant="success"  v-b-modal="row.index.toString()">
               Zobacz szczegóły
     </b-button>
     <div v-else>
       Brak szczegółów
     </div>
        <b-modal v-bind:id="row.index.toString()" ok-only>
              {{row.item.description}}
        </b-modal>
   </template>
       <template slot="id" scope="row">
        <b-button size="lg" @click.stop="row.toggleDetails"
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
                      @click.stop="openInfoModal(message, row.item, $event.target)"
                      class="mr-1">
              {{ message.type }}
            </b-button>
            <b-button variant="warning" size="" @click.stop="showLogs(row.item.id)" class="mr-1">
              Zobacz kto już udostępnił
            </b-button>
           </b-card>

           <b-modal id="modalInfo"  @ok="handleSharedMessage" @hide="resetModal" :title="modalInfo.title" ok-title="Nalicz punkty za udostępnienie" cancel-title="Anuluj">

                     <b-form-textarea id="textarea1"
                            :value="modalInfo.content"
                            :rows="5">

                      </b-form-textarea>
           </b-modal>
      </template>

    </b-table>

    <b-modal id="modalLogs" ok-only>
      <div v-for="log in logs">
        <b-alert show>  <b-badge> {{log.owner_name }}</b-badge>  udostępnił na {{log.message}} {{getHumanDate(log.date_created)}} dodane punkty: {{log.coins}} </b-alert>
      </div>
    </b-modal>
    <b-modal id="modalPoints" ok-only>
          {{modalPointsResponse}}
    </b-modal>
  </b-container>
  <loader v-show="isLoading"></loader>
    </div>
</template>

<script>
import axios from 'axios';
import moment from 'moment';


const items = [
]

export default {
  components: {
    axios,
  },
  data () {
    return {
      items: items,
      fields: [
        { key: 'owner', label: 'Organizacja', sortable: true, 'class': 'text-center' },
        { key: 'title', label: 'tytuł' , sortable: true,},
        { key: 'date_starting', label: "Rozpoczęcie" , sortable: true, formatter: 'getHumanDate'},
        { key: 'date_ending', label: 'Zakończenie', sortable: true, formatter: 'getHumanDate'},
        { key: 'date_modified', label: 'Data modyfikacji', sortable: true, formatter: 'getHumanDate'},
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
      logs : {},
      actualSharedMessageId : '',
      isLoading: false,
      modalPointsResponse: ''
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
    openInfoModal (message, row, button) {
      this.modalInfo.title = `Serwis: ${message["type"]}`;
      const content = message["content"]+" "+row.hashtag;
      this.modalInfo.content = content;
      this.actualSharedMessageId = message.id
      console.log(this.actualSharedMessageId)
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

      if (date == null){
        return '--';
      }
        return moment(date).format('YYYY-MM-DD HH:mm');
    },
   get_all_messages: function () {
     this.isLoading = true;
     axios.defaults.headers.common['Authorization'] = `JWT ${localStorage.getItem('jwtToken')}`;
     axios.get(process.env.BACKEND+"message/?format=json")

    .then(response =>{
    // JSON responses are automatically parsed.
    this.messages= response.data;
    this.isLoading = false;
    }).
      catch(e => {
        this.errors.push(e)
        this.isLoading = false;
      console.log(e);
    })
    },
    get_market:function(){
          this.isLoading = true;
          axios.defaults.headers.common['Authorization'] = `JWT ${localStorage.getItem('jwtToken')}`;
          axios.get(process.env.BACKEND+"market/?format=json")

    .then(response =>{
    // JSON responses are automatically parsed.
    this.items= response.data;
    this.isLoading = false;
    }).catch(e => {
        console.log(e)
      console.log(e);
      this.isLoading = false;
    })
    },
    get_logs:function(market_id){
      this.isLoading = true;
      axios.defaults.headers.common['Authorization'] = `JWT ${localStorage.getItem('jwtToken')}`;
          axios.get(process.env.BACKEND+"share_log/"+market_id+"/?format=json")

        .then(response =>{
    // JSON responses are automatically parsed.
      this.logs = response.data;
      this.isLoading = false;
    }).catch(e => {
      this.isLoading = false;
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
    handleSharedMessage () {
      this.sendShareEvent(this.actualSharedMessageId);

      this.$root.$emit('bv::show::modal', 'modalPoints');
    },
    showLogs(market_id){
      this.get_logs(market_id);
      this.$root.$emit('bv::show::modal', 'modalLogs');
    },
    sendShareEvent:function(message_id){
      this.isLoading = true;
      axios.defaults.headers.common['Authorization'] = `JWT ${localStorage.getItem('jwtToken')}`;
          axios.post(process.env.BACKEND+"share_log/"+message_id+"/")
        .then(response =>{
    // JSON responses are automatically parsed.
    if ('success' in response.data){
        this.modalPointsResponse = response.data.success;
    }else{
      this.modalPointsResponse = response.data.error;
    }
      this.isLoading = false;
    }).catch(e => {
      this.isLoading = false;
      console.log(e);
    })
    },
    isDescription(msg){
      if (msg.length> 0)
      {
        return true;
      }
        else{
          return false;
        }

    }

  }
}
</script>

<style>
.description{
    left: 0px;
}
</style>
<!-- table-complete-1.vue -->
