<template>
   <v-app id="inspire">
      <v-main>
            <v-form class="ccf" @submit.prevent="executeCrawler" id="create-crawler-form">
              <v-container>
                <v-row>
                  <v-col
                    cols="12"
                    sm="6">
                    <v-text-field
                      v-model="form.start_url"
                      name="start_url"
                      solo
                      label="Start URL"
                      clearable>
                      </v-text-field>
                      <v-spacer></v-spacer>
                      <v-btn type="submit" :loading="isLoading" color="primary" form="create-crawler-form">Go</v-btn>
                  </v-col>
                </v-row>
              </v-container>
            </v-form>
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
        form:{
          start_url: ''
        },
      }
    },

    computed: {
      ...mapGetters("Crawler",["isLoading"]),
    },

    methods:{
        ...mapActions('Crawler',['runCrawler']),
        executeCrawler(){
          this.runCrawler(this.form)
        },
        
    },
  }
</script>
