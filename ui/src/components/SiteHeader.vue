<template>
  <div class="navbar" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <!-- TODO: Put a navbar brand here. -->
    </div>
    <div class="navbar-menu">
      <div class="navbar-item">
        <button type="button" class="button is-link" @click="home">Home</button>
      </div>
      <div class="navbar-item" v-show="showLogin">
        <button type="button" class="button is-link" @click="login">Login</button>
      </div>
      <div class="navbar-item" v-show="showLogout">
        <button type="button" :class="logoutButtonClass" @click="logout">Logout</button>
      </div>
      <div class="navbar-item" v-show="showRegister">
        <button type="button" class="button is-link navbar-item" @click="register">Register</button>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import config from '../config'

  export default {
    name: 'SiteHeader',
    data () {
      return {
        msg: 'Welcome to Your Vue.js App',
        disableLogout: false
      }
    },
    computed: {
      showLogin: function () {
        return !this.$store.state.isLoggedIn
        // return !this.$store.state.isLoggedIn && this.$router.history.current.name !== 'Login'
      },
      showLogout: function () {
        return this.$store.state.isLoggedIn
      },
      showRegister: function () {
        return !this.$store.state.isLoggedIn
      },
      logoutButtonClass: function () {
        return {
          button: true,
          'is-link': true,
          'is-loading': this.disableLogout
        }
      }
    },
    methods: {
      home: function () {
        this.$router.push({path: '/'})
      },
      login: function () {
        var referrer = this.$router.history.current.fullPath
        if (this.$router.history.current.name === 'Register' &&
            this.$router.history.current.query.referrer !== undefined) {
          referrer = this.$router.history.current.query.referrer
        }
        if (this.$router.history.current.name !== 'Login') {
          this.$router.push({path: '/login', query: {referrer: referrer}})
        }
      },
      logout: function () {
        this.disableLogout = true
        let baseUrl = config['corp-hq-api-url']
        axios.post(baseUrl + 'logout', {
          token: this.$store.state.token
        })
        .then((resp) => {
          sessionStorage.removeItem('corp-hq-api-auth-token')
          sessionStorage.removeItem('corp-hq-api-auth-token-exp')
          this.$store.commit('setToken', null)
          this.$store.commit('setExpiry', null)
          this.disableLogout = false
          // TODO: Should this redirect somewhere?
          // this.$router.push({ path: this.$router.history.current.query.referrer })
        })
        .catch((err) => {
          console.log(err)
          this.disableLogout = false
          // if (err.response === undefined) {
          //    this.alertMessage = err.message + '; Please try again later.'
          // } else if (err.response.status === 400) {
          //   this.alertMessage = 'Login failed. Please try again.'
          //   this.password = ''
          // } else {
          //   console.log(err)
          // }
          // this.disableInputs = false
        })
      },
      register: function () {
        var referrer = this.$router.history.current.fullPath
        if (this.$router.history.current.name === 'Login' &&
          this.$router.history.current.query.referrer !== undefined) {
          referrer = this.$router.history.current.query.referrer
        }
        if (this.$router.history.current.name !== 'Register') {
          this.$router.push({path: '/register', query: {referrer: referrer}})
        }
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
