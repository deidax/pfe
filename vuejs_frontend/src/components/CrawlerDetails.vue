<template>
  <v-row justify="center">
    <v-dialog
      v-model="openDialog"
      fullscreen
      hide-overlay
      transition="dialog-bottom-transition"
    >
      <v-card>
        <v-toolbar
          dark
          color="primary"
        >
          <v-btn
            icon
            dark
            @click="closeDialog()"
          >
            <v-icon>mdi-close</v-icon>
          </v-btn>
          <v-toolbar-title>Settings</v-toolbar-title>
          <v-spacer></v-spacer>
          <!-- <v-toolbar-items>
            <v-btn
              dark
              text
              @click="closeDialog"
            >
              Save
            </v-btn>
          </v-toolbar-items> -->
        </v-toolbar>
        <v-list
          three-line
          subheader
        >
          <!-- <v-subheader>Loading Products Data From Avito</v-subheader> -->
          <v-list-item>
            <v-list-item-content>
            <v-list-item-title><i>Loading Products Data From Avito</i></v-list-item-title>
              <v-list-item-title>
                <v-progress-linear
                  v-model="percentage"
                  height="25"
                >
                  <strong>{{ percentage }}%</strong>
                </v-progress-linear>
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>
              <v-list-item-title>Products found: <b>{{ activeCrawlerDetails.number_of_products_found }}</b></v-list-item-title>
              <v-list-item-title>Estimated time to finish: <b>{{ activeCrawlerDetails.estimated_time_to_finish }}</b></v-list-item-title>
             <!-- <v-list-item-subtitle>{{ activeCrawlerDetails.number_of_products_found }}</v-list-item-subtitle> -->
            </v-list-item-content>
          </v-list-item>
        </v-list>
        <v-divider></v-divider>
        <v-list
          three-line
          subheader
        >
          <v-subheader>General</v-subheader>
          <v-list-item>
            <v-list-item-action>
              <v-checkbox v-model="notifications"></v-checkbox>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Notifications</v-list-item-title>
              <v-list-item-subtitle>Notify me about updates to apps or games that I downloaded</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-action>
              <v-checkbox v-model="sound"></v-checkbox>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Sound</v-list-item-title>
              <v-list-item-subtitle>Auto-update apps at any time. Data charges may apply</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-action>
              <v-checkbox v-model="widgets"></v-checkbox>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>Auto-add widgets</v-list-item-title>
              <v-list-item-subtitle>Automatically add home screen widgets</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card>
    </v-dialog>
  </v-row>
</template>
<script>
  export default {
    name: 'CrawlerDetails',
    props:{
        openDialog: Boolean,
        percentage: 0,
        activeCrawlerDetails: {}
    },
    data () {
      return {
        notifications: false,
        sound: true,
        widgets: false,

        openDialogSwitch: false
      }
    },
    methods: {
      closeDialog(){
        let openDialogSwitch = this.openDialog
        openDialogSwitch = false
        this.$emit('update-openDialog', openDialogSwitch)
      }
    }
    

  }
</script>