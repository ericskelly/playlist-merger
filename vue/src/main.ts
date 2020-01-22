import Vue from 'vue';
import App from './App.vue';
import router from './router';
import BootstrapVue from "bootstrap-vue";
import Vuetify from 'vuetify';
import 'vuetify/dist/vuetify.min.css';
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';

Vue.config.productionTip = false;
Vue.use(BootstrapVue);
const vuetifyOptions = {};
Vue.use(Vuetify);

new Vue({
  router,
  render: (h) => h(App),
  vuetify: new Vuetify(vuetifyOptions),
}).$mount('#app');
