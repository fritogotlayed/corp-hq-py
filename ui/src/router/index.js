import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import Hello2 from '@/components/Hello2'
import Login from '@/components/Login'
import Register from '@/components/Register'

Vue.use(Router)

export default new Router({
  routes: [
    { path: '/', name: 'Hello', component: Hello },
    { path: '/hello2', name: 'Hello2', component: Hello2 },
    { path: '/login', name: 'Login', component: Login },
    { path: '/register', name: 'Register', component: Register }
  ]
})
