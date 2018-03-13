import Vue from 'vue'
import Router from 'vue-router'

import Market from '@/components/market/market'
import AddMessages from '@/components/services_messages/add_messages'
import EditMessagesServices from '@/components/services_messages/edit_messages'
import AddMarketImages from '@/components/images/add-image-panel'
import EditPanel from '@/components/market/edit/panel'
import EditImagesMarket from '@/components/images/edit-images-panel'
import EditBasicMarket from '@/components/market/edit/basic_market'
import AddMarket from '@/components/market/add/add_market'

import LogIn from '@/components/login'
import SignUp from '@/components/signUp/signUp'
import NotFound from '@/components/notFound'
import hexagon from '@/components/hexagon-spinner.vue'
import axios from 'axios';

Vue.use(Router)
Vue.component('loader',hexagon)

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
        {
            path: '/signup',
            name: 'SignUp',
            component: SignUp
        },
        {
            path: '/dodaj_wiadomosc/:market_id',
            name: 'AddMessages',
            component: AddMessages,
            meta: { requiresAuth: true }
        },
        {
            path: '/dodaj_obrazek/:market_id',
            name: 'AddMarketImages',
            component: AddMarketImages,
            meta: { requiresAuth: true }
        },
        {
            path: '/panel_edycji/:market_id',
            name: 'EditPanel',
            component: EditPanel,
            meta: { requiresAuth: true }
        },
        {
            path: '/edytuj_market/:market_id',
            name: 'EditBasicMarket',
            component: EditBasicMarket,
            meta: { requiresAuth: true }
        },
        {
            path: '/edytuj_wiadomosci/:market_id',
            name: 'EditMessagesServices',
            component: EditMessagesServices,
            meta: { requiresAuth: true }
        },
        {
            path: '/edytuj_obrazki/:market_id',
            name: 'EditImagesMarket',
            component: EditImagesMarket,
            meta: { requiresAuth: true }
        },
        {
          path:'*',
          name:'NotFound',
          component:NotFound,
        }
    ]
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {

    axios.post(process.env.BACKEND+"ngo/token-verify/", {token:localStorage.getItem('jwtToken')})
    .then(response =>{
      const user_data = response.data.user;
      localStorage.setItem('coins', user_data.coins);

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
