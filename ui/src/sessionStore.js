import Vue from 'vue'
import Vuex from 'vuex'
// Referenced examples at: https://github.com/vuejs/vuex

Vue.use(Vuex)

// root state object.
// each Vuex instance is just a single state tree.
const state = {
  token: null,
  exipry: null,
  isLoggedIn: false,
  previousIsLoggedIn: false
}

// mutations are operations that actually mutate the state.
// each mutation handler gets the entire state tree as the
// first argument, followed by additional payload arguments.
// mutations must be synchronous and can be recorded by plugins
// for debugging purposes.
const mutations = {
  setToken (state, token) {
    console.log('setToken called.')
    state.token = token
    state.isLoggedIn = !!token
  },
  setExpiry (state, expiry) {
    console.log('setExpiry called.')
    state.expiry = expiry
    state.isLoggedIn = !!expiry
  },
  getToken (state) {
    var now = new Date()
    state.previousIsLoggedIn = state.isLoggedIn
    if (state.exipry && now < state.expiry) {
      state.isLoggedIn = false
      return this.state.token
    }
    state.isLoggedIn = false
    return null
  }
}

// actions are functions that cause side effects and can involve
// asynchronous operations.
const actions = {
  setToken ({ commit }, data) {
    console.log('setToken action called.')
    commit('setToken', data)
  },
  setExpiry: ({ commit }, expiry) => commit('setExpiry', expiry),
  getToken ({ commit, state }) {
    if (state.previousIsLoggedIn !== state.isLoggedIn) {
      commit('isLoggedIn')
    }
  }
}

// getters are functions
const getters = {
  loggedIn: state => state.isLoggedIn
}

export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations
})
