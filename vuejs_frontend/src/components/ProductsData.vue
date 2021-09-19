<template>
   <v-app id="inspire">
      <v-main>
        <v-card>
          <v-card-title>
            Products Data
            <!-- {{getRunningCrawlerTaskId['task_id']}} -->
            <v-spacer></v-spacer>
            </v-card-title>
          <v-data-table
            :headers="headers"
            :items="getProductsDataFromDB"
            class="elevation-1"
            :loading="getLoadingProductsData"
            loading-text="Loading... Please wait, this might take sometime"
          >
            <!-- <template v-slot:header.name="{ generateHeaders }">
              {{ header.text.toUpperCase() }}
            </template> -->
          </v-data-table>
        </v-card>
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
        headers: []
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

      getFullPath () {
        return this.$route.path
      },
    },

    methods:{
        ...mapActions('Crawler',['getProductsData']),

        removeDuplicates(array) {
          return array.filter((a, b) => array.indexOf(a) === b)
        },

        getProductsDataElementsKeys(){
          let _productkeys = []
          this.getProductsDataFromDB.forEach(product => {
            _productkeys.push(Object.keys(product))
          });
          let mergeProductsKeys = [].concat.apply([], _productkeys);
          this.productsKeys = this.removeDuplicates(mergeProductsKeys)
        },

        generateHeaders(){
          this.productsKeys.forEach(key => {
            let header = {}
            header['text'] = key;
            header['value'] = key;
            header['align'] = 'left'
            this.headers.push(header)
          });
        },

        renderProductsDataTable(){
          this.getProductsData()  
          this.getProductsDataElementsKeys()
          this.generateHeaders()
        }
        
    },

    created() {
      this.renderProductsDataTable()
    }
  }
</script>
