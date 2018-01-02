import Vue from 'vue'
import Router from 'vue-router'
import Market from '@/components/market/market'
import Page2 from '@/components/page2'

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
            path: '/page2',
            name: 'Page2',
            component: Page2
        }
    ]
})
