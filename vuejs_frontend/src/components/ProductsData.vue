<template>
   <v-app id="inspire">
      <v-main>
        <v-btn color="error" 
              style="margin-right: 10px;margin-bottom:10px" 
              @click="dropProducts"
              :disabled="getJobState != 'finished' || getProductsDataFromDB.length == 0  ? true : false"
              >
          <v-icon left>mdi-database-remove</v-icon>
              CLEAR PRODUCTS DATA
        </v-btn>
        <v-btn 
              style="margin-right: 10px;margin-bottom:10px" 
              @click="refreshDataTable"
              >
          <v-icon left>mdi-database-refresh</v-icon>
              Refresh
        </v-btn>
        <v-card>
          <v-card-title v-if="getProductsDataFromDB.length > 0">
            Products Data ({{getProductsDataFromDB.length}} products)
            <v-spacer></v-spacer>
            </v-card-title>
          <v-card-title v-else>
            No products data found
            <v-spacer></v-spacer>
            </v-card-title>
          <v-data-table v-show="getProductsDataFromDB.length > 0"
            :headers="headers"
            :items="getProductsDataFromDB"
            class="elevation-1"
            :loading="getLoadingProductsData"
            loading-text="Loading... Please wait, this might take sometime"
          >
            <template v-slot:item.url="{ item }">
              <a :href="item.url" target="_blank">{{item.url}}</a>
            </template>
          </v-data-table>
        </v-card>
        <v-snackbar
          ref="dropProductsData"
          elevation="24"
          color="success"
          v-model="dropProductsDataAlert"
          :timeout="dropProductsDataTimeoutMessage"
        >
            <v-icon large>{{dropProductsDataAlertIcon}}</v-icon>
            <b style="font-size:150%; margin-left:5px">{{ dropProductsDataAlertMessage }}</b>
            <template v-slot:action="{ attrs }">
              <v-btn
                color="white"
                text
                v-bind="attrs"
                @click="dropProductsDataAlert = false"
              >
                Close
              </v-btn>
            </template>
        </v-snackbar>
        <v-overlay :value="getLoadingProductsDrop">
          <v-progress-circular
            indeterminate
            size="64"
          ></v-progress-circular>
        </v-overlay>
      </v-main>
   </v-app>
</template>


<script>
import {mapActions,mapGetters} from "vuex"

  export default {
    name: 'CreateCrawler',

    data()
    {
      return{
        productsKeys: [],
        headers: [],
        dropProductsDataAlert: false,
        dropProductsDataTimeoutMessage: 5000,
        dropProductsDataAlertIcon: '',
        dropProductsDataAlertMessage: '',

      }
    },

    watch: {
      getFullPath(){
        this.renderProductsDataTable()
        console.log(this.headers)
      }
    },

    mounted(){
      
    },

    computed: {
      ...mapGetters("Crawler",["getProductsDataFromDB"]),
      ...mapGetters("Crawler",["getLoadingProductsData"]),
      ...mapGetters("Crawler",["getLoadingProductsDrop"]),
      ...mapGetters("Crawler",["getJobState"]),

      getFullPath () {
        return this.$route.path
      },
    },

    methods:{
        ...mapActions('Crawler',['getProductsData']),
        ...mapActions('Crawler',['dropProductsData']),

        removeDuplicates(array) {
          return array.filter((a, b) => array.indexOf(a) === b)
        },

        getProductsDataElementsKeys(){
          try {
            let _productkeys = []
            this.getProductsDataFromDB.forEach(product => {
              _productkeys.push(Object.keys(product))
            });
            let mergeProductsKeys = [].concat.apply([], _productkeys);
            this.productsKeys = this.removeDuplicates(mergeProductsKeys)
          } catch (error) {
            console.error('No Products data')
          }
          
        },

        generateHeaders(){
          try {
            this.productsKeys.forEach(key => {
              let header = {}
              header['text'] = key;
              header['value'] = key;
              header['align'] = 'left'
              this.headers.push(header)
            });
          } catch (error) {
            console.error('No Products data')
          }
          
        },

        renderProductsDataTable(){
          this.getProductsData()  
          this.getProductsDataElementsKeys()
          this.generateHeaders()
        },

        refreshDataTable(){
          location.reload();
        },

        dropProducts(){
          let vm = this
          this.dropProductsData(vm)
        }
        
    },

    created() {
      this.renderProductsDataTable()
    }
  }
</script>
