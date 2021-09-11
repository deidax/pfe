<template>
  <v-container>
  <nav-bar/>
  <span style="display: none">{{displayOtherServerErrors}}</span>
  <h1 v-show="createCrawler">Create a new Crawler</h1>
  <create-crawler v-show="createCrawler"/>
  <crawlers-list v-show="crawlersList"/>
  <!-- Server errors -->
      <v-snackbar
        v-model="snackbar"
        color="red"
        :vertical="true"
      >
      <v-icon>mdi-alert</v-icon>
      <strong style="margin-left: 5px">Oops!...Something is wrong</strong>
        <ul>
          <li v-for="(error, index) in getOtherErrors" :key="index">{{error}}</li>
        </ul>
        <template v-slot:action="{ attrs }">
          <v-btn
            color="white"
            text
            v-bind="attrs"
            @click="snackbar = false"
          >
            Close
          </v-btn>
        </template>
      </v-snackbar>
</v-container>
</template>

<script>
import CrawlersList from '../components/CrawlersList.vue'
import CreateCrawler from '../components/CreateCrawler.vue'
import NavBar from '../components/NavBar.vue'
import {mapActions,mapGetters} from "vuex"

  export default {
    name: 'Crawler',

    data: () => ({
      snackbar: false,
    }),
    
    components: {
        NavBar,
        CreateCrawler,
        CrawlersList   
    },
    computed: {
      ...mapGetters("Crawler",["getOtherErrors"]),

      displayOtherServerErrors(){
        if(this.getOtherErrors == null || this.getOtherErrors.length == 0)
          return this.snackbar = false
        return this.snackbar = true
      },

      createCrawler() {
        if(this.$route.name == "create_crawler") {
          return true
        }
        return false
      },
      crawlersList() {
        if(this.$route.name == "crawlers_list") {
          return true
        }
        return false
      }
    }
  }
</script>
