<template>
  <v-row justify="center">
    <v-dialog
      v-model="openCreateForm"
      persistent
      max-width="600px"
    >
      <v-card>
        <v-card-title>
          <span class="text-h5">Create New Crawler</span>
        </v-card-title>
        <v-card-text>
          <v-form class="ccf" @submit.prevent="createNewCrawler" id="create-crawler-form">
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  label="Crawler Name*"
                  v-model="form.name"
                  name="name"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  label="Crawler Start URL*"
                  v-model="form.start_url"
                  hint="This's the Avito url where the crawler will start loading products data from"
                  name="start_url"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
          </v-form>
          <small>*indicates required field</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
           <v-btn
            color="blue darken-1"
            text
            @click="closeDialog()"
          >
            Close
          </v-btn>
          <v-btn
            type="submit" 
            :loading="isLoading" 
            form="create-crawler-form"
            color="blue darken-1"
            text
          >
            <!-- @click="closeDialog()" -->
            Save
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>
import {mapActions,mapGetters} from "vuex"
  export default {
    name: "CreateCrawler",
    
    props: {
      openCreateForm: Boolean,
    },

    data: () => ({
      form:{
          name: '',
          start_url: ''
      },
    }),

    computed: {
      ...mapGetters("Crawler",["isLoading"]),
    },

    methods: {
      ...mapActions('Crawler',['createCrawler']),
      ...mapActions('Crawler',['getAllCrawlers']),
      
      createNewCrawler(){
        let playload = {}
        playload['form'] = this.form
        playload['vm'] = this
        this.createCrawler(playload).then(this.closeDialog())
        this.$emit('update-crawlersList')
      },

      closeDialog(){
        let openForm = this.openCreateForm
        openForm = false
        this.$emit('update-openCreateForm', openForm)
    },

  }
}
</script>