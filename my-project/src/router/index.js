import Vue from 'vue'
import Router from 'vue-router'
import Market from '@/components/market/market'
import AddMarket from '@/components/add_market'

Vue.use(Router)

export default new Router({
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
            component: Market
        },
        {
            path: '/dodaj_market',
            name: 'AddMarket',
            component: AddMarket
        }
    ]
})
