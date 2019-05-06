import Vue from 'vue'
import './plugins/axios'
import App from './App.vue'
import router from './router'
import { store } from './store'
import moment from 'moment'

Vue.config.productionTip = false
Vue.prototype.moment = moment

new Vue({
  router,
  store,
  render: function (h) { return h(App) }
}).$mount('#app')
