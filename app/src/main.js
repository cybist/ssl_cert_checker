import Vue from 'vue'
import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
import App from './App.vue'
import axios from 'axios'
import './registerServiceWorker'
import VueMeta from 'vue-meta'
Vue.use(VueMeta)
Vue.use(BootstrapVue)
Vue.config.productionTip = false
Vue.prototype.$axios = axios

new Vue({
  render: h => h(App),
}).$mount('#app')
