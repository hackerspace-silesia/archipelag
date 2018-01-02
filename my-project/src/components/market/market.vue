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
        <b-button size="sm" @click.stop="row.toggleDetails" v-on:click="get_messages(row.item.id)">
          {{ row.detailsShowing ? 'Schowaj' : 'Pokaż' }} udostępnianie
        </b-button>
      </template>
      <template slot="row-details" scope="row">
        <b-card>

        <b-button v-for="item in messages" variant="primary" size="" @click.stop="info(row.item, item.type, $event.target)" class="mr-1">
          {{ item.type }}
        </b-button>

        <b-button variant="warning" size="" @click.stop="info(row.item, 'Udostępnienia', $event.target)" class="mr-1">
          Zobacz kto już udostępnił
        </b-button>
        </b-card>
      </template>
      <template slot="message-content" scope="row">
        Nothing
      </template>

    </b-table>
        <b-modal id="modalInfo" @hide="resetModal" :title="modalInfo.title" ok-only>
      <pre>{{ modalInfo.content }}</pre>
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
      messages : {}
    }
  },
  created(){
  axios.get("http://127.0.0.1:8000/market/?format=json")
    .then(response =>{
    // JSON responses are automatically parsed.
    this.items= response.data;
      console.log(this.items);
    })
.
  catch(e => {
    this.errors.push(e)
  console.log(e);
})
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
    info (item, index, button) {
      this.modalInfo.title = `Serwis: ${index}`
      //JSON.stringify(item, null, 2)
      this.modalInfo.content = "Wiadomośc do udostępniania"
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
   get_messages: function (id) {

     axios.get("http://127.0.0.1:8000/message/?format=json&market_id="+id)
    .then(response =>{
    // JSON responses are automatically parsed.
    this.messages= response.data;
      console.log(this.messages);
    }).
      catch(e => {
        this.errors.push(e)
      console.log(e);
    })
    }

  }
}
</script>

<!-- table-complete-1.vue -->
