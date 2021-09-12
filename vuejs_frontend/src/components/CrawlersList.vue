<template>
   <v-app id="inspire">
      <v-main>
        <v-card>
          <v-card-title>
            Crawlers List
            <!-- {{getRunningCrawlerTaskId['task_id']}} -->
            <v-spacer></v-spacer>
            <v-text-field
              v-model="search"
              append-icon="mdi-magnify"
              label="Search"
              single-line
              hide-details
            ></v-text-field>
          </v-card-title>
          <v-data-table
            :headers="headers"
            :items="getCrawlers"
            :search="search"
            class="elevation-1"
            :loading="isLoading"
            loading-text="Loading... Please wait">
            <template v-slot:item.name="{ item }">
              <b>{{item.name}}</b>
            </template>
            <template v-slot:item.start_url="{ item }">
              <a :href="item.start_url" target="_blank">{{item.start_url}}</a>
            </template>
            <template v-slot:item.state="{ item }">
                <span v-if="getCrawlerInfo(item.task_id) != null && crawlerButtonControlSwitch(item.task_id) ">
                  <!-- {{ getJobState }} -->
                  <v-chip
                    class="ma-2"
                    small
                    v-if="getJobState == 'pending'"
                  >
                  <v-icon left small>
                    mdi-cog-sync
                  </v-icon>
                    {{getJobState}}
                  </v-chip>
                  <v-chip
                    class="ma-2"
                    small
                    color="red"
                    text-color="white"
                    v-else-if="getJobState == 'running'"
                  >
                    <span style="margin: 3px">
                      <i  class="fas fa-cog fa-spin" style="color:white"></i>
                    </span>
                      {{getJobState}}
                  </v-chip>
                  <v-chip
                    class="ma-2"
                    small
                    color="green"
                    text-color="white"
                    v-else-if="getJobState == 'finished'"
                  >
                  <v-icon left small>
                    mdi-check-all
                  </v-icon>
                  {{getJobState}}
                  </v-chip>
                </span>
                <span v-else-if="getCrawlerInfo(item.task_id) != null">
                  <!-- {{getCrawlerInfo(item.task_id).state}} -->
                  <v-chip
                    class="ma-2"
                    small
                    v-if="getCrawlerInfo(item.task_id).state == 'pending'"
                  >
                    {{getCrawlerInfo(item.task_id).state}}
                  </v-chip>
                  <v-chip
                    class="ma-2"
                    small
                    color="red"
                    text-color="white"
                    v-else-if="getCrawlerInfo(item.task_id).state == 'running'"
                  >
                    <span style="margin: 3px">
                      <i class="fas fa-cog fa-spin" style="color:white"></i>
                    </span>
                    {{getCrawlerInfo(item.task_id).state}}
                  </v-chip>
                  <v-chip
                    class="ma-2"
                    small
                    color="green"
                    text-color="white"
                    v-else-if="getCrawlerInfo(item.task_id).state == 'finished'"
                  >
                  <v-icon left small>
                    mdi-check-all
                  </v-icon>
                  {{getCrawlerInfo(item.task_id).state}}
                  </v-chip>
                </span>
                <span v-else><v-icon small>mdi-check-outline</v-icon></span>
            </template>
            <template v-slot:item.task_id="{ item }">
                <v-chip
                    class="ma-2"
                    small
                    color="orange"
                    text-color="white"
                    v-if="item.task_id == 'New Crawler'"
                  >
                  <v-icon left small>
                    mdi-alert-decagram
                  </v-icon>
                  {{item.task_id}}
                  </v-chip>
                  <span v-else>{{item.task_id}}</span>
            </template>
              <template v-slot:item.btn_run_stop="{ item }">
                <v-btn
                  icon
                  v-if="crawlerButtonControlSwitch(item.task_id) && getJobState != 'finished'"
                  :disabled="getLoadingRunningCrawlerExecution || stoppingCrawler"
                  v-on:click="exitRunningJob(item.task_id)"
                  color="black">
                  <v-icon>mdi-close-circle-outline</v-icon>
                </v-btn>
                <v-btn
                  icon
                  v-else
                  :disabled="getLoadingRunningCrawlerExecution || getJobState != 'finished' || stoppingCrawler || getDeletingCrawlerLoading"
                  v-on:click="executeCrawler(item.crawlerId)"
                  color="black">
                  <v-icon>mdi-play</v-icon>
                </v-btn>
                <!-- <span>{{item.crawlerId}}</span> -->
              </template>
              <template v-slot:item.btn_delete="{ item }">
                <v-btn
                  icon
                  :disabled="getLoadingRunningCrawlerExecution || getJobState != 'finished'"
                  v-on:click="removeCrawler(item.crawlerId)"
                  color="black">
                  <v-icon>mdi-delete</v-icon>
                </v-btn>
              </template>
            </v-data-table>
        </v-card>
        <v-overlay :value="stoppingCrawler">
          <v-progress-circular
            indeterminate
            size="64"
          ></v-progress-circular>
        </v-overlay>

        <v-dialog
          v-model="getDeletingCrawlerLoading"
          hide-overlay
          persistent
          width="300"
        >
          <v-card
            color="primary"
            dark
          >
            <v-card-text>
              Please stand by
              <v-progress-linear
                indeterminate
                color="white"
                class="mb-0"
              ></v-progress-linear>
            </v-card-text>
          </v-card>
        </v-dialog>
        <v-snackbar
        ref="snackbarDeleteCrawler"
        elevation="24"
        color="success"
        v-model="crawlerAlert"
        :timeout="crawlerAlertTimeoutMessage"
        >
        <v-icon large>{{crawlerAlertIcon}}</v-icon>
        <b style="font-size:150%; margin-left:5px">{{ crawlerAlertMessage }}</b>
        <template v-slot:action="{ attrs }">
          <v-btn
            color="white"
            text
            v-bind="attrs"
            @click="crawlerAlert = false"
          >
            Close
          </v-btn>
        </template>
    </v-snackbar>
      </v-main>
   </v-app>
</template>


<script>
import {mapActions,mapGetters} from "vuex"
  export default {

    name: 'CrawlersList',
    
    data () {
      return {
        search: '',
        inProcess: true,
        startLongPolling:false,
        polling: null,
        stoppingCrawler: false,
        crawlerAlert: false,
        crawlerAlertTimeoutMessage: 5000,
        crawlerAlertMessage: '',
        crawlerAlertIcon: '',
        crawlerInProcess:{
          project: 'default',
          job: ''
        },
        headers: [
          {
            text: 'Crawler Name',
            align: 'start',
            value: 'name',
          },
          { text: 'Start URL', value: 'start_url', sortable: false },
          { text: 'State', value: 'state', sortable: false },
          { text: 'Unique ID', value: 'task_id', sortable: false},
          { text: ' ', value: 'btn_run_stop', sortable: false },
          { text: ' ', value: 'btn_delete', sortable: false },
        ],
        // crawlers_data: getCrawlers
      }
    },

    mounted () {
      this.getCrawlersData();
    },

    watch: {
      getFullPath () {
        this.getCrawlersData()
      },

      // startLongPolling () {
      //   console.log("LongPolling")
      //   this.pollingFreshCrawlersInfo()
      // },

      getJobState(newVal, oldVal){
          console.log("OLD: "+oldVal)
          console.log("NEW: "+newVal)
          console.log("POLLING!!!!!!!!")
          this.pollingFreshCrawlersInfo()
      }

    },

    computed: {
      ...mapGetters("Auth",["isAuth"]),
      ...mapGetters("Crawler",["getCrawlers"]),
      ...mapGetters("Crawler",["isLoading"]),
      ...mapGetters("Crawler",["getLoadingRunningCrawlerExecution"]),
      ...mapGetters("Crawler",["getRunningCrawler"]),
      ...mapGetters("Crawler",["getRunningCrawlerTaskId"]),
      ...mapGetters("Crawler",["getJob"]),
      ...mapGetters("Crawler",["getFinishedJobs"]),
      ...mapGetters("Crawler",["getJobState"]),
      ...mapGetters("Crawler",["getDeletingCrawlerLoading"]),
      

      getFullPath () {
        return this.$route.path
      },

      // activateLongPolling(){
      //   console.log(this.getJobState)
      //   return this.startLongPolling && this.getJobState != 'finished'
      // }

      

      
    },

    methods:{
        ...mapActions('Crawler',['getAllCrawlers']),
        ...mapActions('Crawler',['runCrawler']),
        ...mapActions('Crawler',['getJobs']),
        ...mapActions('Crawler',['cancelRunningJob']),
        ...mapActions('Crawler',['getRuningJobs']),
        ...mapActions('Crawler',['deleteCrawler']),

        getCrawlersData(){
          this.getAllCrawlers(this.crawlerInProcess)
        },


        executeCrawler(id){
          let playload = {'id': id, 'form': this.crawlerInProcess}
          console.log(playload)
          this.runCrawler(playload)
          this.startLongPolling=true
          this.crawlerAlert = true
          this.crawlerAlertMessage = "Crawler started"
          this.crawlerAlertIcon = 'mdi-spider'
          // this.pollingFreshCrawlersInfo()
        },

        exitRunningJob(taskId){
          this.crawlerInProcess['job'] = taskId
          this.stoppingCrawler = true
          this.cancelRunningJob(this.crawlerInProcess)
          this.inProcess = false
          this.getAllCrawlers(this.crawlerInProcess)
        },

        removeCrawler(crawlerId){
          let playload = {}
          playload['crawler_id'] = crawlerId
          playload['crawlerInProcess'] = this.crawlerInProcess
          playload['vm'] = this
          this.deleteCrawler(playload)
        },

        getCrawlerInfo (task_id){
          let jobs = this.getJob
          let finished_jobs = this.getFinishedJobs
          let crawler = null
          if(jobs.length > 0){
              crawler = jobs.find(o => o.id === task_id);
              if(crawler == null && finished_jobs.length > 0){
                  crawler = finished_jobs.find(o => o.id === task_id);
              }
          }
          else if(finished_jobs.length > 0){
              crawler = finished_jobs.find(o => o.id === task_id);
          }

          return crawler
        },

        crawlerButtonControlSwitch(task_id){
          let isActive = this.getCrawlerInfo(task_id) ? this.getCrawlerInfo(task_id).isActive : false
          
          return isActive
        },

        pollingFreshCrawlersInfo(){
          // console.log(this.activateLongPolling)
            var interval = setInterval(
              function () { 
                console.log("LongPolling--->"+this.getJobState)
                this.getAllCrawlers(this.crawlerInProcess)
                console.log('interval--->'+ this.isAuth)
                // this.$store.commit('Crawler/SET_POLLING_INTERVAL', interval)
                if(this.getJobState == 'finished' || !this.isAuth){
                  console.log("STOP POLLING!!")
                  clearInterval(interval);
                  this.stoppingCrawler = false
                  this.crawlerAlert = true
                  this.crawlerAlertMessage = "Crawler finished"
                  this.crawlerAlertIcon = 'mdi-spider'
                  // clearInterval(this.$store.getters['Crawler/getPollingInterval'])
                }
              }
              .bind(this), 3000)
            // this.polling = interval
        }

    },

    // beforeDestroy () {
    //   clearInterval(this.polling)
    // },

    created () {
      if(this.getJobState != 'finished'){
        console.log("created===>")
        this.pollingFreshCrawlersInfo()
      }
    }
    
  }
</script>
