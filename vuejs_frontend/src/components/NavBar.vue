<template>
<div>
      <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        <v-toolbar-title>Project PFE</v-toolbar-title>
      </div>

      <v-spacer></v-spacer>

      
      <v-btn
        text
        v-for="item in menuItems"
        :key="item.title"
        :to="item.path">
        <v-badge
          v-if="item.id == 2 && getJobState != 'finished'"
          dot
          left
          :bordered="false"
          color="red"
          overlap
        >
          <v-icon left dark>{{ item.icon }}</v-icon>
        </v-badge>
        <v-icon left dark v-else>{{ item.icon }}</v-icon>
        <span class="mr-2">{{ item.title }}</span>
      </v-btn>
      <v-chip
        class="ma-2"
        color="green"
        text-color="white"
      >
        <v-icon left dark>mdi-account-tie</v-icon>
        {{ getUser.username }}
      </v-chip>
      <v-chip
        class="ma-2"
        :color="getOtherErrors.length > 0 ? 'black' : 'green'"
        text-color="white"
      >
        <v-icon left dark>{{ getOtherErrors.length > 0 ? 'mdi-server-off' : 'mdi-server' }}</v-icon>
        {{ getOtherErrors.length > 0 ? 'Server Error' : 'Server Running' }}
      </v-chip>
      <v-btn
        text
        @click="logout()">
        <span class="mr-2">Logout</span>
        <v-icon left dark>mdi-logout</v-icon>
      </v-btn>
      
    </v-app-bar>
    <v-overlay :value="isLogoutLoading">
      <v-progress-circular
        indeterminate
        size="64"
      ></v-progress-circular>
    </v-overlay>
    
</div>
</template>

<script>
import {mapActions,mapGetters} from "vuex"

export default {
  name: "NavBar",
  data(){
    return {
      appTitle: 'PFE Project',
      sidebar: false,
      menuItems: [
          { title: 'New Crawler', path: '/create_crawler', icon: 'mdi-lead-pencil', id: 1 },
          { title: 'Crawlers', path: '/crawlers_list', icon: 'mdi-spider', id: 2 },
     ]
    }
  },

  methods: {
    ...mapActions('Auth',['logout']),
  },
  computed: {
    ...mapGetters("Auth", ["getUser"]),
    ...mapGetters("Auth", ["isLogoutLoading"]),
    ...mapGetters("Crawler",["getJobState"]),
    ...mapGetters("Crawler",["getOtherErrors"]),
    


  }

};

</script>
