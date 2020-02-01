import Vue from 'vue';
import Router from 'vue-router';
import SpotifyLogin from './components/SpotifyLogin.vue';
import MainPage from './components/MainPage.vue';

Vue.use(Router);

export default new Router({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'MainPage',
      component: MainPage,
      meta: { title: 'Playlist Merger' },
    },
    {
      path: '/login',
      name: 'SpotifyLogin',
      component: SpotifyLogin,
      meta: { title: 'Playlist Merger - Login' },
    },
  ],
});
