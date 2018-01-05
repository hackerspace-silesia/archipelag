import Vue from 'vue'
import Router from 'vue-router'
import Market from '@/components/market/market'
import AddMarket from '@/components/add_market'
import LogIn from '@/components/login'
import Auth from '@/services/auth'
import axios from 'axios';
Vue.use(Router)

const router = new Router({
    routes: [
        {
            path: "/",
            redirect: {
                name: "market"
            }
        },
        {
            path: '/market',
            name: 'market',
            component: Market,
            meta: { requiresAuth: true }
        },
        {
            path: '/dodaj_market',
            name: 'AddMarket',
            component: AddMarket,
            meta: { requiresAuth: true }
        },
        {
            path: '/login',
            name: 'LogIn',
            component: LogIn
        },
    ]
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {

    axios.post("http://127.0.0.1:8000/ngo/token-verify/", {token:localStorage.getItem('jwtToken')})
    .then(response =>{
    // JSON responses are automatically parsed.
      next()
    }).catch(e => {
      next({
         path: '/login',
       });})
  } else {
    next();
  }
})

export default router
