<template>
  <div class="register-wrapper columns">
    <div class="column is-offset-one-quarter is-half">
      <div class="message is-warning" v-show="showAlert">
        <div class="message-header">
          <p>Alert</p>
          <button class="delete" aria-label="delete" @click="alertMessage = ''"></button>
        </div>
        <div class="message-body">
          {{ alertMessage }}
        </div>
      </div>
      <div class="field">
        <label class="label">Username</label>
        <div class="control has-icons-right">
          <input :class="usernameClass" type="text" placeholder="Username" v-model="username" :disabled="disableInputs == true" />
          <span class="icon is-small is-right">
            <i class="fa fa-user"></i>
          </span>
        </div>
      </div>
      <div class="field">
        <label class="label">Password</label>
        <div class="control has-icons-right">
          <input :class="passwordClass" type="password" placeholder="Password" v-model="password" :disabled="disableInputs == true"/>
          <span class="icon is-small is-right">
            <i class="fa fa-key"></i>
          </span>
        </div>
      </div>
      <div class="field">
        <label class="label">Retype Password</label>
        <div class="control has-icons-right">
          <input :class="password2Class" type="password" placeholder="Retype Password" v-model="password2" :disabled="disableInputs == true"/>
          <span class="icon is-small is-right">
            <i class="fa fa-key"></i>
          </span>
        </div>
      </div>
      <div class="field">
        <label class="label">Email</label>
        <div class="control has-icons-right">
          <input :class="emailClass" type="text" placeholder="Username" v-model="email" :disabled="disableInputs == true" />
          <span class="icon is-small is-right">
            <i class="fa fa-envelope"></i>
          </span>
        </div>
      </div>
      <div class="field">
        <button :class="buttonClass" @click="register">Register</button>
      </div>
    </div>
  </div>
</template>

<script>
  import axios from 'axios'
  import config from '../config'

  export default {
    name: 'Login',
    data () {
      return {
        username: '',
        password: '',
        password2: '',
        email: '',
        disableInputs: false,
        alertMessage: '',
        alertUsername: false,
        alertPassword: false,
        alertPassword2: false,
        alertEmail: false
      }
    },
    computed: {
      usernameClass: function () {
        return {
          input: true,
          'is-warning': this.alertUsername
        }
      },
      passwordClass: function () {
        return {
          input: true,
          'is-warning': this.alertPassword
        }
      },
      password2Class: function () {
        return {
          input: true,
          'is-warning': this.alertPassword2
        }
      },
      emailClass: function () {
        return {
          input: true,
          'is-warning': this.alertEmail
        }
      },
      buttonClass: function () {
        return {
          button: true,
          'is-primary': true,
          'is-pulled-right': true,
          'is-loading': this.disableInputs
        }
      },
      showAlert: function () {
        return this.alertMessage !== ''
      }
    },
    methods: {
      register () {
        // Validate our inputs
        if (!this.isFormValid()) {
          return
        }

        this.disableInputs = true
        let baseUrl = config['corp-hq-api-url']
        axios.post(baseUrl + 'register', {
          username: this.username,
          password: this.password,
          email: this.email
        })
        .then((resp) => {
          this.disableInputs = false
          this.$router.push({ path: this.$router.history.current.query.referrer })
        })
        .catch((err) => {
          if (err.response === undefined) {
            this.alertMessage = err.message + '; Please try again later.'
          } else {
            this.alertMessage = 'Registration failed. Please try again.'
            this.password = ''
            this.password2 = ''
            console.log(err)
          }
          this.disableInputs = false
        })
      },
      isFormValid: function () {
        this.resetAlerts()

        if (this.username === '') {
          this.alertMessage = 'Username is a required field.'
          this.alertUsername = true
          return false
        }

        if (this.password === '') {
          this.alertMessage = 'Password is a required field.'
          this.alertPassword = true
          return false
        }

        if (this.password2 === '') {
          this.alertMessage = 'Password is a required field.'
          this.alertPassword2 = true
          return false
        }

        if (this.password2 !== this.password) {
          this.alertMessage = 'Password fields do not match.'
          this.alertPassword = true
          this.alertPassword2 = true
          return false
        }

        if (this.email === '') {
          this.alertMessage = 'Email is a required field.'
          this.alertEmail = true
          return false
        }

        return true
      },
      resetAlerts () {
        this.alertMessage = ''
        this.alertUsername = false
        this.alertPassword = false
        this.alertPassword2 = false
        this.alertEmail = false
      }
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
