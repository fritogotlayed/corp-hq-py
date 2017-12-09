<template>
  <div class="hello">
    <p>Hello 2</p>
    <router-link class="button is-link" to="/">Hello1</router-link>
    <button type="button" class="button is-link" @click="login">Login</button>
    <div>
      <img src="../assets/logo.png">
    </div>
    <div>
      <h1>{{ msg }}</h1>
      <h2>Essential Links</h2>
      <ul>
        <li><a class="button is-link" href="https://vuejs.org" target="_blank">Core Docs</a></li>
        <li><a class="button is-link" href="https://forum.vuejs.org" target="_blank">Forum</a></li>
        <li><a class="button is-link" href="https://chat.vuejs.org" target="_blank">Community Chat</a></li>
        <li><a class="button is-link" href="https://twitter.com/vuejs" target="_blank">Twitter</a></li>
        <br>
        <li><a class="button is-link" href="http://vuejs-templates.github.io/webpack/" target="_blank">Docs for This Template</a></li>
      </ul>
      <h2>Ecosystem</h2>
      <ul>
        <li><a class="button is-link" href="http://router.vuejs.org/" target="_blank">vue-router</a></li>
        <li><a class="button is-link" href="http://vuex.vuejs.org/" target="_blank">vuex</a></li>
        <li><a class="button is-link" href="http://vue-loader.vuejs.org/" target="_blank">vue-loader</a></li>
        <li><a class="button is-link" href="https://github.com/vuejs/awesome-vue" target="_blank">awesome-vue</a></li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'hello',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App'
    }
  },
  methods: {
    login: function () {
      this.$router.push({path: '/login', query: {referrer: this.$router.history.current.fullPath}})
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h1, h2 {
    font-weight: normal;
  }

  ul {
    list-style-type: none;
    padding: 0;
  }

  li {
    display: inline-block;
    margin: 0 10px;
  }

  a {
    color: #42b983;
  }

  .button {
    color: #42b983;
    text-decoration: none;
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
  }

  .hello {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #455b6f;
    margin-top: 60px;
  }
</style>
