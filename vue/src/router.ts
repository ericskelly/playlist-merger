import Vue from 'vue';
import Router from 'vue-router';
import spotifyLogin from './components/spotifyLogin.vue';
import main from './components/main.vue';

Vue.use(Router);

export default new Router({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'main',
      component: main,
      meta: { title: 'Playlist Merger' },
    },
    {
      path: '/login',
      name: 'spotifyLogin',
      component: spotifyLogin,
      meta: { title: 'Playlist Merger - Login' },
    },
  ],
});
